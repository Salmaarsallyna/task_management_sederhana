"""
🌐 Task Management Web App - Streamlit Version
Cara menjalankan: streamlit run app.py
"""
import streamlit as st
from datetime import datetime, date
from models import Task
from storage import TaskStorage

# Konfigurasi halaman
st.set_page_config(
    page_title="📋 Task Management",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi storage
@st.cache_resource
def get_storage():
    return TaskStorage()

storage = get_storage()

# CSS Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .task-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .task-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #212529;
    }
    .task-meta {
        color: #6c757d;
        font-size: 0.9rem;
    }
    .badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.5rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .badge-pending { background-color: #ffc107; color: #000; }
    .badge-in_progress { background-color: #17a2b8; color: #fff; }
    .badge-completed { background-color: #28a745; color: #fff; }
    .badge-low { background-color: #28a745; color: #fff; }
    .badge-medium { background-color: #ffc107; color: #000; }
    .badge-high { background-color: #dc3545; color: #fff; }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Menu
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3176/3176218.png", width=100)
    st.title("📋 Menu")
    
    menu = st.radio(
        "Pilih Menu:",
        ["🏠 Dashboard", "➕ Tambah Task", "📋 Semua Task", "🔍 Filter Task"]
    )
    
    st.markdown("---")
    st.markdown("### 📊 Statistik")
    
    all_tasks = storage.get_all()
    total = len(all_tasks)
    pending = len([t for t in all_tasks if t.status == "pending"])
    in_progress = len([t for t in all_tasks if t.status == "in_progress"])
    completed = len([t for t in all_tasks if t.status == "completed"])
    
    st.metric("Total Task", total)
    st.metric("⏳ Pending", pending)
    st.metric("🔄 In Progress", in_progress)
    st.metric("✅ Completed", completed)

# Fungsi helper untuk badge
def get_status_badge(status):
    icons = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
    return f"<span class='badge badge-{status}'>{icons.get(status, '⏳')} {status.replace('_', ' ').title()}</span>"

def get_priority_badge(priority):
    icons = {"low": "🟢", "medium": "🟡", "high": "🔴"}
    return f"<span class='badge badge-{priority}'>{icons.get(priority, '🟡')} {priority.upper()}</span>"

# Halaman Dashboard
if menu == "🏠 Dashboard":
    st.title("📋 Task Management Dashboard")
    st.markdown("Selamat datang di aplikasi manajemen tugas sederhana!")
    
    # Statistik Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"**Total Task**\n\n### {total}")
    with col2:
        st.warning(f"**Pending**\n\n### {pending}")
    with col3:
        st.info(f"**In Progress**\n\n### {in_progress}")
    with col4:
        st.success(f"**Completed**\n\n### {completed}")
    
    # Progress bar
    if total > 0:
        progress = (completed / total) * 100
        st.markdown(f"### 📊 Progress: {progress:.1f}%")
        st.progress(progress / 100)
    
    # Task Prioritas Tinggi
    st.markdown("---")
    st.markdown("### 🔴 Prioritas Tinggi (High Priority)")
    
    high_priority = storage.filter_by_priority("high")
    high_priority = [t for t in high_priority if t.status != "completed"]
    
    if high_priority:
        for task in high_priority[:5]:  # Tampilkan 5 saja
            with st.container():
                st.warning(f"**{task.title}** | Status: {task.status} | Due: {task.due_date or 'Tidak ada'}")
    else:
        st.success("🎉 Tidak ada task prioritas tinggi yang pending!")
    
    # Task Terbaru
    st.markdown("---")
    st.markdown("### 📝 Task Terbaru")
    
    recent_tasks = sorted(all_tasks, key=lambda x: x.created_at, reverse=True)[:5]
    
    if recent_tasks:
        for task in recent_tasks:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{task.title}** - {task.description or 'Tidak ada deskripsi'}")
            with col2:
                st.write(f"Status: {get_status_badge(task.status)}", unsafe_allow_html=True)
    else:
        st.info("Belum ada task. Tambahkan task baru!")

# Halaman Tambah Task
elif menu == "➕ Tambah Task":
    st.title("➕ Tambah Task Baru")
    
    with st.form("add_task_form"):
        title = st.text_input("📌 Judul Task *", placeholder="Masukkan judul task...")
        description = st.text_area("📝 Deskripsi", placeholder="Deskripsi task (opsional)...")
        
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("🎯 Priority", ["low", "medium", "high"], 
                                   format_func=lambda x: {"low": "🟢 Low", "medium": "🟡 Medium", "high": "🔴 High"}[x])
        with col2:
            status = st.selectbox("📊 Status", ["pending", "in_progress", "completed"],
                                 format_func=lambda x: {"pending": "⏳ Pending", "in_progress": "🔄 In Progress", "completed": "✅ Completed"}[x])
        
        due_date = st.date_input("📅 Due Date (opsional)", value=None)
        
        submitted = st.form_submit_button("💾 Simpan Task", use_container_width=True)
        
        if submitted:
            if not title:
                st.error("❌ Judul task wajib diisi!")
            else:
                task = Task(
                    id=0,
                    title=title,
                    description=description,
                    status=status,
                    priority=priority,
                    due_date=due_date.strftime("%Y-%m-%d") if due_date else None
                )
                storage.add(task)
                st.success(f"✅ Task '{title}' berhasil ditambahkan dengan ID: {task.id}")
                st.balloons()

# Halaman Semua Task
elif menu == "📋 Semua Task":
    st.title("📋 Daftar Semua Task")
    
    if not all_tasks:
        st.info("📭 Belum ada task. Silakan tambah task baru!")
    else:
        # Search & Filter
        search = st.text_input("🔍 Cari task...", placeholder="Ketik judul atau deskripsi...")
        
        filtered_tasks = all_tasks
        if search:
            filtered_tasks = [t for t in all_tasks if search.lower() in t.title.lower() or search.lower() in (t.description or "").lower()]
        
        st.markdown(f"**Menampilkan {len(filtered_tasks)} task**")
        
        for task in filtered_tasks:
            with st.container():
                st.markdown(f"""
                <div class='task-card'>
                    <div class='task-title'>#{task.id} {task.title}</div>
                    <div class='task-meta'>{task.description or 'Tidak ada deskripsi'}</div>
                    <div style='margin-top: 10px;'>
                        {get_status_badge(task.status)} 
                        {get_priority_badge(task.priority)}
                        <span style='margin-left: 10px;'>📅 {task.due_date or 'No due date'} | 🕐 {task.created_at}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
                
                with col1:
                    if task.status != "completed":
                        if st.button(f"✅ Selesai", key=f"complete_{task.id}"):
                            storage.update(task.id, status="completed")
                            st.success("Task ditandai selesai!")
                            st.rerun()
                
                with col2:
                    new_status = st.selectbox(
                        "Status",
                        ["pending", "in_progress", "completed"],
                        index=["pending", "in_progress", "completed"].index(task.status),
                        key=f"status_{task.id}",
                        label_visibility="collapsed"
                    )
                    if new_status != task.status:
                        storage.update(task.id, status=new_status)
                        st.rerun()
                
                with col3:
                    new_priority = st.selectbox(
                        "Priority",
                        ["low", "medium", "high"],
                        index=["low", "medium", "high"].index(task.priority),
                        key=f"priority_{task.id}",
                        label_visibility="collapsed"
                    )
                    if new_priority != task.priority:
                        storage.update(task.id, priority=new_priority)
                        st.rerun()
                
                with col4:
                    if st.button(f"🗑️ Hapus", key=f"delete_{task.id}", type="primary"):
                        storage.delete(task.id)
                        st.warning("Task dihapus!")
                        st.rerun()
                
                st.markdown("---")

# Halaman Filter Task
elif menu == "🔍 Filter Task":
    st.title("🔍 Filter Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Filter by Status")
        status_filter = st.selectbox(
            "Pilih Status",
            ["Semua", "pending", "in_progress", "completed"],
            format_func=lambda x: {"Semua": "📋 Semua", "pending": "⏳ Pending", "in_progress": "🔄 In Progress", "completed": "✅ Completed"}[x]
        )
    
    with col2:
        st.markdown("### 🎯 Filter by Priority")
        priority_filter = st.selectbox(
            "Pilih Priority",
            ["Semua", "low", "medium", "high"],
            format_func=lambda x: {"Semua": "📋 Semua", "low": "🟢 Low", "medium": "🟡 Medium", "high": "🔴 High"}[x]
        )
    
    # Apply filters
    filtered = all_tasks
    
    if status_filter != "Semua":
        filtered = [t for t in filtered if t.status == status_filter]
    
    if priority_filter != "Semua":
        filtered = [t for t in filtered if t.priority == priority_filter]
    
    st.markdown("---")
    st.markdown(f"**Hasil: {len(filtered)} task ditemukan**")
    
    if not filtered:
        st.info("📭 Tidak ada task yang cocok dengan filter.")
    else:
        for task in filtered:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**#{task.id} {task.title}**")
                    st.caption(f"{task.description or 'Tidak ada deskripsi'} | 📅 {task.due_date or 'No due date'}")
                with col2:
                    st.markdown(get_status_badge(task.status), unsafe_allow_html=True)
                    st.markdown(get_priority_badge(task.priority), unsafe_allow_html=True)
                st.markdown("---")

# Footer
st.markdown("---")
st.caption("🚀 Task Management Sederhana - Made with Streamlit ❤️")
