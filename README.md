# 📋 Task Management Sederhana (Bisa Dibuka Tanpa Python)

Aplikasi manajemen task/tugas super mudah berbasis Web Statis! Kini dengan antarmuka modern yang dapat langsung Anda jalankan di browser mana saja secara instan.

## ✨ Fitur Utama

- ⚡ **Tanpa Install / Tanpa Server** - Cukup *double-click* file `index.html`
- 🎨 **Minimalis & Interaktif** - Tema biru muda (Light Blue) dengan efek *glassmorphism* dan animasi yang memanjakan mata.
- ➕ **Tambah / Edit Deskripsi Task** - Simpan prioritas tugas dan tanggal tenggat waktu.
- 💾 **Auto Save** - Data akan otomatis tersimpan di Local Storage browser (tidak akan hilang kalau di-refresh).
- 🔍 **Realtime Search & Filter** - Cari tugas dan saring berdasarkan Prioritas maupun Status.

## 🚀 Cara Menjalankan

Lupakan Python, instalasi dependensi, atau pengetikan di Command Line.

1. Buka folder `task_management_sederhana`.
2. Klik 2x file **`index.html`** (Nanti akan otomatis terbuka di Chrome / Edge / Firefox / Safari).
3. Selesai! Mulailah buat daftar tugas Anda.

## 📁 Struktur Project

```text
task_management_sederhana/
├── index.html       # Antarmuka (UI) Aplikasi
├── style.css        # Desain dan Gaya (Warna Biru Muda, Layout, dll.)
├── script.js        # Logika aplikasi (Simpan Data & Interaksi)
├── README.md        # Dokumentasi
├── .gitignore       
└── arsip/           # Berisi file-file code Python dan CLI versi lama
```

## 📖 Cara Penggunaan

1. **Tambah Tugas:** Klik tombol **"Tambah Task Baru"** di sudut kanan atas. Masukkan detail tugas Anda (Judul wajib diisi).
2. **Selesaikan Tugas:** Centang kotak [*checkbox* = kotak persegi] di sebelah kiri judul tugas untuk menandainya sebagai Selesai.
3. **Filter Data:** Gunakan dropdown di atas untuk hanya melihat tugas *High Priority* atau yang belum selesai.
4. **Hapus Sekaligus:** Klik tombol "Hapus Semua Selesai" jika Anda sudah menyelesaikan banyak tugas dan ingin mengosongkan riwayat tugas yang sudah centang biru.

## 💾 Tentang Data Anda

Aplikasi ini menggunakan teknologi yang disebut **Local Storage** pada browser Anda. Data tugas Anda aman secara lokal di laptop/komputer Anda. Jika folder ini Anda pindahkan ke HP sekalipun, Anda bisa melihat antarmukanya (meskipun data di laptop dan HP akan tersimpan terpisah di masing-masing perangkat).

## 🔧 Teknologi
- HTML5 (Semantic Structure)
- CSS3 (Custom Variables, Flexbox, Animations)
- Vanilla JavaScript (ES6, LocalStorage API, DOM Manipulation)

## 📄 Lisensi
Open Source 🎉
