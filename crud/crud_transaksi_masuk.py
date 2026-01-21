import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate

class TransaksiMasukHandler:
    def __init__(self, page, user):
        self.page = page      # page ui yang sudah di load
        self.user = user      # data user login

        # hubungkan tombol
        self.page.pushButton_4.clicked.connect(self.save_transaksi_to_db)  # save
        self.page.pushButton_2.clicked.connect(self.edit_selected_row)     # edit
        self.page.pushButton_3.clicked.connect(self.delete_selected_row)   # delete

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

        # Barang
        cursor.execute("SELECT id, nama_barang FROM barang ORDER BY nama_barang ASC")
        barang_list = cursor.fetchall()
        self.page.comboBox.clear()
        for barang in barang_list:
            self.page.comboBox.addItem(barang["nama_barang"], barang["id"])

        # Supplier
        cursor.execute("SELECT id, nama_supplier FROM supplier ORDER BY nama_supplier ASC")
        supplier_list = cursor.fetchall()
        self.page.comboBox_2.clear()
        for supplier in supplier_list:
            self.page.comboBox_2.addItem(supplier["nama_supplier"], supplier["id"])

        cursor.close()
        conn.close()

    # ================= TABLE =================
    def load_transaksi_masuk_table(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT t.kode_transaksi, b.nama_barang, dt.quantity, s.nama_supplier, t.tanggal, t.total_harga, t.keterangan
            FROM detail_transaksi dt
            JOIN transaksi t ON dt.id_transaksi = t.id
            JOIN barang b ON dt.id_barang = b.id
            LEFT JOIN supplier s ON t.id_supplier = s.id
            WHERE t.type_transaksi='masuk'
            ORDER BY t.created_at DESC
        """)
        rows = cursor.fetchall()
        table = self.page.tableWidget
        table.setRowCount(0)

        for row in rows:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            table.setItem(row_pos, 0, QTableWidgetItem(row["kode_transaksi"]))
            table.setItem(row_pos, 1, QTableWidgetItem(row["nama_barang"]))
            table.setItem(row_pos, 2, QTableWidgetItem(str(row["quantity"])))
            table.setItem(row_pos, 3, QTableWidgetItem(row["nama_supplier"] if row["nama_supplier"] else ""))
            table.setItem(row_pos, 4, QTableWidgetItem(str(row["tanggal"])))
            table.setItem(row_pos, 5, QTableWidgetItem(str(row["total_harga"])))
            table.setItem(row_pos, 6, QTableWidgetItem(row["keterangan"]))

        # ❌ table read-only
        table.setEditTriggers(table.NoEditTriggers)

        # ✅ hubungkan klik row → isi form
        table.cellClicked.connect(self.fill_form_from_table)

        cursor.close()
        conn.close()

    # ================= CLICK TABLE → ISI FORM =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget
        self.page.lineEdit.setText(table.item(row, 0).text())  # kode

        # pilih barang di combobox sesuai nama
        nama_barang = table.item(row, 1).text()
        index_barang = self.page.comboBox.findText(nama_barang)
        if index_barang >= 0:
            self.page.comboBox.setCurrentIndex(index_barang)

        self.page.spinBox.setValue(int(table.item(row, 2).text()))

        # pilih supplier di combobox sesuai nama
        nama_supplier = table.item(row, 3).text()
        index_supplier = self.page.comboBox_2.findText(nama_supplier)
        if index_supplier >= 0:
            self.page.comboBox_2.setCurrentIndex(index_supplier)

        # set tanggal
        tanggal_str = table.item(row, 4).text()
        self.page.dateEdit.setDate(QDate.fromString(tanggal_str, "yyyy-MM-dd"))

        # total & keterangan
        self.page.lineEdit_5.setText(table.item(row, 5).text())
        self.page.lineEdit_3.setText(table.item(row, 6).text())

    # ================= EDIT =================
    def edit_selected_row(self):
        table = self.page.tableWidget
        selected = table.currentRow()
        if selected < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih baris yang akan diedit")
            return
        # update dari inputan ke baris yang dipilih
        table.setItem(selected, 0, QTableWidgetItem(self.page.lineEdit.text()))
        table.setItem(selected, 1, QTableWidgetItem(self.page.comboBox.currentText()))
        table.setItem(selected, 2, QTableWidgetItem(str(self.page.spinBox.value())))
        table.setItem(selected, 3, QTableWidgetItem(self.page.comboBox_2.currentText()))
        table.setItem(selected, 4, QTableWidgetItem(self.page.dateEdit.date().toString("yyyy-MM-dd")))
        table.setItem(selected, 5, QTableWidgetItem(self.page.lineEdit_5.text()))
        table.setItem(selected, 6, QTableWidgetItem(self.page.lineEdit_3.text()))

    # ================= DELETE =================
    def delete_selected_row(self):
        table = self.page.tableWidget
        selected = table.currentRow()
        if selected < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih baris yang akan dihapus")
            return
        table.removeRow(selected)

    # ================= SAVE =================
    def save_transaksi_to_db(self):
        # ambil data dari input form
        kode = self.page.lineEdit.text()
        id_barang = self.page.comboBox.currentData()
        jumlah = self.page.spinBox.value()
        id_supplier = self.page.comboBox_2.currentData()
        tanggal = self.page.dateEdit.date().toString("yyyy-MM-dd")
        total = self.page.lineEdit_5.text()
        keterangan = self.page.lineEdit_3.text()

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO transaksi (kode_transaksi, id_supplier, tanggal, total_harga, keterangan, type_transaksi)
                VALUES (%s, %s, %s, %s, %s, 'masuk')
            """, (kode, id_supplier, tanggal, total, keterangan))

            id_transaksi = cursor.lastrowid

            cursor.execute("""
                INSERT INTO detail_transaksi (id_transaksi, id_barang, quantity)
                VALUES (%s, %s, %s)
            """, (id_transaksi, id_barang, jumlah))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Transaksi berhasil disimpan")

            # reset form
            self.page.lineEdit.clear()
            self.page.lineEdit_5.clear()
            self.page.lineEdit_3.clear()
            self.page.spinBox.setValue(1)
            self.page.comboBox.setCurrentIndex(0)
            self.page.comboBox_2.setCurrentIndex(0)

        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal menyimpan transaksi:\n{e}")

        finally:
            cursor.close()
            conn.close()
