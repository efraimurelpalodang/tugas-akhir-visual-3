import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, Qt


class TransaksiMasukHandler:
    def __init__(self, page, user):
        self.page = page
        self.user = user

        self.page.pushButton_4.clicked.connect(self.save_transaksi_to_db)
        self.page.pushButton_2.clicked.connect(self.edit_selected_row)
        self.page.pushButton_3.clicked.connect(self.delete_selected_row)

        self.load_combobox_data()
        self.load_transaksi_masuk_table()

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

        # barang
        cursor.execute("SELECT id, nama_barang FROM barang ORDER BY nama_barang ASC")
        self.page.comboBox.clear()
        for row in cursor.fetchall():
            self.page.comboBox.addItem(row["nama_barang"], row["id"])

        # supplier
        cursor.execute("SELECT id, nama_supplier FROM supplier ORDER BY nama_supplier ASC")
        self.page.comboBox_2.clear()
        for row in cursor.fetchall():
            self.page.comboBox_2.addItem(row["nama_supplier"], row["id"])

        cursor.close()
        conn.close()

    # ================= TABLE =================
    def load_transaksi_masuk_table(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                t.id AS id_transaksi,
                t.kode_transaksi,
                b.nama_barang,
                dt.quantity,
                s.nama_supplier,
                t.tanggal,
                t.total_harga,
                t.keterangan
            FROM detail_transaksi dt
            JOIN transaksi t ON dt.id_transaksi = t.id
            JOIN barang b ON dt.id_barang = b.id
            LEFT JOIN supplier s ON t.id_supplier = s.id
            WHERE t.type_transaksi = 'masuk'
            ORDER BY t.created_at DESC
        """)

        table = self.page.tableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setColumnCount(8)

        for data in cursor.fetchall():
            row = table.rowCount()
            table.insertRow(row)

            # ID transaksi (hidden)
            item_id = QTableWidgetItem(str(data["id_transaksi"]))
            item_id.setData(Qt.UserRole, data["id_transaksi"])
            table.setItem(row, 0, item_id)

            table.setItem(row, 1, QTableWidgetItem(data["kode_transaksi"]))
            table.setItem(row, 2, QTableWidgetItem(data["nama_barang"]))
            table.setItem(row, 3, QTableWidgetItem(str(data["quantity"])))
            table.setItem(row, 4, QTableWidgetItem(data["nama_supplier"] or ""))
            table.setItem(row, 5, QTableWidgetItem(str(data["tanggal"])))
            table.setItem(row, 6, QTableWidgetItem(str(data["total_harga"])))
            table.setItem(row, 7, QTableWidgetItem(data["keterangan"] or ""))

        table.setColumnHidden(0, True)
        table.setEditTriggers(table.NoEditTriggers)
        table.cellClicked.connect(self.fill_form_from_table)

        cursor.close()
        conn.close()

    # ================= SAFE TEXT =================
    def _text(self, table, r, c):
        item = table.item(r, c)
        return item.text() if item else ""

    # ================= CLICK TABLE =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget

        self.page.lineEdit.setText(self._text(table, row, 1))

        idx_barang = self.page.comboBox.findText(self._text(table, row, 2))
        if idx_barang >= 0:
            self.page.comboBox.setCurrentIndex(idx_barang)

        qty = self._text(table, row, 3)
        self.page.spinBox.setValue(int(qty) if qty.isdigit() else 0)

        idx_supplier = self.page.comboBox_2.findText(self._text(table, row, 4))
        if idx_supplier >= 0:
            self.page.comboBox_2.setCurrentIndex(idx_supplier)

        self.page.dateEdit.setDate(
            QDate.fromString(self._text(table, row, 5), "yyyy-MM-dd")
        )

        self.page.lineEdit_5.setText(self._text(table, row, 6))
        self.page.lineEdit_3.setText(self._text(table, row, 7))

    # ================= EDIT =================
    def edit_selected_row(self):
        table = self.page.tableWidget
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih transaksi dulu")
            return

        # 🔑 ID transaksi
        id_transaksi = int(table.item(row, 0).text())

        # 🔑 data baru dari form
        kode_baru = self.page.lineEdit.text().strip()
        id_barang_baru = self.page.comboBox.currentData()
        id_supplier_baru = self.page.comboBox_2.currentData()
        jumlah_baru = self.page.spinBox.value()
        tanggal = self.page.dateEdit.date().toString("yyyy-MM-dd")
        total = self.page.lineEdit_5.text().strip()
        keterangan = self.page.lineEdit_3.text().strip()

        if not kode_baru or not total:
            QMessageBox.warning(self.page, "Peringatan", "Kode & total wajib diisi")
            return

        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # ambil detail lama
            cursor.execute("""
                SELECT id_barang, quantity
                FROM detail_transaksi
                WHERE id_transaksi = %s
            """, (id_transaksi,))
            lama = cursor.fetchone()

            if not lama:
                QMessageBox.critical(self.page, "Error", "Detail transaksi tidak ditemukan")
                return

            # rollback stok lama
            cursor.execute("""
                UPDATE barang
                SET stok = stok - %s
                WHERE id = %s
            """, (lama["quantity"], lama["id_barang"]))

            # 🔥 UPDATE TRANSAKSI (LENGKAP)
            cursor.execute("""
                UPDATE transaksi
                SET kode_transaksi=%s,
                    id_supplier=%s,
                    tanggal=%s,
                    total_harga=%s,
                    keterangan=%s
                WHERE id=%s
            """, (kode_baru, id_supplier_baru, tanggal, total, keterangan, id_transaksi))

            # update detail transaksi
            cursor.execute("""
                UPDATE detail_transaksi
                SET id_barang=%s, quantity=%s
                WHERE id_transaksi=%s
            """, (id_barang_baru, jumlah_baru, id_transaksi))

            # tambah stok baru
            cursor.execute("""
                UPDATE barang
                SET stok = stok + %s
                WHERE id = %s
            """, (jumlah_baru, id_barang_baru))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Transaksi berhasil diperbarui")
            self.load_transaksi_masuk_table()

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
            self.page,
            "Konfirmasi",
            "Hapus baris ini?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            table.removeRow(row)

    # ================= SAVE =================
    def save_transaksi_to_db(self):
        kode = self.page.lineEdit.text().strip()
        id_barang = self.page.comboBox.currentData()
        jumlah = self.page.spinBox.value()
        id_supplier = self.page.comboBox_2.currentData()
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
                VALUES (%s, %s, %s, %s, %s, %s, 'masuk')
            """, (kode, id_user, id_supplier, tanggal, total, keterangan))

            id_transaksi = cursor.lastrowid

            cursor.execute("""
                INSERT INTO detail_transaksi
                (id_transaksi, id_barang, quantity)
                VALUES (%s, %s, %s)
            """, (id_transaksi, id_barang, jumlah))

            cursor.execute("""
                UPDATE barang SET stok = stok + %s WHERE id = %s
            """, (jumlah, id_barang))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Transaksi berhasil disimpan")
            self.load_transaksi_masuk_table()

        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", str(e))
        finally:
            cursor.close()
            conn.close()
