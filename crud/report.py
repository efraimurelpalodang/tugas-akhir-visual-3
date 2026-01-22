import os
from datetime import datetime
import mysql.connector
from PyQt5.QtWidgets import QMessageBox


class ReportHandler:
    def __init__(self, page):
        self.page = page
        self.setup_buttons()

    # ====================== KONEKSI DB ======================
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    # ====================== CONNECT BUTTON ======================
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

    # ====================== EXPORT HTML (EXCEL) ======================
    def export_to_excel_html(self, title, headers, rows):
        folder = os.path.join(os.getcwd(), "exports")
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.replace(' ', '_')}_{timestamp}.xls"
        filepath = os.path.join(folder, filename)

        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th {{
                    background-color: #2f3542;
                    color: white;
                    padding: 8px;
                    border: 1px solid #555;
                    text-align: center;
                }}
                td {{
                    padding: 6px;
                    border: 1px solid #999;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                h2 {{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <h2>{title}</h2>
            <table>
                <thead>
                    <tr>
        """

        for h in headers:
            html += f"<th>{h}</th>"

        html += "</tr></thead><tbody>"

        for row in rows:
            html += "<tr>"
            for col in row:
                html += f"<td>{col}</td>"
            html += "</tr>"

        html += """
                </tbody>
            </table>
        </body>
        </html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        QMessageBox.information(
            self.page,
            "Export Berhasil",
            f"Laporan berhasil diexport ke Excel:\n{filepath}"
        )

    # ====================== 1. LAPORAN USER ======================
    def report_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, nama_lengkap, role, is_active
            FROM user
            ORDER BY username ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ["Username", "Nama Lengkap", "Role", "Status Aktif"]
        self.export_to_excel_html("Laporan Semua User", headers, rows)

    # ====================== 2. LAPORAN BARANG ======================
    def report_all_barang(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT kode_barang, nama_barang, kategori, stok, harga
            FROM barang
            ORDER BY nama_barang ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ["Kode Barang", "Nama Barang", "Kategori", "Stok", "Harga"]
        self.export_to_excel_html("Laporan Semua Barang", headers, rows)

    # ====================== 3. BARANG MASUK ======================
    def report_barang_masuk(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tanggal, kode_barang, jumlah, username
            FROM barang_masuk
            ORDER BY tanggal DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ["Tanggal", "Kode Barang", "Jumlah", "User"]
        self.export_to_excel_html("Laporan Barang Masuk", headers, rows)

    # ====================== 4. BARANG KELUAR ======================
    def report_barang_keluar(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tanggal, kode_barang, jumlah, tujuan, username
            FROM barang_keluar
            ORDER BY tanggal DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ["Tanggal", "Kode Barang", "Jumlah", "Tujuan", "User"]
        self.export_to_excel_html("Laporan Barang Keluar", headers, rows)

    # ====================== 5. STOK MINIMUM ======================
    def report_stok_min(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT kode_barang, nama_barang, kategori, stok
            FROM barang
            WHERE stok <= 5
            ORDER BY stok ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ["Kode Barang", "Nama Barang", "Kategori", "Stok"]
        self.export_to_excel_html("Laporan Stok Minimum", headers, rows)

    # ====================== 6. TRANSAKSI KESELURUHAN ======================
    def report_transaksi_keseluruhan(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 'Masuk', tanggal, kode_barang, jumlah, username, ''
            FROM barang_masuk
        """)
        masuk = cursor.fetchall()

        cursor.execute("""
            SELECT 'Keluar', tanggal, kode_barang, jumlah, username, tujuan
            FROM barang_keluar
        """)
        keluar = cursor.fetchall()

        rows = masuk + keluar
        rows.sort(key=lambda x: x[1], reverse=True)

        cursor.close()
        conn.close()

        headers = ["Tipe", "Tanggal", "Kode Barang", "Jumlah", "User", "Tujuan"]
        self.export_to_excel_html("Laporan Transaksi Keseluruhan", headers, rows)

    # ====================== 7. AKTIVITAS USER ======================
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

        headers = ["Username", "Aktivitas", "Keterangan", "Tabel", "Waktu"]
        self.export_to_excel_html("Laporan Aktivitas User", headers, rows)
