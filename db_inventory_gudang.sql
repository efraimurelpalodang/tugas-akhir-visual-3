-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.4.3 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for db_inventory_gudang
CREATE DATABASE IF NOT EXISTS `db_inventory_gudang` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_inventory_gudang`;

-- Dumping structure for table db_inventory_gudang.barang
CREATE TABLE IF NOT EXISTS `barang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_barang` varchar(150) DEFAULT NULL,
  `id_kategori` int NOT NULL,
  `id_satuan` int NOT NULL,
  `harga_beli` decimal(15,2) DEFAULT NULL,
  `harga_jual` decimal(15,2) DEFAULT NULL,
  `stok_minimum` int DEFAULT NULL,
  `stok` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_kategori_barang` (`id_kategori`),
  KEY `fk_kategori_satuan` (`id_satuan`),
  CONSTRAINT `fk_kategori_barang` FOREIGN KEY (`id_kategori`) REFERENCES `kategori` (`id`),
  CONSTRAINT `fk_kategori_satuan` FOREIGN KEY (`id_satuan`) REFERENCES `satuan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.barang: ~11 rows (approximately)
INSERT INTO `barang` (`id`, `nama_barang`, `id_kategori`, `id_satuan`, `harga_beli`, `harga_jual`, `stok_minimum`, `stok`, `created_at`, `updated_at`) VALUES
	(1, 'Mouse Wireless Logitech M185', 1, 1, 50000.00, 75000.00, 10, 50, '2025-10-16 23:50:46', '2025-10-16 23:50:46'),
	(2, 'Kertas HVS A4 70gsm', 2, 2, 150000.00, 200000.00, 20, 130, '2025-10-16 23:50:46', '2025-10-16 23:50:46'),
	(3, 'Keripik Kentang Rasa Original', 3, 1, 2000.00, 3500.00, 5, 80, '2025-10-16 23:50:46', '2025-10-16 23:50:46'),
	(4, 'Cairan Pembersih Lantai 5L', 4, 6, 3000.00, 5000.00, 5, 30, '2025-10-16 23:50:46', '2025-10-16 23:50:46'),
	(5, 'Palu Kambing 16 Oz', 5, 1, 12000.00, 15000.00, 5, 25, '2025-10-16 23:50:46', '2025-10-16 23:50:46'),
	(6, 'Plastik Kemasan Roll 1 Meter', 6, 5, 30000.00, 35000.00, 10, 45, '2025-10-16 23:50:46', '2025-10-16 23:50:46'),
	(7, 'Mouse Wireless', 1, 1, 50000.00, 75000.00, 5, 2, '2026-01-22 00:54:54', '2026-01-22 00:54:54'),
	(8, 'Keyboard Mechanical', 1, 1, 150000.00, 200000.00, 3, 1, '2026-01-22 00:54:54', '2026-01-22 00:54:54'),
	(9, 'Pulpen Biru', 2, 1, 2000.00, 3500.00, 10, 4, '2026-01-22 00:54:54', '2026-01-22 00:54:54'),
	(10, 'Air Mineral 600ml', 4, 3, 3000.00, 5000.00, 12, 6, '2026-01-22 00:54:54', '2026-01-22 00:54:54'),
	(11, 'Gula Pasir', 3, 4, 12000.00, 15000.00, 8, 3, '2026-01-22 00:54:54', '2026-01-22 00:54:54');

-- Dumping structure for table db_inventory_gudang.detail_transaksi
CREATE TABLE IF NOT EXISTS `detail_transaksi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_transaksi` int NOT NULL,
  `id_barang` int NOT NULL,
  `quantity` int DEFAULT NULL,
  `harga_satuan` decimal(15,2) DEFAULT NULL,
  `sub_total` decimal(15,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_transaksi_detail` (`id_transaksi`),
  KEY `fk_barang_detail` (`id_barang`),
  CONSTRAINT `fk_barang_detail` FOREIGN KEY (`id_barang`) REFERENCES `barang` (`id`),
  CONSTRAINT `fk_transaksi_detail` FOREIGN KEY (`id_transaksi`) REFERENCES `transaksi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.detail_transaksi: ~8 rows (approximately)
INSERT INTO `detail_transaksi` (`id`, `id_transaksi`, `id_barang`, `quantity`, `harga_satuan`, `sub_total`, `created_at`) VALUES
	(1, 1, 1, 50, 55000.00, 2750000.00, '2025-10-17 00:04:51'),
	(2, 1, 4, 0, 45000.00, 0.00, '2025-10-17 00:04:51'),
	(3, 2, 2, 10, 45000.00, 450000.00, '2025-10-17 00:04:51'),
	(4, 3, 2, 120, 35000.00, 4200000.00, '2025-10-17 00:04:51'),
	(5, 3, 6, 0, 25000.00, 0.00, '2025-10-17 00:04:51'),
	(6, 4, 3, 20, 15000.00, 300000.00, '2025-10-17 00:04:51'),
	(7, 5, 5, 2, 60000.00, 120000.00, '2025-10-17 00:04:51'),
	(8, 6, 1, 10, 75000.00, 750000.00, '2025-10-17 00:04:51');

-- Dumping structure for table db_inventory_gudang.kategori
CREATE TABLE IF NOT EXISTS `kategori` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.kategori: ~6 rows (approximately)
INSERT INTO `kategori` (`id`, `nama_kategori`) VALUES
	(1, 'Elektronik'),
	(2, 'Alat Tulis Kantor'),
	(3, 'Makanan Ringan'),
	(4, 'Alat Kebersihan'),
	(5, 'Perkakas'),
	(6, 'Bahan Baku');

-- Dumping structure for table db_inventory_gudang.log_aktivitas
CREATE TABLE IF NOT EXISTS `log_aktivitas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `aktivitas` varchar(50) DEFAULT NULL,
  `keterangan` text,
  `tabel_terkait` varchar(50) DEFAULT NULL,
  `tabel_record` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_user_log_aktivitas` (`id_user`),
  CONSTRAINT `fk_user_log_aktivitas` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.log_aktivitas: ~8 rows (approximately)
INSERT INTO `log_aktivitas` (`id`, `id_user`, `aktivitas`, `keterangan`, `tabel_terkait`, `tabel_record`, `created_at`) VALUES
	(1, 1, 'Login', 'Admin Budi Santoso berhasil masuk', 'User', 1, '2025-10-17 00:12:04'),
	(2, 2, 'Input Transaksi Masuk', 'Input TRM-20250105-001', 'Transaksi', 1, '2025-10-17 00:12:04'),
	(3, 2, 'Update Stok', 'Stok Barang ID 1 diperbarui dari 0 menjadi 50', 'Barang', 1, '2025-10-17 00:12:04'),
	(4, 4, 'Input Transaksi Keluar', 'Input TRK-20250106-001', 'Transaksi', 2, '2025-10-17 00:12:04'),
	(5, 4, 'Update Stok', 'Stok Barang ID 2 dikurangi 10 (dari 130 menjadi 120)', 'Barang', 2, '2025-10-17 00:12:04'),
	(6, 3, 'Tambah Kategori', 'Menambahkan kategori Perkakas', 'Kategori', 5, '2025-10-17 00:12:04'),
	(7, 2, 'Input Transaksi Masuk', 'Input TRM-20250108-002', 'Transaksi', 3, '2025-10-17 00:12:04'),
	(8, 2, 'Update Stok', 'Stok Barang ID 2 diperbarui dari 120 menjadi 240', 'Barang', 2, '2025-10-17 00:12:04');

-- Dumping structure for table db_inventory_gudang.satuan
CREATE TABLE IF NOT EXISTS `satuan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_satuan` varchar(70) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.satuan: ~6 rows (approximately)
INSERT INTO `satuan` (`id`, `nama_satuan`) VALUES
	(1, 'Pcs'),
	(2, 'Dus'),
	(3, 'kg'),
	(4, 'Meter'),
	(5, 'Roll'),
	(6, 'Liter');

-- Dumping structure for table db_inventory_gudang.supplier
CREATE TABLE IF NOT EXISTS `supplier` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_supplier` varchar(100) NOT NULL,
  `alamat` text,
  `telepon` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.supplier: ~7 rows (approximately)
INSERT INTO `supplier` (`id`, `nama_supplier`, `alamat`, `telepon`, `email`, `created_at`) VALUES
	(1, 'PT Sinar Terang', 'Jl. Raya No. 12', '021-123456', 'sinar@mail.com', '2025-10-16 23:37:47'),
	(2, 'CV Maju Bersama', 'Jl. Industri III No. 5', '022-987654', 'maju@mail.com', '2025-10-16 23:37:47'),
	(3, 'Toko Bahan Baku Abadi', 'Jl. Merdeka Kav. 8', '0812-3456-789', 'abadi@mail.com', '2025-10-16 23:37:47'),
	(4, 'UD Jaya Sentosa', 'Jl. A. Yani Blok B', '0856-7890-123', 'jaya@mail.com', '2025-10-16 23:37:47'),
	(5, 'Distributor Peralatan Cepat', 'Jl. Pramuka No. 1', '021-555555', 'cepat@mail.com', '2025-10-16 23:37:47'),
	(6, 'Global Food Supply', 'Jl. Gatot Subroto IV', '022-234567', 'global@mail.com', '2025-10-16 23:37:47'),
	(7, 'PT. Jaya', 'hallogaga@gmail.co.id', 'jl. A. Yani aja', '0123456789', '2026-01-22 00:16:31');

-- Dumping structure for table db_inventory_gudang.transaksi
CREATE TABLE IF NOT EXISTS `transaksi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kode_transaksi` varchar(20) NOT NULL,
  `tanggal` date DEFAULT NULL,
  `type_transaksi` enum('keluar','masuk') DEFAULT NULL,
  `id_supplier` int DEFAULT NULL,
  `id_user` int NOT NULL,
  `total_harga` decimal(15,2) DEFAULT NULL,
  `keterangan` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_supplier_transaksi` (`id_supplier`),
  KEY `fk_user_transaksi` (`id_user`),
  CONSTRAINT `fk_supplier_transaksi` FOREIGN KEY (`id_supplier`) REFERENCES `supplier` (`id`),
  CONSTRAINT `fk_user_transaksi` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.transaksi: ~6 rows (approximately)
INSERT INTO `transaksi` (`id`, `kode_transaksi`, `tanggal`, `type_transaksi`, `id_supplier`, `id_user`, `total_harga`, `keterangan`, `created_at`) VALUES
	(1, 'TRM-20250105-001', '2025-01-05', 'masuk', 1, 2, 2750000.00, 'Pembelian Mouse dan Pembersih', '2025-10-16 23:59:21'),
	(2, 'TRK-20250106-001', '2025-01-06', 'keluar', NULL, 4, 450000.00, 'Pengeluaran untuk Bagian Penjualan', '2025-10-16 23:59:21'),
	(3, 'TRM-20250108-002', '2025-01-08', 'masuk', 2, 2, 4200000.00, 'Pembelian Stok ATK dan Plastik', '2025-10-16 23:59:21'),
	(4, 'TRK-20250110-002', '2025-01-10', 'keluar', NULL, 2, 120000.00, 'Pengeluaran barang rusak (Keripik)', '2025-10-16 23:59:21'),
	(5, 'TRM-20250115-003', '2025-01-15', 'masuk', 5, 4, 300000.00, 'Tambah Stok Palu', '2025-10-16 23:59:21'),
	(6, 'TRK-20250120-003', '2025-01-20', 'keluar', NULL, 4, 750000.00, 'Permintaan Divisi Marketing', '2025-10-16 23:59:21');

-- Dumping structure for table db_inventory_gudang.user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `role` enum('petugas','admin') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table db_inventory_gudang.user: ~7 rows (approximately)
INSERT INTO `user` (`id`, `username`, `password`, `nama_lengkap`, `role`, `created_at`, `is_active`) VALUES
	(1, 'budi.santo', 'password123', 'Budi Santoso', 'petugas', '2025-10-16 23:44:19', 1),
	(2, 'petugas_inv', 'password123', 'Sita Dewi', 'petugas', '2025-10-16 23:44:19', 1),
	(3, 'rama.jaya', 'password123', 'Rahmat Jaya', 'admin', '2025-10-16 23:44:19', 1),
	(4, 'petugas_stok', 'password123', 'Eko Prasetyo', 'petugas', '2025-10-16 23:44:19', 1),
	(5, 'nonaktif', 'password123', 'Tina Susanti', 'petugas', '2025-10-16 23:44:19', 0),
	(6, 'fajar.kur', 'password123', 'Fajar Kurniawan', 'admin', '2025-10-16 23:44:19', 1),
	(7, 'jhon', 'password123', 'Jhon', 'admin', '2026-01-22 01:40:52', 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
