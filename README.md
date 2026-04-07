# 📋 Task Management Sederhana

Aplikasi manajemen task/tugas sederhana berbasis CLI (Command Line Interface) dengan penyimpanan data menggunakan JSON.

## ✨ Fitur

- ➕ **Tambah Task** - Buat task baru dengan judul, deskripsi, status, priority, dan due date
- 📋 **Lihat Semua Task** - Tampilkan daftar semua task yang tersimpan
- 🔍 **Cari Task** - Cari task berdasarkan ID
- ✏️ **Update Task** - Edit informasi task yang sudah ada
- 🗑️ **Hapus Task** - Hapus task dari daftar
- 📊 **Filter by Status** - Filter task berdasarkan status (pending, in_progress, completed)
- 🎯 **Filter by Priority** - Filter task berdasarkan priority (low, medium, high)

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.7 atau lebih baru

### Install & Run

```bash
# Clone repository
git clone https://github.com/username/task_management_sederhana.git
cd task_management_sederhana

# Jalankan aplikasi
python main.py
```

## 📁 Struktur Project

```
task_management_sederhana/
├── main.py          # Entry point aplikasi CLI
├── models.py        # Definisi data class Task
├── storage.py       # Logika penyimpanan JSON
├── tasks.json       # File database (auto-generated)
├── README.md        # Dokumentasi
└── .gitignore       # Git ignore rules
```

## 📖 Cara Penggunaan

1. **Jalankan aplikasi** dengan `python main.py`
2. **Pilih menu** sesuai kebutuhan (ketik angka 0-7)
3. **Ikuti instruksi** yang muncul di layar

### Status Task
- `pending` - Belum dikerjakan
- `in_progress` - Sedang dikerjakan
- `completed` - Selesai

### Priority Task
- `low` - Prioritas rendah 🟢
- `medium` - Prioritas sedang 🟡
- `high` - Prioritas tinggi 🔴

## 💾 Penyimpanan Data

Data disimpan secara otomatis dalam file `tasks.json` di folder yang sama. Tidak perlu setup database!

## 📝 Contoh Penggunaan

```
📋 TASK MANAGEMENT SEDERHANA
========================================
1. ➕ Tambah Task
2. 📋 Lihat Semua Task
3. 🔍 Cari Task by ID
4. ✏️  Update Task
5. 🗑️  Hapus Task
6. 📊 Filter by Status
7. 🎯 Filter by Priority
0. 🚪 Keluar
========================================
Pilih menu: 1

--- TAMBAH TASK ---
Judul Task: Belajar Python
Deskripsi (opsional): Belajar OOP dan File Handling
Priority: medium
Status: pending
Due Date (YYYY-MM-DD, opsional): 2024-12-31

✅ Task berhasil ditambahkan dengan ID: 1
```

## 🔧 Teknologi

- Python 3.7+
- Standard Library: `dataclasses`, `json`, `datetime`

## 📄 Lisensi

Open Source - Bebas digunakan dan dimodifikasi! 🎉
