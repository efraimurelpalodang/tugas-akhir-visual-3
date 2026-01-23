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
        try:
            # Cari semua atribut yang merupakan tombol
            for attr_name in dir(self.page):
                if not attr_name.startswith('_') and hasattr(getattr(self.page, attr_name), 'clicked'):
                    btn = getattr(self.page, attr_name)
                    
                    # Cek jika ini tombol laporan berdasarkan nama
                    attr_lower = attr_name.lower()
                    
                    # ✅ **URUTKAN DENGAN BENAR: aktivitas HARUS SEBELUM barang**
                    
                    # 1. AKTIVITAS USER (PERTAMA!)
                    if 'aktivitas' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()  # Hapus koneksi lama
                        except:
                            pass
                        btn.clicked.connect(self.report_aktivitas_user)
                        continue  # Penting: skip kondisi lainnya
                        
                    # 2. USER
                    elif 'user' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_all_users)
                        continue
                        
                    # 3. BARANG MASUK (spesifik)
                    elif 'barang' in attr_lower and 'masuk' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_barang_masuk)
                        continue
                        
                    # 4. BARANG KELUAR (spesifik)
                    elif 'barang' in attr_lower and 'keluar' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_barang_keluar)
                        continue
                        
                    # 5. STOK
                    elif 'stok' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_stok_min)
                        continue
                        
                    # 6. TRANSAKSI
                    elif 'transaksi' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_transaksi_keseluruhan)
                        continue
                        
                    # 7. BARANG (umum) - HARUS DITEMPATKAN TERAKHIR
                    elif 'barang' in attr_lower and ('cetak' in attr_lower or 'report' in attr_lower or 'export' in attr_lower or 'print' in attr_lower):
                        try:
                            btn.clicked.disconnect()
                        except:
                            pass
                        btn.clicked.connect(self.report_all_barang)
                        
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
                SELECT 
                    id,
                    username, 
                    nama_lengkap, 
                    role, 
                    DATE_FORMAT(created_at, '%d-%m-%Y %H:%i') as tanggal_dibuat,
                    CASE WHEN is_active = 1 THEN 'Aktif' ELSE 'Non-Aktif' END as status
                FROM user
                ORDER BY id
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["ID", "Username", "Nama Lengkap", "Role", "Tanggal Dibuat", "Status"]
            self.export_to_excel_html("Laporan Data User", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data user:\n{str(e)}")

    # ====================== 2. BARANG ======================
    def report_all_barang(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    b.id,
                    b.nama_barang,
                    k.nama_kategori,
                    s.nama_satuan,
                    b.stok,
                    b.stok_minimum,
                    CONCAT('Rp ', FORMAT(b.harga_beli, 0)) as harga_beli,
                    CONCAT('Rp ', FORMAT(b.harga_jual, 0)) as harga_jual,
                    DATE_FORMAT(b.created_at, '%d-%m-%Y') as tanggal_input
                FROM barang b
                LEFT JOIN kategori k ON b.id_kategori = k.id
                LEFT JOIN satuan s ON b.id_satuan = s.id
                ORDER BY b.nama_barang
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["ID", "Nama Barang", "Kategori", "Satuan", "Stok", "Stok Minimum", "Harga Beli", "Harga Jual", "Tanggal Input"]
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
                    t.kode_transaksi,
                    DATE_FORMAT(t.tanggal, '%d-%m-%Y') as tanggal,
                    b.nama_barang,
                    dt.quantity,
                    CONCAT('Rp ', FORMAT(dt.harga_satuan, 0)) as harga_satuan,
                    CONCAT('Rp ', FORMAT(dt.sub_total, 0)) as sub_total,
                    sp.nama_supplier,
                    u.nama_lengkap as user_input
                FROM transaksi t
                JOIN detail_transaksi dt ON dt.id_transaksi = t.id
                JOIN barang b ON dt.id_barang = b.id
                LEFT JOIN supplier sp ON t.id_supplier = sp.id
                JOIN user u ON t.id_user = u.id
                WHERE t.type_transaksi = 'masuk'
                ORDER BY t.tanggal DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Kode Transaksi", "Tanggal", "Nama Barang", "Jumlah", "Harga Satuan", "Sub Total", "Supplier", "User Input"]
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
                    t.kode_transaksi,
                    DATE_FORMAT(t.tanggal, '%d-%m-%Y') as tanggal,
                    b.nama_barang,
                    dt.quantity,
                    CONCAT('Rp ', FORMAT(dt.harga_satuan, 0)) as harga_satuan,
                    CONCAT('Rp ', FORMAT(dt.sub_total, 0)) as sub_total,
                    u.nama_lengkap as user_input,
                    IFNULL(t.keterangan, '-') as keterangan
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

            headers = ["Kode Transaksi", "Tanggal", "Nama Barang", "Jumlah", "Harga Satuan", "Sub Total", "User Input", "Keterangan"]
            self.export_to_excel_html("Laporan Barang Keluar", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data barang keluar:\n{str(e)}")

    # ====================== 5. STOK MIN ======================
    def report_stok_min(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    b.id,
                    b.nama_barang,
                    k.nama_kategori,
                    b.stok,
                    b.stok_minimum,
                    CASE 
                        WHEN b.stok <= b.stok_minimum THEN 'Kritis'
                        WHEN b.stok <= (b.stok_minimum * 2) THEN 'Hampir Habis'
                        ELSE 'Aman'
                    END as status_stok
                FROM barang b
                LEFT JOIN kategori k ON b.id_kategori = k.id
                WHERE b.stok <= (b.stok_minimum * 2)
                ORDER BY b.stok
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["ID", "Nama Barang", "Kategori", "Stok Saat Ini", "Stok Minimum", "Status Stok"]
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
                    t.kode_transaksi,
                    DATE_FORMAT(t.tanggal, '%d-%m-%Y') as tanggal,
                    CASE 
                        WHEN t.type_transaksi = 'masuk' THEN 'Barang Masuk'
                        WHEN t.type_transaksi = 'keluar' THEN 'Barang Keluar'
                    END as jenis_transaksi,
                    b.nama_barang,
                    dt.quantity,
                    CONCAT('Rp ', FORMAT(dt.harga_satuan, 0)) as harga_satuan,
                    CONCAT('Rp ', FORMAT(dt.sub_total, 0)) as sub_total,
                    sp.nama_supplier,
                    u.nama_lengkap as user_input,
                    IFNULL(t.keterangan, '-') as keterangan
                FROM transaksi t
                JOIN detail_transaksi dt ON dt.id_transaksi = t.id
                JOIN barang b ON dt.id_barang = b.id
                LEFT JOIN supplier sp ON t.id_supplier = sp.id
                JOIN user u ON t.id_user = u.id
                ORDER BY t.tanggal DESC, t.kode_transaksi
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Kode Transaksi", "Tanggal", "Jenis Transaksi", "Nama Barang", "Jumlah", "Harga Satuan", "Sub Total", "Supplier", "User Input", "Keterangan"]
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
                    u.nama_lengkap,
                    l.aktivitas,
                    l.keterangan,
                    l.tabel_terkait,
                    l.tabel_record,
                    DATE_FORMAT(l.created_at, '%d-%m-%Y %H:%i:%s') as waktu
                FROM log_aktivitas l
                JOIN user u ON l.id_user = u.id
                ORDER BY l.created_at DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            headers = ["Username", "Nama Lengkap", "Aktivitas", "Keterangan", "Tabel Terkait", "ID Record", "Waktu"]
            self.export_to_excel_html("Laporan Aktivitas User", headers, rows)
        except Exception as e:
            QMessageBox.critical(self.page, "Error", f"Gagal mengambil data aktivitas:\n{str(e)}")