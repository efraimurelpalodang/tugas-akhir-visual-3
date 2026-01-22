import mysql.connector
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

class SupplierHandler:
    def __init__(self, page):
        self.page = page

        # hubungkan tombol
        self.page.tambah.clicked.connect(self.add_supplier)
        self.page.edit.clicked.connect(self.edit_supplier)
        self.page.hapus.clicked.connect(self.delete_supplier)

        # hubungkan klik table → isi form
        self.page.tableWidget.cellClicked.connect(self.fill_form_from_table)

    # ================= DB CONNECTION =================
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    # ================= LOAD TABLE =================
    def load_table(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nama_supplier, alamat, telepon, email FROM supplier ORDER BY nama_supplier ASC")
        rows = cursor.fetchall()
        table = self.page.tableWidget
        table.setRowCount(0)

        for row in rows:
            idx = table.rowCount()
            table.insertRow(idx)
            table.setItem(idx, 0, QTableWidgetItem(row["nama_supplier"]))
            table.setItem(idx, 1, QTableWidgetItem(row["alamat"]))
            table.setItem(idx, 2, QTableWidgetItem(row["telepon"]))
            table.setItem(idx, 3, QTableWidgetItem(row["email"]))

        table.setEditTriggers(table.NoEditTriggers)
        cursor.close()
        conn.close()

    # ================= CLICK TABLE → ISI FORM =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget
        self.page.nama.setText(table.item(row, 0).text())     # nama
        self.page.alamat.setText(table.item(row, 1).text())   # alamat
        self.page.telp.setText(table.item(row, 2).text())     # telepon
        self.page.email.setText(table.item(row, 3).text()) 

    # ================= ADD =================
    def add_supplier(self):
        nama = self.page.nama.text().strip()
        telp = self.page.telp.text().strip()
        email = self.page.email.text().strip()
        alamat = self.page.alamat.text().strip()

        if not nama:
            QMessageBox.warning(self.page, "Peringatan", "Nama supplier wajib diisi")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO supplier (nama_supplier, telepon, email, alamat)
                VALUES (%s, %s, %s, %s)
            """, (nama, telp, email, alamat))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Supplier berhasil ditambahkan")
            self.clear_form()
            self.load_table()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal menambahkan supplier:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # ================= EDIT =================
    def edit_supplier(self):
        table = self.page.tableWidget
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih supplier yang akan diedit")
            return

        # dapatkan id supplier dari row yang dipilih
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # ambil id dari database sesuai nama yang dipilih
            nama_lama = table.item(row, 0).text()
            cursor.execute("SELECT id FROM supplier WHERE nama_supplier=%s", (nama_lama,))
            result = cursor.fetchone()
            if not result:
                QMessageBox.warning(self.page, "Error", "Supplier tidak ditemukan")
                return

            id_supplier = result["id"]
            nama = self.page.nama.text().strip()
            telp = self.page.telp.text().strip()
            email = self.page.email.text().strip()
            alamat = self.page.alamat.text().strip()

            if not nama:
                QMessageBox.warning(self.page, "Peringatan", "Nama supplier wajib diisi")
                return

            cursor.execute("""
                UPDATE supplier
                SET nama_supplier=%s, telepon=%s, email=%s, alamat=%s
                WHERE id=%s
            """, (nama, telp, email, alamat, id_supplier))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "Supplier berhasil diupdate")
            self.clear_form()
            self.load_table()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal update supplier:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # ================= DELETE =================
    def delete_supplier(self):
        table = self.page.tableWidget
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih supplier yang akan dihapus")
            return

        reply = QMessageBox.question(
            self.page,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus supplier ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # dapatkan id supplier dari database
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            try:
                nama = table.item(row, 0).text()
                cursor.execute("SELECT id FROM supplier WHERE nama_supplier=%s", (nama,))
                result = cursor.fetchone()
                if not result:
                    QMessageBox.warning(self.page, "Error", "Supplier tidak ditemukan")
                    return
                id_supplier = result["id"]

                cursor.execute("DELETE FROM supplier WHERE id=%s", (id_supplier,))
                conn.commit()
                QMessageBox.information(self.page, "Sukses", "Supplier berhasil dihapus")
                self.clear_form()
                self.load_table()
            except mysql.connector.Error as e:
                conn.rollback()
                QMessageBox.critical(self.page, "Error", f"Gagal hapus supplier:\n{e}")
            finally:
                cursor.close()
                conn.close()

    # ================= CLEAR FORM =================
    def clear_form(self):
        self.page.nama.clear()
        self.page.telp.clear()
        self.page.email.clear()
        self.page.alamat.clear()
