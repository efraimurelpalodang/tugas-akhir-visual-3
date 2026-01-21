import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

class BarangHandler:
    def __init__(self, page):
        self.page = page

        # Hubungkan tombol
        self.page.tambah.clicked.connect(self.add_barang)
        self.page.edit.clicked.connect(self.edit_selected_barang)
        self.page.hapus.clicked.connect(self.delete_selected_barang)

        # Load combobox kategori & satuan
        self.load_combobox_data()
        # Load tabel barang
        self.load_table_barang()

        # Klik row isi form
        self.page.tableWidget.cellClicked.connect(self.fill_form_from_table)

    # ================= DB CONNECTION =================
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    # ================= LOAD COMBOBOX =================
    def load_combobox_data(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Kategori
        cursor.execute("SELECT id, nama_kategori FROM kategori ORDER BY nama_kategori ASC")
        kategori_list = cursor.fetchall()
        self.page.comboBox.clear()
        for kat in kategori_list:
            self.page.comboBox.addItem(kat["nama_kategori"], kat["id"])

        # Satuan
        cursor.execute("SELECT id, nama_satuan FROM satuan ORDER BY nama_satuan ASC")
        satuan_list = cursor.fetchall()
        self.page.comboBox_2.clear()
        for s in satuan_list:
            self.page.comboBox_2.addItem(s["nama_satuan"], s["id"])

        cursor.close()
        conn.close()

    # ================= LOAD TABEL =================
    def load_table_barang(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT b.id, b.nama_barang, k.nama_kategori, s.nama_satuan,
                    b.harga_beli, b.harga_jual, b.stok_minimum, b.stok
            FROM barang b
            LEFT JOIN kategori k ON b.id_kategori = k.id
            LEFT JOIN satuan s ON b.id_satuan = s.id
            ORDER BY b.nama_barang ASC
        """)
        rows = cursor.fetchall()
        table = self.page.tableWidget
        table.setRowCount(0)

        for row in rows:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            table.setItem(row_pos, 0, QTableWidgetItem(row["nama_barang"]))
            table.setItem(row_pos, 1, QTableWidgetItem(row["nama_kategori"] if row["nama_kategori"] else ""))
            table.setItem(row_pos, 2, QTableWidgetItem(row["nama_satuan"] if row["nama_satuan"] else ""))
            table.setItem(row_pos, 3, QTableWidgetItem(str(row["harga_beli"])))
            table.setItem(row_pos, 4, QTableWidgetItem(str(row["harga_jual"])))
            table.setItem(row_pos, 5, QTableWidgetItem(str(row["stok_minimum"])))
            table.setItem(row_pos, 6, QTableWidgetItem(str(row["stok"])))
            table.item(row_pos, 0).setData(Qt.UserRole, row["id"])  # simpan id barang di kolom pertama

        table.setEditTriggers(table.NoEditTriggers)

    # ================= FILL FORM =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget
        self.page.lineEdit.setText(table.item(row, 0).text())

        # pilih kategori
        nama_kategori = table.item(row, 1).text()
        idx_kat = self.page.comboBox.findText(nama_kategori)
        if idx_kat >= 0:
            self.page.comboBox.setCurrentIndex(idx_kat)

        # pilih satuan
        nama_satuan = table.item(row, 2).text()
        idx_satuan = self.page.comboBox_2.findText(nama_satuan)
        if idx_satuan >= 0:
            self.page.comboBox_2.setCurrentIndex(idx_satuan)

        self.page.lineEdit_2.setText(table.item(row, 3).text())
        self.page.lineEdit_3.setText(table.item(row, 4).text())
        self.page.spinBox.setValue(int(table.item(row, 5).text()))
        self.page.spinBox_2.setValue(int(table.item(row, 6).text()))

    # ================= ADD =================
    def add_barang(self):
        nama = self.page.lineEdit.text()
        id_kategori = self.page.comboBox.currentData()
        id_satuan = self.page.comboBox_2.currentData()
        harga_beli = self.page.lineEdit_2.text()
        harga_jual = self.page.lineEdit_3.text()
        stok_min = self.page.spinBox.value()
        stok = self.page.spinBox_2.value()

        if not nama:
            QMessageBox.warning(self.page, "Peringatan", "Nama barang tidak boleh kosong")
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO barang (nama_barang, id_kategori, id_satuan, harga_beli, harga_jual, stok_minimum, stok)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nama, id_kategori, id_satuan, harga_beli, harga_jual, stok_min, stok))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Barang berhasil ditambahkan")
            self.load_table_barang()
            self.reset_form()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal menambahkan barang:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # ================= EDIT =================
    def edit_selected_barang(self):
        table = self.page.tableWidget
        selected = table.currentRow()
        if selected < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih barang yang akan diedit")
            return

        id_barang = table.item(selected, 0).data(Qt.UserRole)
        nama = self.page.lineEdit.text()
        id_kategori = self.page.comboBox.currentData()
        id_satuan = self.page.comboBox_2.currentData()
        harga_beli = self.page.lineEdit_2.text()
        harga_jual = self.page.lineEdit_3.text()
        stok_min = self.page.spinBox.value()
        stok = self.page.spinBox_2.value()

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE barang
                SET nama_barang=%s, id_kategori=%s, id_satuan=%s, harga_beli=%s, harga_jual=%s, stok_minimum=%s, stok=%s
                WHERE id=%s
            """, (nama, id_kategori, id_satuan, harga_beli, harga_jual, stok_min, stok, id_barang))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Barang berhasil diupdate")
            self.load_table_barang()
            self.reset_form()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal mengupdate barang:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # ================= DELETE =================
    def delete_selected_barang(self):
        table = self.page.tableWidget
        selected = table.currentRow()
        if selected < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih barang yang akan dihapus")
            return

        id_barang = table.item(selected, 0).data(Qt.UserRole)

        reply = QMessageBox.question(
            self.page,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus barang ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM barang WHERE id=%s", (id_barang,))
                conn.commit()
                QMessageBox.information(self.page, "Sukses", "Barang berhasil dihapus")
                self.load_table_barang()
                self.reset_form()
            except mysql.connector.Error as e:
                conn.rollback()
                QMessageBox.critical(self.page, "Error", f"Gagal menghapus barang:\n{e}")
            finally:
                cursor.close()
                conn.close()

    # ================= RESET FORM =================
    def reset_form(self):
        self.page.lineEdit.clear()
        self.page.lineEdit_2.clear()
        self.page.lineEdit_3.clear()
        self.page.spinBox.setValue(0)
        self.page.spinBox_2.setValue(0)
        self.page.comboBox.setCurrentIndex(0)
        self.page.comboBox_2.setCurrentIndex(0)
