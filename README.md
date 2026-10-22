# Sistem Informasi E-Parkir Plaza Andalas

> Spesifikasi Kebutuhan, Rancangan Arsitektur, Flowchart Sistem, dan Data Flow Diagram (DFD Level 0 & Level 1) berbasis Draw.io.

---

## 📋 Deskripsi Proyek
Aplikasi **E-Parkir Plaza Andalas** adalah sistem manajemen parkir berbasis web yang dirancang untuk menangani:
1. Proses masuk dan keluar kendaraan secara otomatis.
2. Pencetakan karcis unik berbasis Token & QR Code untuk Non-Member.
3. Pengelolaan pelanggan berlangganan (Member) berbasis kartu QR.
4. Transaksi pembayaran tunai di pintu keluar oleh Petugas Kasir.
5. Pelaporan transaksi terpusat untuk Petugas dan Super Admin.

---

## 👥 Aktor & Hak Akses
| No | Aktor | Hak Akses Utama |
|---|---|---|
| 1 | **User Non-Member** | Akses Landing Page gate masuk, tekan tombol PRINT untuk mendapatkan karcis QR & Token, menerima invoice di pintu keluar. |
| 2 | **User Member** | Scan QR kartu member di gate masuk, bayar langganan bulanan di awal bulan, menerima kartu member & invoice. |
| 3 | **Petugas (Kasir)** | Login/lupa password, scan QR/input token non-member, input transaksi pembayaran (kategori, no. plat, uang tunai, kembalian), kelola member (CRUD), cetak laporan transaksi. |
| 4 | **Super Admin** | Kelola akun petugas (CRUD), cari & cetak laporan pembayaran member serta non-member seluruh petugas. |

---

## 🛠️ Rekomendasi Tech Stack
* **Backend:** PHP 8.2+ dengan Framework Laravel 10/11 (MVC, OOP, Middleware, PHPUnit)
* **Frontend:** Blade Templating + Tailwind CSS + Alpine.js / Vanilla JS
* **Database:** MySQL / MariaDB (Relasional, ACID, Foreign Key)
* **QR Engine:** `simplesoftwareio/simple-qrcode` & `html5-qrcode`
* **Dokumen/Struk:** `barryvdh/laravel-dompdf` & `@media print`

---

## 📊 Diagram Arsitektur Draw.io (`.drawio`)
Diagram arsitektur sistem ini disimpan dalam format XML native draw.io di folder `drawio/`:

1. **`drawio/flowchart-eparkir.drawio`**
   * **Parkir Masuk:** Gate In Non-Member (Print Token/QR & Simpan DB) vs Member (Scan Kartu & Validasi).
   * **Parkir Keluar & Kasir:** Perhitungan durasi `ceil(Keluar - Masuk)`, perhitungan tarif bertingkat, validasi uang tunai `>=` total tagihan, perhitungan kembalian, update database, dan cetak invoice.

2. **`drawio/dfd-eparkir.drawio`** (Multi-Page Diagram)
   * **Page 1 - DFD Level 0 (Diagram Konteks):** Hubungan 3 entitas eksternal (`User`, `Petugas Kasir`, `Super Admin`) dengan sistem sentral `0.0 Sistem Informasi E-Parkir`.
   * **Page 2 - DFD Level 1 (Rincian Proses & Data Store):**
     * `1.0 Autentikasi & Reset Password`
     * `2.0 Manajemen Akun & Member`
     * `3.0 Registrasi Parkir Masuk`
     * `4.0 Transaksi Pembayaran & Cetak Invoice`
     * `5.0 Pelaporan Keuangan & Transaksi Terpusat`
     * Data Stores: `D1: users`, `D2: members`, `D3: parking_transactions`, `D4: member_payments`.

---

## 💡 Cara Membuka Diagram di Draw.io
1. Buka [app.diagrams.net](https://app.diagrams.net/) di browsermu.
2. Klik **Open Existing Diagram**.
3. Pilih salah satu file dari folder `drawio/` (`flowchart-eparkir.drawio` atau `dfd-eparkir.drawio`).
4. Alternatif: Buka file `.drawio` dengan text editor, copy teks XML-nya, lalu di draw.io klik **Arrange → Insert → Advanced → From Text...** dan tempel XML-nya.

---

## 📁 Struktur Repositori
```text
eparkir-plaza-andalas/
├── docs/
│   └── SPESIFIKASI_SISTEM.txt       # Dokumen spesifikasi kebutuhan lengkap Bab 1-7
├── drawio/
│   ├── flowchart-eparkir.drawio     # Diagram Flowchart Masuk & Keluar (Draw.io XML)
│   └── dfd-eparkir.drawio           # Diagram DFD Level 0 & Level 1 (Multi-page XML)
├── scripts/
│   └── generate_drawio_diagrams.py  # Script Python generator diagram draw.io XML
├── index.html                       # Viewer HTML interaktif untuk web
├── .gitignore
└── README.md
```

---

## 📄 Lisensi
Hak Cipta &copy; 2026 E-Parkir Plaza Andalas Project.
