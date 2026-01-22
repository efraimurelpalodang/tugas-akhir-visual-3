import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, Qt


class TransaksiKeluarHandler:
    def __init__(self, page, user):
        self.page = page
        self.user = user

        self.page.pushButton_4.clicked.connect(self.save_transaksi_to_db)
        self.page.pushButton_2.clicked.connect(self.edit_selected_row)
        self.page.pushButton_3.clicked.connect(self.delete_selected_row)

        self.load_combobox_data()
        self.load_transaksi_keluar_table()

    # ================= DB CONNECTION =================
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    # ================= COMBOBOX =================
    def load_combobox_data(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nama_barang FROM barang ORDER BY nama_barang ASC")
        self.page.comboBox.clear()

        for row in cursor.fetchall():
            self.page.comboBox.addItem(row["nama_barang"], row["id"])

        cursor.close()
        conn.close()

    # ================= TABLE =================
    def load_transaksi_keluar_table(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                t.id AS id_transaksi,
                t.kode_transaksi,
                b.nama_barang,
                dt.quantity,
                t.tanggal,
                t.total_harga,
                t.keterangan
            FROM detail_transaksi dt
            JOIN transaksi t ON dt.id_transaksi = t.id
            JOIN barang b ON dt.id_barang = b.id
            WHERE t.type_transaksi = 'keluar'
            ORDER BY t.created_at DESC
        """)

        table = self.page.tableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setColumnCount(7)

        for data in cursor.fetchall():
            row = table.rowCount()
            table.insertRow(row)

            # simpan ID transaksi (hidden)
            item_id = QTableWidgetItem(str(data["id_transaksi"]))
            item_id.setData(Qt.UserRole, data["id_transaksi"])
            table.setItem(row, 0, item_id)

            table.setItem(row, 1, QTableWidgetItem(data["kode_transaksi"]))
            table.setItem(row, 2, QTableWidgetItem(data["nama_barang"]))
            table.setItem(row, 3, QTableWidgetItem(str(data["quantity"])))
            table.setItem(row, 4, QTableWidgetItem(str(data["tanggal"])))
            table.setItem(row, 5, QTableWidgetItem(str(data["total_harga"])))

            keterangan = data["keterangan"] if data["keterangan"] else ""
            table.setItem(row, 6, QTableWidgetItem(keterangan))

        table.setColumnHidden(0, True)
        table.setEditTriggers(table.NoEditTriggers)
        table.cellClicked.connect(self.fill_form_from_table)

        cursor.close()
        conn.close()

    # ================= SAFE GET TEXT =================
    def _text(self, table, r, c):
        item = table.item(r, c)
        return item.text() if item else ""

    # ================= CLICK TABLE =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget

        self.page.lineEdit.setText(self._text(table, row, 1))

        index = self.page.comboBox.findText(self._text(table, row, 2))
        if index >= 0:
            self.page.comboBox.setCurrentIndex(index)

        qty = self._text(table, row, 3)
        self.page.spinBox.setValue(int(qty) if qty.isdigit() else 0)

        self.page.dateEdit.setDate(
            QDate.fromString(self._text(table, row, 4), "yyyy-MM-dd")
        )

        self.page.lineEdit_5.setText(self._text(table, row, 5))
        self.page.lineEdit_3.setText(self._text(table, row, 6))

    # ================= EDIT =================
    def edit_selected_row(self):
        table = self.page.tableWidget
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih transaksi dulu")
            return

        id_transaksi = int(table.item(row, 0).text())

        id_barang_baru = self.page.comboBox.currentData()
        jumlah_baru = self.page.spinBox.value()
        tanggal = self.page.dateEdit.date().toString("yyyy-MM-dd")
        total = self.page.lineEdit_5.text()
        keterangan = self.page.lineEdit_3.text()

        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id_barang, quantity
                FROM detail_transaksi
                WHERE id_transaksi = %s
            """, (id_transaksi,))
            lama = cursor.fetchone()

            if not lama:
                QMessageBox.critical(self.page, "Error", "Detail transaksi tidak ditemukan")
                return

            cursor.execute("""
                UPDATE barang SET stok = stok + %s WHERE id = %s
            """, (lama["quantity"], lama["id_barang"]))

            cursor.execute("""
                UPDATE transaksi
                SET tanggal=%s, total_harga=%s, keterangan=%s
                WHERE id=%s
            """, (tanggal, total, keterangan, id_transaksi))

            cursor.execute("""
                UPDATE detail_transaksi
                SET id_barang=%s, quantity=%s
                WHERE id_transaksi=%s
            """, (id_barang_baru, jumlah_baru, id_transaksi))

            cursor.execute("""
                UPDATE barang SET stok = stok - %s WHERE id = %s
            """, (jumlah_baru, id_barang_baru))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Transaksi diperbarui")
            self.load_transaksi_keluar_table()

        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", str(e))
        finally:
            cursor.close()
            conn.close()

    # ================= DELETE (UI ONLY) =================
    def delete_selected_row(self):
        table = self.page.tableWidget
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih baris dulu")
            return

        if QMessageBox.question(
            self.page, "Konfirmasi", "Hapus baris ini?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            table.removeRow(row)

    # ================= SAVE =================
    def save_transaksi_to_db(self):
        kode = self.page.lineEdit.text().strip()
        id_barang = self.page.comboBox.currentData()
        jumlah = self.page.spinBox.value()
        tanggal = self.page.dateEdit.date().toString("yyyy-MM-dd")
        total = self.page.lineEdit_5.text().strip()
        keterangan = self.page.lineEdit_3.text().strip()
        id_user = self.user["id"]

        if not kode or not total:
            QMessageBox.warning(self.page, "Peringatan", "Kode & total wajib diisi")
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO transaksi
                (kode_transaksi, id_user, id_supplier, tanggal,
                 total_harga, keterangan, type_transaksi)
                VALUES (%s, %s, NULL, %s, %s, %s, 'keluar')
            """, (kode, id_user, tanggal, total, keterangan))

            id_transaksi = cursor.lastrowid

            cursor.execute("""
                INSERT INTO detail_transaksi
                (id_transaksi, id_barang, quantity)
                VALUES (%s, %s, %s)
            """, (id_transaksi, id_barang, jumlah))

            cursor.execute("""
                UPDATE barang SET stok = stok - %s WHERE id = %s
            """, (jumlah, id_barang))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Transaksi berhasil disimpan")
            self.load_transaksi_keluar_table()

        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", str(e))
        finally:
            cursor.close()
            conn.close()
