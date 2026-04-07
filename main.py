#!/usr/bin/env python3
"""Aplikasi Task Management Sederhana - CLI"""

from models import Task
from storage import TaskStorage


def print_menu():
    """Tampilkan menu utama."""
    print("\n" + "=" * 40)
    print("📋 TASK MANAGEMENT SEDERHANA")
    print("=" * 40)
    print("1. ➕ Tambah Task")
    print("2. 📋 Lihat Semua Task")
    print("3. 🔍 Cari Task by ID")
    print("4. ✏️  Update Task")
    print("5. 🗑️  Hapus Task")
    print("6. 📊 Filter by Status")
    print("7. 🎯 Filter by Priority")
    print("0. 🚪 Keluar")
    print("=" * 40)


def get_input(prompt: str, required: bool = True) -> str:
    """Ambil input dari user."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("⚠️  Input tidak boleh kosong!")


def tambah_task(storage: TaskStorage):
    """Tambah task baru."""
    print("\n--- TAMBAH TASK ---")
    title = get_input("Judul Task: ")
    description = get_input("Deskripsi (opsional): ", required=False)
    
    print("\nPriority: low, medium, high")
    priority = get_input("Priority [medium]: ", required=False) or "medium"
    
    print("\nStatus: pending, in_progress, completed")
    status = get_input("Status [pending]: ", required=False) or "pending"
    
    due_date = get_input("Due Date (YYYY-MM-DD, opsional): ", required=False) or None
    
    task = Task(
        id=0,  # Akan di-set oleh storage
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date
    )
    
    storage.add(task)
    print(f"\n✅ Task berhasil ditambahkan dengan ID: {task.id}")


def lihat_semua_task(storage: TaskStorage):
    """Tampilkan semua task."""
    print("\n--- DAFTAR SEMUA TASK ---")
    tasks = storage.get_all()
    
    if not tasks:
        print("📭 Belum ada task.")
        return
    
    print(f"\nTotal: {len(tasks)} task\n")
    for task in tasks:
        print(f"  {task}")
        if task.description:
            print(f"      📝 {task.description}")
        if task.due_date:
            print(f"      📅 Due: {task.due_date}")
        print(f"      🕐 Dibuat: {task.created_at}")
        print()


def cari_task(storage: TaskStorage):
    """Cari task berdasarkan ID."""
    print("\n--- CARI TASK ---")
    try:
        task_id = int(get_input("Masukkan ID Task: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return
    
    task = storage.get_by_id(task_id)
    if task:
        print(f"\n📋 Detail Task #{task.id}:")
        print(f"  Judul: {task.title}")
        print(f"  Deskripsi: {task.description or '-'}")
        print(f"  Status: {task.status}")
        print(f"  Priority: {task.priority}")
        print(f"  Due Date: {task.due_date or '-'}")
        print(f"  Dibuat: {task.created_at}")
    else:
        print(f"❌ Task dengan ID {task_id} tidak ditemukan.")


def update_task(storage: TaskStorage):
    """Update task yang sudah ada."""
    print("\n--- UPDATE TASK ---")
    try:
        task_id = int(get_input("Masukkan ID Task yang akan diupdate: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return
    
    task = storage.get_by_id(task_id)
    if not task:
        print(f"❌ Task dengan ID {task_id} tidak ditemukan.")
        return
    
    print(f"\nTask saat ini: {task.title}")
    print("(Tekan Enter untuk mempertahankan nilai saat ini)\n")
    
    title = get_input(f"Judul [{task.title}]: ", required=False)
    description = get_input(f"Deskripsi [{task.description}]: ", required=False)
    status = get_input(f"Status [{task.status}]: ", required=False)
    priority = get_input(f"Priority [{task.priority}]: ", required=False)
    due_date = get_input(f"Due Date [{task.due_date or '-'}]: ", required=False)
    
    updates = {}
    if title:
        updates['title'] = title
    if description:
        updates['description'] = description
    if status:
        updates['status'] = status
    if priority:
        updates['priority'] = priority
    if due_date:
        updates['due_date'] = due_date
    
    if storage.update(task_id, **updates):
        print(f"\n✅ Task #{task_id} berhasil diupdate!")
    else:
        print(f"\n❌ Gagal mengupdate task.")


def hapus_task(storage: TaskStorage):
    """Hapus task."""
    print("\n--- HAPUS TASK ---")
    try:
        task_id = int(get_input("Masukkan ID Task yang akan dihapus: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return
    
    task = storage.get_by_id(task_id)
    if not task:
        print(f"❌ Task dengan ID {task_id} tidak ditemukan.")
        return
    
    confirm = get_input(f"Yakin hapus '{task.title}'? (y/n): ").lower()
    if confirm == 'y':
        if storage.delete(task_id):
            print(f"\n✅ Task #{task_id} berhasil dihapus!")
        else:
            print(f"\n❌ Gagal menghapus task.")
    else:
        print("❌ Penghapusan dibatalkan.")


def filter_status(storage: TaskStorage):
    """Filter task berdasarkan status."""
    print("\n--- FILTER BY STATUS ---")
    print("Status: pending, in_progress, completed")
    status = get_input("Masukkan status: ")
    
    tasks = storage.filter_by_status(status)
    
    if not tasks:
        print(f"📭 Tidak ada task dengan status '{status}'.")
        return
    
    print(f"\n📋 Task dengan status '{status}': {len(tasks)} task\n")
    for task in tasks:
        print(f"  {task}")


def filter_priority(storage: TaskStorage):
    """Filter task berdasarkan priority."""
    print("\n--- FILTER BY PRIORITY ---")
    print("Priority: low, medium, high")
    priority = get_input("Masukkan priority: ")
    
    tasks = storage.filter_by_priority(priority)
    
    if not tasks:
        print(f"📭 Tidak ada task dengan priority '{priority}'.")
        return
    
    print(f"\n📋 Task dengan priority '{priority}': {len(tasks)} task\n")
    for task in tasks:
        print(f"  {task}")


def main():
    """Fungsi utama aplikasi."""
    storage = TaskStorage()
    
    print("\n🚀 Selamat datang di Task Management Sederhana!")
    
    while True:
        print_menu()
        choice = get_input("Pilih menu: ", required=False)
        
        if choice == "1":
            tambah_task(storage)
        elif choice == "2":
            lihat_semua_task(storage)
        elif choice == "3":
            cari_task(storage)
        elif choice == "4":
            update_task(storage)
        elif choice == "5":
            hapus_task(storage)
        elif choice == "6":
            filter_status(storage)
        elif choice == "7":
            filter_priority(storage)
        elif choice == "0":
            print("\n👋 Terima kasih! Sampai jumpa!\n")
            break
        else:
            print("\n❌ Pilihan tidak valid!")


if __name__ == "__main__":
    main()
