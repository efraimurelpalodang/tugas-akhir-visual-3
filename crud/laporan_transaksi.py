import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem

class LaporanTransaksiHandler:
    def __init__(self, page):
        self.page = page

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

        # ambil data transaksi + join ke supplier & user
        cursor.execute("""
            SELECT 
                t.kode_transaksi,
                s.nama_supplier,
                t.total_harga,
                t.type_transaksi,
                u.nama_lengkap AS petugas,
                t.keterangan,
                t.tanggal
            FROM transaksi t
            LEFT JOIN supplier s ON t.id_supplier = s.id
            LEFT JOIN user u ON t.id_user = u.id
            ORDER BY t.created_at DESC
        """)

        rows = cursor.fetchall()
        table = self.page.tableWidget
        table.setRowCount(0)

        for row in rows:
            idx = table.rowCount()
            table.insertRow(idx)
            table.setItem(idx, 0, QTableWidgetItem(row["kode_transaksi"]))
            table.setItem(idx, 1, QTableWidgetItem(row["nama_supplier"] if row["nama_supplier"] else "-"))
            table.setItem(idx, 2, QTableWidgetItem(str(row["total_harga"])))
            table.setItem(idx, 3, QTableWidgetItem(row["type_transaksi"]))
            table.setItem(idx, 4, QTableWidgetItem(row["petugas"] if row["petugas"] else "-"))
            table.setItem(idx, 5, QTableWidgetItem(row["keterangan"]))
            table.setItem(idx, 6, QTableWidgetItem(str(row["tanggal"])))

        # table hanya read-only
        table.setEditTriggers(table.NoEditTriggers)

        cursor.close()
        conn.close()
