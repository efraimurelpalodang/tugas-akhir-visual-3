import os
import sys
import mysql.connector
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QTableWidgetItem, QMessageBox
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "crud"))
from crud_transaksi_masuk import TransaksiMasukHandler
from crud_transaksi_keluar import TransaksiKeluarHandler
from crud_data_barang import BarangHandler
from crud_data_kategori_satuan import KategoriSatuanHandler
from crud_data_supplier import SupplierHandler
from laporan_transaksi import LaporanTransaksiHandler

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

        # ================= BUTTON SIDEBAR =================
        self.pushButton.clicked.connect(self.load_page_dashboard)            # Dashboard
        self.pushButton_6.clicked.connect(self.load_page_transaksi_masuk)    # Transaksi Barang Masuk
        self.pushButton_7.clicked.connect(self.load_page_transaksi_keluar)   # Transaksi Barang Keluar
        self.pushButton_2.clicked.connect(self.load_page_data_barang)        # Data Barang
        self.pushButton_3.clicked.connect(self.load_page_data_kategori_satuan)  # Data Kategori & satuan
        self.pushButton_5.clicked.connect(self.load_page_data_supplier)      # Data Supplier
        self.pushButton_8.clicked.connect(self.load_page_laporan_transaksi)  # Laporan Transaksi
        self.pushButton_9.clicked.connect(self.load_page_laporan_stok)       # Laporan Stok
        self.pushButton_10.clicked.connect(self.load_page_management_user)   # Management User

        self.load_page_dashboard()

    def clear_content(self):
        while self.contentLayout.count():
            item = self.contentLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # ================= HALAMAN DASHBOARD =================
    def load_page_dashboard(self):
        self.clear_content()
        page = uic.loadUi(os.path.join(UI_DIR, "pages", "page_dashboard.ui"))
        self.contentLayout.addWidget(page)
        # load tabel aktivitas juga
        self.load_table()

    # ================= HALAMAN TRANSAKSI BARANG MASUK =================
    def load_page_transaksi_masuk(self):
        self.clear_content()
        self.page_trm = uic.loadUi(os.path.join(UI_DIR, "pages", "page_transaksi_barang_masuk.ui"))
        self.contentLayout.addWidget(self.page_trm)

        # panggil class handler
        self.trm_handler = TransaksiMasukHandler(self.page_trm, self.user)
        self.trm_handler.load_combobox_data()
        self.trm_handler.load_transaksi_masuk_table()

    # ================= HALAMAN TRANSAKSI BARANG KELUAR =================
    def load_page_transaksi_keluar(self):
        self.clear_content()
        self.page_trm = uic.loadUi(os.path.join(UI_DIR, "pages", "page_transaksi_barang_keluar.ui"))
        self.contentLayout.addWidget(self.page_trm)

        # panggil class handler
        self.trm_handler = TransaksiKeluarHandler(self.page_trm, self.user)
        self.trm_handler.load_combobox_data()
        self.trm_handler.load_transaksi_keluar_table()

    # ================= HALAMAN DATA BARANG =================
    def load_page_data_barang(self):
        self.clear_content()
        self.page_trm = uic.loadUi(os.path.join(UI_DIR, "pages", "page_data_barang.ui"))
        self.contentLayout.addWidget(self.page_trm)

        # panggil class handler
        self.trm_handler = BarangHandler(self.page_trm)
        self.trm_handler.load_combobox_data()
        self.trm_handler.load_table_barang()

    # ================= HALAMAN DATA KATEGORI & SATUAN =================
    def load_page_data_kategori_satuan(self):
        self.clear_content()
        self.page_trm = uic.loadUi(os.path.join(UI_DIR, "pages", "page_data_kategori_satuan.ui"))
        self.contentLayout.addWidget(self.page_trm)

        self.handler = KategoriSatuanHandler(self.page_trm)
        self.handler.load_table_kategori()
        self.handler.load_table_satuan()

    # ================= HALAMAN DATA SUPPLIER =================
    def load_page_data_supplier(self):
        self.clear_content()
        self.page_trm = uic.loadUi(os.path.join(UI_DIR, "pages", "page_data_supplier.ui"))
        self.contentLayout.addWidget(self.page_trm)

        self.handler = SupplierHandler(self.page_trm)
        self.handler.load_table()

    # ================= HALAMAN LAPORAN TRANSAKSI =================
    def load_page_laporan_transaksi(self):
        self.clear_content()
        self.page_laporan = uic.loadUi(os.path.join(UI_DIR, "pages", "page_laporan_transaksi.ui"))
        self.contentLayout.addWidget(self.page_laporan)

        self.laporan_handler = LaporanTransaksiHandler(self.page_laporan)
        self.laporan_handler.load_table()

    # ================= HALAMAN LAPORAN STOK =================
    def load_page_laporan_stok(self):
        self.clear_content()
        page = uic.loadUi(os.path.join(UI_DIR, "pages", "page_laporan_stok.ui"))
        self.contentLayout.addWidget(page)

    # ================= HALAMAN MANAGEMENT USER =================
    def load_page_management_user(self):
        self.clear_content()
        page = uic.loadUi(os.path.join(UI_DIR, "pages", "page_management_user.ui"))
        self.contentLayout.addWidget(page)

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
        table.setEditTriggers(table.NoEditTriggers)
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
