import mysql.connector
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

class UserHandler:
    def __init__(self, page):
        self.page = page

        # Hubungkan tombol
        self.page.tambah.clicked.connect(self.add_user)
        self.page.edit.clicked.connect(self.edit_user)
        self.page.hapus.clicked.connect(self.delete_user)

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
        cursor.execute("SELECT username, nama_lengkap, role, is_active FROM user ORDER BY id ASC")
        rows = cursor.fetchall()
        table = self.page.tableWidget
        table.setRowCount(0)

        for row in rows:
            idx = table.rowCount()
            table.insertRow(idx)
            table.setItem(idx, 0, QTableWidgetItem(row["username"]))
            table.setItem(idx, 1, QTableWidgetItem(row["nama_lengkap"]))
            table.setItem(idx, 2, QTableWidgetItem(row["role"]))
            table.setItem(idx, 3, QTableWidgetItem(str(row["is_active"])))

        table.setEditTriggers(table.NoEditTriggers)
        cursor.close()
        conn.close()

        # Hubungkan klik tabel → isi form
        table.cellClicked.connect(self.fill_form_from_table)

    # ================= CLICK TABLE → ISI FORM =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget
        username = table.item(row, 0).text()
        self.page.username.setText(username)
        self.page.nama_lengkap.setText(table.item(row, 1).text())
        
        role = table.item(row, 2).text()
        index_role = self.page.peran.findText(role)
        if index_role >= 0:
            self.page.peran.setCurrentIndex(index_role)

        # Ambil password dari DB
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM user WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result:
            self.page.password.setText(result["password"])
        else:
            self.page.password.clear()
        cursor.close()
        conn.close()


    # ================= ADD =================
    def add_user(self):
        username = self.page.username.text().strip()
        password = self.page.password.text().strip()
        nama_lengkap = self.page.nama_lengkap.text().strip()
        role = self.page.peran.currentText()
        is_active = 1  # set default aktif

        if not username or not password or not nama_lengkap:
            QMessageBox.warning(self.page, "Peringatan", "Semua field wajib diisi")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user (username, password, nama_lengkap, role, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, nama_lengkap, role, is_active))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "User berhasil ditambahkan")
            self.clear_form()
            self.load_table()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal menambahkan user:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # ================= EDIT =================
    def edit_user(self):
        table = self.page.tableWidget
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih user yang akan diedit")
            return

        old_username = table.item(row, 0).text()  # username lama
        username = self.page.username.text().strip()
        password = self.page.password.text().strip()
        nama_lengkap = self.page.nama_lengkap.text().strip()
        role = self.page.peran.currentText()

        if not username or not nama_lengkap:
            QMessageBox.warning(self.page, "Peringatan", "Username dan Nama Lengkap wajib diisi")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Jika password diisi, update password juga
            if password:
                cursor.execute("""
                    UPDATE user
                    SET username=%s, password=%s, nama_lengkap=%s, role=%s
                    WHERE username=%s
                """, (username, password, nama_lengkap, role, old_username))
            else:
                # Password kosong → jangan update password
                cursor.execute("""
                    UPDATE user
                    SET username=%s, nama_lengkap=%s, role=%s
                    WHERE username=%s
                """, (username, nama_lengkap, role, old_username))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "User berhasil diupdate")
            self.clear_form()
            self.load_table()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", f"Gagal update user:\n{e}")
        finally:
            cursor.close()
            conn.close()

    # ================= DELETE =================
    def delete_user(self):
        table = self.page.tableWidget
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih user yang akan dihapus")
            return

        reply = QMessageBox.question(
            self.page,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus user ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            user_id = int(table.item(row, 0).text())
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM user WHERE id=%s", (user_id,))
                conn.commit()
                QMessageBox.information(self.page, "Sukses", "User berhasil dihapus")
                self.clear_form()
                self.load_table()
            except mysql.connector.Error as e:
                conn.rollback()
                QMessageBox.critical(self.page, "Error", f"Gagal hapus user:\n{e}")
            finally:
                cursor.close()
                conn.close()

    # ================= CLEAR FORM =================
    def clear_form(self):
        self.page.username.clear()
        self.page.password.clear()
        self.page.nama_lengkap.clear()
        self.page.peran.setCurrentIndex(0)
