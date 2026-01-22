import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

class LaporanStokHandler:
    def __init__(self, page):
        self.page = page

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_inventory_gudang"
        )

    def load_table_low_stock(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                b.nama_barang,
                k.nama_kategori,
                s.nama_satuan,
                b.stok,
                b.stok_minimum
            FROM barang b
            LEFT JOIN kategori k ON b.id_kategori = k.id
            LEFT JOIN satuan s ON b.id_satuan = s.id
            WHERE b.stok < b.stok_minimum
            ORDER BY b.nama_barang ASC
        """)

        rows = cursor.fetchall()
        table = self.page.tableWidget
        table.setRowCount(0)

        if not rows:
            # semua stok aman → buat 1 row, gabungkan semua kolom
            col_count = table.columnCount() or 5  # pastikan jumlah kolom
            table.setRowCount(1)
            table.setSpan(0, 0, 1, col_count)  # gabungkan semua kolom di baris 0
            item = QTableWidgetItem("Semua stok aman")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)
            table.setEditTriggers(table.NoEditTriggers)
            cursor.close()
            conn.close()
            return

        # kalau ada barang di bawah minimum
        for row in rows:
            idx = table.rowCount()
            table.insertRow(idx)
            table.setItem(idx, 0, QTableWidgetItem(row["nama_barang"]))
            table.setItem(idx, 1, QTableWidgetItem(row["nama_kategori"] if row["nama_kategori"] else "-"))
            table.setItem(idx, 2, QTableWidgetItem(row["nama_satuan"] if row["nama_satuan"] else "-"))
            table.setItem(idx, 3, QTableWidgetItem(str(row["stok"])))
            table.setItem(idx, 4, QTableWidgetItem(str(row["stok_minimum"])))

        table.setEditTriggers(table.NoEditTriggers)
        cursor.close()
        conn.close()
