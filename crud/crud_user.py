import mysql.connector
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt


class UserHandler:
    def __init__(self, page):
        self.page = page

        self.page.tambah.clicked.connect(self.add_user)
        self.page.edit.clicked.connect(self.edit_user)
        self.page.hapus.clicked.connect(self.delete_user)

        self.load_table()

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

        cursor.execute("""
            SELECT id, username, nama_lengkap, role, is_active
            FROM user
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()

        table = self.page.tableWidget
        table.setRowCount(0)
        table.setColumnCount(5)

        for row in rows:
            r = table.rowCount()
            table.insertRow(r)

            # 🔑 ID USER (hidden)
            item_id = QTableWidgetItem(str(row["id"]))
            item_id.setData(Qt.UserRole, row["id"])
            table.setItem(r, 0, item_id)

            table.setItem(r, 1, QTableWidgetItem(row["username"]))
            table.setItem(r, 2, QTableWidgetItem(row["nama_lengkap"]))
            table.setItem(r, 3, QTableWidgetItem(row["role"]))
            table.setItem(r, 4, QTableWidgetItem(str(row["is_active"])))

        table.setColumnHidden(0, True)
        table.setEditTriggers(table.NoEditTriggers)
        table.cellClicked.connect(self.fill_form_from_table)

        cursor.close()
        conn.close()

    # ================= CLICK TABLE =================
    def fill_form_from_table(self, row, column):
        table = self.page.tableWidget

        username = table.item(row, 1).text()
        self.page.username.setText(username)
        self.page.nama_lengkap.setText(table.item(row, 2).text())

        role = table.item(row, 3).text()
        idx = self.page.peran.findText(role)
        if idx >= 0:
            self.page.peran.setCurrentIndex(idx)

        # ambil password
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM user WHERE username=%s", (username,))
        data = cursor.fetchone()
        self.page.password.setText(data["password"] if data else "")
        cursor.close()
        conn.close()

    # ================= ADD =================
    def add_user(self):
        username = self.page.username.text().strip()
        password = self.page.password.text().strip()
        nama_lengkap = self.page.nama_lengkap.text().strip()
        role = self.page.peran.currentText()

        if not username or not password or not nama_lengkap:
            QMessageBox.warning(self.page, "Peringatan", "Semua field wajib diisi")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user (username, password, nama_lengkap, role, is_active)
                VALUES (%s, %s, %s, %s, 1)
            """, (username, password, nama_lengkap, role))
            conn.commit()
            QMessageBox.information(self.page, "Sukses", "User berhasil ditambahkan")
            self.clear_form()
            self.load_table()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", str(e))
        finally:
            cursor.close()
            conn.close()

    # ================= EDIT =================
    def edit_user(self):
        table = self.page.tableWidget
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih user dulu")
            return

        user_id = int(table.item(row, 0).text())

        username = self.page.username.text().strip()
        password = self.page.password.text().strip()
        nama_lengkap = self.page.nama_lengkap.text().strip()
        role = self.page.peran.currentText()

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if password:
                cursor.execute("""
                    UPDATE user
                    SET username=%s, password=%s, nama_lengkap=%s, role=%s
                    WHERE id=%s
                """, (username, password, nama_lengkap, role, user_id))
            else:
                cursor.execute("""
                    UPDATE user
                    SET username=%s, nama_lengkap=%s, role=%s
                    WHERE id=%s
                """, (username, nama_lengkap, role, user_id))

            conn.commit()
            QMessageBox.information(self.page, "Sukses", "User berhasil diupdate")
            self.clear_form()
            self.load_table()
        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self.page, "Error", str(e))
        finally:
            cursor.close()
            conn.close()

    # ================= DELETE =================
    def delete_user(self):
        table = self.page.tableWidget
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Peringatan", "Pilih user dulu")
            return

        user_id = int(table.item(row, 0).text())

        if QMessageBox.question(
            self.page,
            "Konfirmasi",
            "Yakin ingin menghapus user ini?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:

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
                QMessageBox.critical(self.page, "Error", str(e))
            finally:
                cursor.close()
                conn.close()

    # ================= CLEAR =================
    def clear_form(self):
        self.page.username.clear()
        self.page.password.clear()
        self.page.nama_lengkap.clear()
        self.page.peran.setCurrentIndex(0)
