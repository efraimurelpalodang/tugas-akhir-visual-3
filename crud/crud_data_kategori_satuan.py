import mysql.connector
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt

class KategoriSatuanHandler:
    def __init__(self, page):
        self.page = page

        # ===== KATEGORI =====
        self.page.tambah_kategori.clicked.connect(self.add_kategori)
        self.page.edit_kategori.clicked.connect(self.edit_kategori)
        self.page.hapus_kategori.clicked.connect(self.delete_kategori)
        self.page.tableWidget_kategori.cellClicked.connect(self.fill_lineEdit_kategori)

        # ===== SATUAN =====
        self.page.tambah_satuan.clicked.connect(self.add_satuan)
        self.page.edit_satuan.clicked.connect(self.edit_satuan)
        self.page.hapus_satuan.clicked.connect(self.delete_satuan)
        self.page.tableWidget_satuan.cellClicked.connect(self.fill_lineEdit_satuan)

    # ================= DB CONNECTION =================
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    # =================== LOAD TABLE ===================
    def load_table_kategori(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nama_kategori FROM kategori ORDER BY nama_kategori ASC")
        rows = cursor.fetchall()
        table = self.page.tableWidget_kategori
        table.setRowCount(0)

        for row in rows:
            idx = table.rowCount()
            table.insertRow(idx)
            item = QTableWidgetItem(row["nama_kategori"])
            item.setData(Qt.UserRole, row["id"])  # simpan id tersembunyi
            table.setItem(idx, 0, item)

        table.setEditTriggers(table.NoEditTriggers)
        cursor.close()
        conn.close()

    def load_table_satuan(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nama_satuan FROM satuan ORDER BY nama_satuan ASC")
        rows = cursor.fetchall()
        table = self.page.tableWidget_satuan
        table.setRowCount(0)

        for row in rows:
            idx = table.rowCount()
            table.insertRow(idx)
            item = QTableWidgetItem(row["nama_satuan"])
            item.setData(Qt.UserRole, row["id"])  # simpan id tersembunyi
            table.setItem(idx, 0, item)

        table.setEditTriggers(table.NoEditTriggers)
        cursor.close()
        conn.close()

    # =================== CLICK TABLE → FILL LINEEDIT ===================
    def fill_lineEdit_kategori(self, row, column):
        table = self.page.tableWidget_kategori
        self.page.lineEdit_kategori.setText(table.item(row, 0).text())

    def fill_lineEdit_satuan(self, row, column):
        table = self.page.tableWidget_satuan
        self.page.lineEdit_satuan.setText(table.item(row, 0).text())

    # =================== ADD ===================
    def add_kategori(self):
        nama = self.page.lineEdit_kategori.text().strip()
        if not nama:
            QMessageBox.warning(self.page, "Peringatan", "Nama kategori wajib diisi")
            return
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO kategori (nama_kategori) VALUES (%s)", (nama,))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Kategori berhasil ditambahkan")
            self.page.lineEdit_kategori.clear()
            self.load_table_kategori()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal menambahkan kategori:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def add_satuan(self):
        nama = self.page.lineEdit_satuan.text().strip()
        if not nama:
            QMessageBox.warning(self.page, "Peringatan", "Nama satuan wajib diisi")
            return
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO satuan (nama_satuan) VALUES (%s)", (nama,))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Satuan berhasil ditambahkan")
            self.page.lineEdit_satuan.clear()
            self.load_table_satuan()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal menambahkan satuan:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # =================== EDIT ===================
    def edit_kategori(self):
        table = self.page.tableWidget_kategori
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih kategori yang akan diedit")
            return
        id_kategori = table.item(row, 0).data(Qt.UserRole)
        nama = self.page.lineEdit_kategori.text().strip()
        if not nama:
            QMessageBox.warning(self.page, "Peringatan", "Nama kategori wajib diisi")
            return
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE kategori SET nama_kategori=%s WHERE id=%s", (nama, id_kategori))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Kategori berhasil diupdate")
            self.page.lineEdit_kategori.clear()
            self.load_table_kategori()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal update kategori:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def edit_satuan(self):
        table = self.page.tableWidget_satuan
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih satuan yang akan diedit")
            return
        id_satuan = table.item(row, 0).data(Qt.UserRole)
        nama = self.page.lineEdit_satuan.text().strip()
        if not nama:
            QMessageBox.warning(self.page, "Peringatan", "Nama satuan wajib diisi")
            return
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE satuan SET nama_satuan=%s WHERE id=%s", (nama, id_satuan))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Satuan berhasil diupdate")
            self.page.lineEdit_satuan.clear()
            self.load_table_satuan()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal update satuan:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # =================== DELETE ===================
    def delete_kategori(self):
        table = self.page.tableWidget_kategori
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih kategori yang akan dihapus")
            return
        reply = QMessageBox.question(
            self.page,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus kategori ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            id_kategori = table.item(row, 0).data(Qt.UserRole)
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM kategori WHERE id=%s", (id_kategori,))
                conn.commit()
                QMessageBox.information(self.page, "Sukses", "Kategori berhasil dihapus")
                self.load_table_kategori()
            except mysql.connector.Error as e:
                conn.rollback()
                QMessageBox.critical(self.page, "Error", f"Gagal hapus kategori:\n{e}")
            finally:
                cursor.close()
                conn.close()

    def delete_satuan(self):
        table = self.page.tableWidget_satuan
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih satuan yang akan dihapus")
            return
        reply = QMessageBox.question(
            self.page,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus satuan ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            id_satuan = table.item(row, 0).data(Qt.UserRole)
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM satuan WHERE id=%s", (id_satuan,))
                conn.commit()
                QMessageBox.information(self.page, "Sukses", "Satuan berhasil dihapus")
                self.load_table_satuan()
            except mysql.connector.Error as e:
                conn.rollback()
                QMessageBox.critical(self.page, "Error", f"Gagal hapus satuan:\n{e}")
            finally:
                cursor.close()
                conn.close()
