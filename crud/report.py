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
        """Menghubungkan tombol laporan yang ada di halaman"""
        try:
            # Cari semua atribut yang merupakan tombol
            for attr_name in dir(self.page):
                if not attr_name.startswith('_') and hasattr(getattr(self.page, attr_name), 'clicked'):
                    btn = getattr(self.page, attr_name)
                    
                    # Cek jika ini tombol laporan berdasarkan nama
                    attr_lower = attr_name.lower()
                    
                    if 'user' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()  # Hapus koneksi lama
                        except:
                            pass
                        btn.clicked.connect(self.report_all_users)
                        print(f"✅ Tombol {attr_name} -> Laporan User")
                        
                    elif 'barang' in attr_lower and 'masuk' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_barang_masuk)
                        print(f"✅ Tombol {attr_name} -> Laporan Barang Masuk")
                        
                    elif 'barang' in attr_lower and 'keluar' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_barang_keluar)
                        print(f"✅ Tombol {attr_name} -> Laporan Barang Keluar")
                        
                    elif 'stok' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_stok_min)
                        print(f"✅ Tombol {attr_name} -> Laporan Stok")
                        
                    elif 'transaksi' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_transaksi_keseluruhan)
                        print(f"✅ Tombol {attr_name} -> Laporan Transaksi")
                        
                    elif 'aktivitas' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_aktivitas_user)
                        print(f"✅ Tombol {attr_name} -> Laporan Aktivitas")
                        
                    elif 'barang' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_all_barang)
                        print(f"✅ Tombol {attr_name} -> Laporan Barang")
                        
        except Exception as e:
            print(f"Error setting up report buttons: {e}")

    # ====================== EXPORT EXCEL ======================
    def export_to_excel_html(self, title, headers, rows):
        if not rows:
            QMessageBox.warning(
                self.page,
                "Data Kosong",
                "Tidak ada data untuk dicetak"
            )
            return

        folder = os.path.join(os.getcwd(), "exports")
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.replace(' ', '_')}_{timestamp}.xls"
        filepath = os.path.join(folder, filename)

        # Buat file HTML sederhana
        html_content = f"""
        <html>
        <head>
            <title>{title}</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h2 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th {{ background-color: #4CAF50; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 8px; border: 1px solid #ddd; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>{title}</h2>
            <p>Tanggal Cetak: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>
            <p>Jumlah Data: {len(rows)}</p>
            <table border="1">
                <tr>
        """
        
        # Header
        for h in headers:
            html_content += f"<th>{h}</th>"
        html_content += "</tr>"
        
        # Data
        for row in rows:
            html_content += "<tr>"
            for col in row:
                if col is None:
                    col = ""
                html_content += f"<td>{col}</td>"
            html_content += "</tr>"
        
        html_content += """
            </table>
        </body>
        </html>
        """

        # Simpan file
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Pesan sukses
            QMessageBox.information(
                self.page,
                "Export Berhasil",
                f"Laporan berhasil disimpan di:\n{filepath}"
            )
            
            # Coba buka file
            try:
                os.startfile(filepath)  # Windows
            except:
                try:
                    os.system(f'xdg-open "{filepath}"')  # Linux
                except:
                    try:
                        os.system(f'open "{filepath}"')  # Mac
                    except:
                        pass
                        
        except Exception as e:
            QMessageBox.critical(
                self.page,
                "Export Gagal",
                f"Gagal menyimpan file:\n{str(e)}"
            )

    # ====================== 1. USER ======================
    def report_all_users(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, nama_lengkap, role, 
                       CASE WHEN is_active = 1 THEN 'Aktif' ELSE 'Non-Aktif' END as status
                FROM user
                ORDER BY username
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Username", "Nama Lengkap", "Role", "Status"]
            self.export_to_excel_html("Laporan Data User", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data user:\n{str(e)}")

    # ====================== 2. BARANG ======================
    def report_all_barang(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT kode_barang, nama_barang, kategori, stok, 
                       CONCAT('Rp ', FORMAT(harga, 0)) as harga
                FROM barang
                ORDER BY nama_barang
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Kode Barang", "Nama Barang", "Kategori", "Stok", "Harga"]
            self.export_to_excel_html("Laporan Data Barang", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data barang:\n{str(e)}")

    # ====================== 3. BARANG MASUK ======================
    def report_barang_masuk(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    DATE_FORMAT(t.tanggal, '%d-%m-%Y %H:%i') as tanggal,
                    b.kode_barang,
                    b.nama_barang,
                    dt.quantity,
                    u.username
                FROM transaksi t
                JOIN detail_transaksi dt ON dt.id_transaksi = t.id
                JOIN barang b ON dt.id_barang = b.id
                JOIN user u ON t.id_user = u.id
                WHERE t.type_transaksi = 'masuk'
                ORDER BY t.tanggal DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Tanggal", "Kode Barang", "Nama Barang", "Jumlah", "User"]
            self.export_to_excel_html("Laporan Barang Masuk", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data barang masuk:\n{str(e)}")

    # ====================== 4. BARANG KELUAR ======================
    def report_barang_keluar(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    DATE_FORMAT(t.tanggal, '%d-%m-%Y %H:%i') as tanggal,
                    b.kode_barang,
                    b.nama_barang,
                    dt.quantity,
                    u.username,
                    IFNULL(t.tujuan, '-') as tujuan
                FROM transaksi t
                JOIN detail_transaksi dt ON dt.id_transaksi = t.id
                JOIN barang b ON dt.id_barang = b.id
                JOIN user u ON t.id_user = u.id
                WHERE t.type_transaksi = 'keluar'
                ORDER BY t.tanggal DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Tanggal", "Kode Barang", "Nama Barang", "Jumlah", "User", "Tujuan"]
            self.export_to_excel_html("Laporan Barang Keluar", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data barang keluar:\n{str(e)}")

    # ====================== 5. STOK MIN ======================
    def report_stok_min(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT kode_barang, nama_barang, kategori, stok
                FROM barang
                WHERE stok <= 5
                ORDER BY stok
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Kode Barang", "Nama Barang", "Kategori", "Stok"]
            self.export_to_excel_html("Laporan Stok Minimum", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data stok minimum:\n{str(e)}")

    # ====================== 6. SEMUA TRANSAKSI ======================
    def report_transaksi_keseluruhan(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    t.type_transaksi,
                    DATE_FORMAT(t.tanggal, '%d-%m-%Y %H:%i') as tanggal,
                    b.kode_barang,
                    b.nama_barang,
                    dt.quantity,
                    u.username,
                    IFNULL(t.tujuan, '') as tujuan
                FROM transaksi t
                JOIN detail_transaksi dt ON dt.id_transaksi = t.id
                JOIN barang b ON dt.id_barang = b.id
                JOIN user u ON t.id_user = u.id
                ORDER BY t.tanggal DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Tipe", "Tanggal", "Kode Barang", "Nama Barang", "Jumlah", "User", "Tujuan"]
            self.export_to_excel_html("Laporan Semua Transaksi", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data transaksi:\n{str(e)}")

    # ====================== 7. AKTIVITAS USER ======================
    def report_aktivitas_user(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    u.username,
                    l.aktivitas,
                    l.keterangan,
                    l.tabel_terkait,
                    DATE_FORMAT(l.created_at, '%d-%m-%Y %H:%i:%s') as waktu
                FROM log_aktivitas l
                JOIN user u ON l.id_user = u.id
                ORDER BY l.created_at DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["User", "Aktivitas", "Keterangan", "Tabel", "Waktu"]
            self.export_to_excel_html("Laporan Aktivitas User", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data aktivitas:\n{str(e)}")