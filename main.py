import os
import sys
import mysql.connector
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QTableWidgetItem, QMessageBox
)

# ================= PATH DASAR =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")


# ================= LOGIN =================
class Login(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(
            os.path.join(UI_DIR, "layouts", "login.ui"),
            self
        )

        self.btnLogin.clicked.connect(self.login_process)

    def login_process(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username dan password wajib diisi")
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nama_lengkap
            FROM user
            WHERE username=%s AND password=%s
        """, (username, password))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            self.dashboard = Dashboard(user)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login gagal", "Username atau password salah")


# ================= DASHBOARD =================
class Dashboard(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user

        uic.loadUi(
            os.path.join(UI_DIR, "layouts", "dashboard.ui"),
            self
        )

        # tampilkan nama user
        if hasattr(self, "labelUser"):
            self.labelUser.setText(self.user["nama_lengkap"])

        # ✅ layout utama di dashboard.ui
        self.contentLayout = self.frameContent.layout()

        self.load_page_dashboard()

    def clear_content(self):
        while self.contentLayout.count():
            item = self.contentLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_page_dashboard(self):
        self.clear_content()

        # load page dashboard
        self.page_dashboard = uic.loadUi(
            os.path.join(UI_DIR, "pages", "page_dashboard.ui")
        )

        # ✅ page masuk ke frameContent
        self.contentLayout.addWidget(self.page_dashboard)

        self.load_table()

    def load_table(self):
        self.table_ui = uic.loadUi(
            os.path.join(UI_DIR, "components", "table_aktivitas.ui")
        )

        # ✅ MASUKKAN TABLE KE frameContent JUGA
        self.contentLayout.addWidget(self.table_ui)

        self.load_data_mysql()

    def load_data_mysql(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                u.nama_lengkap,
                l.aktivitas,
                l.keterangan,
                l.tabel_terkait
            FROM log_aktivitas l
            JOIN user u ON l.id_user = u.id
            ORDER BY l.created_at DESC
        """)

        rows = cursor.fetchall()

        table = self.table_ui.tableWidget
        table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(str(value)))

        cursor.close()
        conn.close()



# ================= RUN APP =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
