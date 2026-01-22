from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QMessageBox
import mysql.connector

class ReportHandler:
    def __init__(self, page):
        self.page = page
        self.report_windows = []
        self.setup_buttons()

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    def setup_buttons(self):
      if hasattr(self.page, "btn_report_users"):
          self.page.btn_report_users.clicked.connect(self.report_all_users)

      if hasattr(self.page, "btn_report_barang"):
          self.page.btn_report_barang.clicked.connect(self.report_all_barang)

      if hasattr(self.page, "btn_report_barang_masuk"):
          self.page.btn_report_barang_masuk.clicked.connect(self.report_barang_masuk)

      if hasattr(self.page, "btn_report_barang_keluar"):
          self.page.btn_report_barang_keluar.clicked.connect(self.report_barang_keluar)

      if hasattr(self.page, "btn_report_stok_min"):
          self.page.btn_report_stok_min.clicked.connect(self.report_stok_min)

      if hasattr(self.page, "btn_report_transaksi"):
          self.page.btn_report_transaksi.clicked.connect(self.report_transaksi_keseluruhan)

      if hasattr(self.page, "btn_report_aktivitas_user"):
          self.page.btn_report_aktivitas_user.clicked.connect(self.report_aktivitas_user)

    # ====================== Fungsi report umum ======================
    def show_report(self, title, headers, rows):
      window = QMainWindow(self.page)  # ⬅️ kasih parent
      window.setWindowTitle(title)

      table = QTableWidget()
      table.setColumnCount(len(headers))
      table.setHorizontalHeaderLabels(headers)
      table.setRowCount(len(rows))

      for i, row in enumerate(rows):
          for j, value in enumerate(row):
              table.setItem(i, j, QTableWidgetItem(str(value)))

      table.resizeColumnsToContents()
      table.setEditTriggers(QTableWidget.NoEditTriggers)

      table.setStyleSheet("""
        QTableWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            gridline-color: #444444;
            font-size: 12px;
        }

        QHeaderView::section {
            background-color: #2b2b2b;
            color: #ffffff;
            padding: 6px;
            border: 1px solid #444444;
            font-weight: bold;
        }

        QTableWidget::item {
            padding: 4px;
        }

        QTableWidget::item:selected {
            background-color: #3d7848;
            color: white;
        }
    """)

      container = QWidget()
      layout = QVBoxLayout(container)
      layout.addWidget(table)

      window.setCentralWidget(container)
      window.resize(900, 450)

      window.show()
      self.report_windows.append(window)

    # ====================== 1. Semua User ======================
    def report_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, nama_lengkap, role, is_active FROM user ORDER BY username ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        headers = ["Username", "Nama Lengkap", "Role", "Status Aktif"]
        self.show_report("Laporan Semua User", headers, rows)

    # ====================== 2. Semua Barang ======================
    def report_all_barang(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT kode_barang, nama_barang, kategori, stok, harga FROM barang ORDER BY nama_barang ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        headers = ["Kode Barang", "Nama Barang", "Kategori", "Stok", "Harga"]
        self.show_report("Laporan Semua Barang", headers, rows)

    # ====================== 3. Barang Masuk ======================
    def report_barang_masuk(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tanggal, kode_barang, jumlah, username FROM barang_masuk ORDER BY tanggal DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        headers = ["Tanggal", "Kode Barang", "Jumlah", "User"]
        self.show_report("Laporan Barang Masuk", headers, rows)

    # ====================== 4. Barang Keluar ======================
    def report_barang_keluar(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tanggal, kode_barang, jumlah, tujuan, username FROM barang_keluar ORDER BY tanggal DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        headers = ["Tanggal", "Kode Barang", "Jumlah", "Tujuan", "User"]
        self.show_report("Laporan Barang Keluar", headers, rows)

    # ====================== 5. Stok Minimum ======================
    def report_stok_min(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT kode_barang, nama_barang, kategori, stok FROM barang WHERE stok <= 5 ORDER BY stok ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        headers = ["Kode Barang", "Nama Barang", "Kategori", "Stok"]
        self.show_report("Laporan Stok Minimum", headers, rows)

    # ====================== Laporan Keseluruhan Transaksi ======================
    def report_transaksi_keseluruhan(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Ambil barang masuk
        cursor.execute("""
            SELECT 'Masuk' AS tipe, tanggal, kode_barang, jumlah, username, NULL AS tujuan
            FROM barang_masuk
        """)
        masuk = cursor.fetchall()

        # Ambil barang keluar
        cursor.execute("""
            SELECT 'Keluar' AS tipe, tanggal, kode_barang, jumlah, username, tujuan
            FROM barang_keluar
        """)
        keluar = cursor.fetchall()

        # Gabungkan
        rows = masuk + keluar
        rows.sort(key=lambda x: x[1], reverse=True)  # urut berdasarkan tanggal DESC

        cursor.close()
        conn.close()

        headers = ["Tipe", "Tanggal", "Kode Barang", "Jumlah", "User", "Tujuan"]
        self.show_report("Laporan Keseluruhan Transaksi", headers, rows)

    # ====================== 7. Aktivitas User ======================
    def report_aktivitas_user(self):
      conn = self.get_connection()
      cursor = conn.cursor()

      cursor.execute("""
          SELECT
              u.username,
              l.aktivitas,
              l.keterangan,
              l.tabel_terkait,
              l.created_at
          FROM log_aktivitas l
          JOIN user u ON l.id_user = u.id
          ORDER BY l.created_at DESC
      """)

      rows = cursor.fetchall()
      cursor.close()
      conn.close()

      headers = [
          "Username",
          "Aktivitas",
          "Keterangan",
          "Tabel",
          "Waktu"
      ]

      self.show_report("Laporan Aktivitas User", headers, rows)
