# Aplikasi Inventory Barang  
*Tugas Akhir Mata Kuliah Pemrograman Visual 3*

## 📌 Deskripsi Proyek
Aplikasi Inventory Barang merupakan proyek tugas akhir pada mata kuliah **Pemrograman Visual 3**.  
Aplikasi ini dibuat menggunakan **Python** dengan **PyQt5** dan **Qt Designer** sebagai antarmuka grafis (GUI).

Aplikasi ini bertujuan untuk membantu pengelolaan data barang secara terkomputerisasi, meliputi proses penambahan, penampilan, pengubahan, dan penghapusan data barang.

---

## 🛠️ Teknologi yang Digunakan
- Python 3
- PyQt5
- Qt Designer
- MySQL
- mysql-connector-python
- Visual Studio Code

---

## 📂 Struktur Folder

tugas-akhir-visual-3/
│
├── crud/
│ ├── crud_user.py
│ ├── crud_barang.py
│ └── ...
│
├── ui/
│ └── layouts/
│ ├── login.ui
│ ├── dashboard.ui
│ └── ...
│
├── main.py
├── README.md
└── .vscode/


---

## ⚙️ Fitur Aplikasi
- Login pengguna
- Manajemen data barang
  - Tambah data barang
  - Lihat data barang
  - Edit data barang
  - Hapus data barang
- Antarmuka grafis menggunakan Qt Designer
- Koneksi database MySQL

---

## 🗄️ Konfigurasi Database
Pastikan MySQL sudah aktif dan database telah dibuat.

konfigurasi database pada program:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_inventory_gudang"
)

▶️ Cara Menjalankan Aplikasi

Clone repository:
git clone https://github.com/efraimurelpalodang/tugas-akhir-visual-3.git

Masuk ke folder project:
cd tugas-akhir-visual-3

Install dependency:
pip install pyqt5 mysql-connector-python

Jalankan aplikasi:
python main.py

👤 Identitas Mahasiswa (Kelompok)
NPM  : 2310010093                                          NPM  : 2310010235
Nama : Efraim Urel Palodang                                Nama : Maulana Zidane   
