document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    let currentEditId = null;

    // --- DOM Elements ---
    const taskList = document.getElementById('task-list');
    const emptyState = document.getElementById('empty-state');
    const totalTasksSpan = document.getElementById('total-tasks');
    
    // Modal & Form Elements
    const modal = document.getElementById('task-modal');
    const form = document.getElementById('task-form');
    const openModalBtn = document.getElementById('open-modal-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelFormBtn = document.getElementById('cancel-form-btn');
    const modalTitle = document.getElementById('modal-title');
    
    // Filter Elements
    const searchInput = document.getElementById('search-input');
    const filterStatus = document.getElementById('filter-status');
    const filterPriority = document.getElementById('filter-priority');
    const clearAllBtn = document.getElementById('clear-all-btn');

    // --- Functions ---

    // Save to LocalStorage
    const saveTasks = () => {
        localStorage.setItem('tasks', JSON.stringify(tasks));
        renderTasks();
    };

    // Render Tasks
    const renderTasks = () => {
        const searchTerm = searchInput.value.toLowerCase();
        const statusFilter = filterStatus.value;
        const priorityFilter = filterPriority.value;

        // Apply filters
        let filteredTasks = tasks.filter(task => {
            const matchesSearch = task.title.toLowerCase().includes(searchTerm) || task.description.toLowerCase().includes(searchTerm);
            const matchesStatus = statusFilter === 'all' || task.status === statusFilter;
            const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter;
            return matchesSearch && matchesStatus && matchesPriority;
        });

        // Update UI stats
        totalTasksSpan.textContent = `${filteredTasks.length} Task${filteredTasks.length !== 1 ? 's' : ''}`;
        
        // Show/hide empty state
        if (filteredTasks.length === 0) {
            taskList.style.display = 'none';
            emptyState.style.display = 'block';
            emptyState.innerHTML = tasks.length === 0 
                ? `<div class="empty-icon">✅</div><h3>Belum ada task</h3><p>Klik tombol "Tambah Task Baru" untuk mulai mencatat tugasmu.</p>`
                : `<div class="empty-icon">🔍</div><h3>Tidak ada hasil</h3><p>Coba sesuaikan kata kunci atau filter pencarian.</p>`;
        } else {
            taskList.style.display = 'flex';
            emptyState.style.display = 'none';
        }

        taskList.innerHTML = '';

        // Render each task
        filteredTasks.forEach(task => {
            const isCompleted = task.status === 'completed';
            
            const taskEl = document.createElement('div');
            taskEl.className = `task-item ${isCompleted ? 'completed' : ''}`;
            taskEl.setAttribute('data-id', task.id);

            // Priority Badge text
            let priorityLabel = '🟡 Medium';
            let priorityClass = 'badge-priority-medium';
            if(task.priority === 'low') { priorityLabel = '🟢 Low'; priorityClass = 'badge-priority-low'; }
            if(task.priority === 'high') { priorityLabel = '🔴 High'; priorityClass = 'badge-priority-high'; }

            // Date formatting
            let dateHtml = '';
            if (task.dueDate) {
                const dateObj = new Date(task.dueDate);
                const formattedDate = dateObj.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric'});
                dateHtml = `<div class="task-date">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    ${formattedDate}
                </div>`;
            }

            taskEl.innerHTML = `
                <div class="checkbox-container">
                    <input type="checkbox" onchange="toggleTaskStatus(${task.id})" ${isCompleted ? 'checked' : ''}>
                    <span class="checkmark"></span>
                </div>
                <div class="task-content">
                    <div class="task-header">
                        <h3 class="task-title">${task.title}</h3>
                        <div class="task-actions">
                            <button class="btn-icon edit" onclick="editTask(${task.id})" title="Edit Task">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </button>
                            <button class="btn-icon delete" onclick="deleteTask(${task.id})" title="Hapus Task">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                            </button>
                        </div>
                    </div>
                    ${task.description ? `<p class="task-desc">${task.description}</p>` : ''}
                    <div class="task-meta">
                        <span class="badge ${priorityClass}">${priorityLabel}</span>
                        ${task.status === 'in_progress' ? `<span class="badge badge-status">🔄 In Progress</span>` : ''}
                        ${task.status === 'pending' && !isCompleted ? `<span class="badge badge-status" style="background:#f1f5f9; color:#475569;">⏳ Pending</span>` : ''}
                        ${dateHtml}
                    </div>
                </div>
            `;
            taskList.appendChild(taskEl);
        });
    };

    // --- Actions ---

    window.toggleTaskStatus = (id) => {
        const task = tasks.find(t => t.id === id);
        if (task) {
            task.status = task.status === 'completed' ? 'pending' : 'completed';
            saveTasks();
        }
    };

    window.deleteTask = (id) => {
        if (confirm('Apakah Anda yakin ingin menghapus task ini?')) {
            tasks = tasks.filter(t => t.id !== id);
            saveTasks();
        }
    };

    window.editTask = (id) => {
        const task = tasks.find(t => t.id === id);
        if (task) {
            currentEditId = id;
            modalTitle.textContent = 'Edit Task';
            
            document.getElementById('task-title').value = task.title;
            document.getElementById('task-desc').value = task.description || '';
            document.getElementById('task-priority').value = task.priority;
            
            // Format status: if it was completed, we keep it as an option or reset to pending. 
            // In a simple app, we can just edit details and it stays in current status.
            
            if (task.dueDate) {
                document.getElementById('task-date').value = task.dueDate;
            } else {
                document.getElementById('task-date').value = '';
            }

            openModal();
        }
    };

    // --- Modal Handling ---
    const openModal = () => {
        modal.classList.add('show');
    };

    const closeModal = () => {
        modal.classList.remove('show');
        form.reset();
        currentEditId = null;
        modalTitle.textContent = 'Tambah Task Baru';
    };

    // Event Listeners related to Modal
    openModalBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    cancelFormBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Form Submit
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const title = document.getElementById('task-title').value.trim();
        const description = document.getElementById('task-desc').value.trim();
        const priority = document.getElementById('task-priority').value;
        const dueDate = document.getElementById('task-date').value;

        if (!title) return;

        if (currentEditId !== null) {
            // Edit existing
            const taskIndex = tasks.findIndex(t => t.id === currentEditId);
            if (taskIndex !== -1) {
                tasks[taskIndex].title = title;
                tasks[taskIndex].description = description;
                tasks[taskIndex].priority = priority;
                tasks[taskIndex].dueDate = dueDate;
            }
        } else {
            // Add new
            const newTask = {
                id: Date.now(),
                title: title,
                description: description,
                status: 'pending',
                priority: priority,
                dueDate: dueDate,
                createdAt: new Date().toISOString()
            };
            tasks.unshift(newTask); // Add to the beginning
        }

        saveTasks();
        closeModal();
    });

    // Filters and Search listeners
    searchInput.addEventListener('input', renderTasks);
    filterStatus.addEventListener('change', renderTasks);
    filterPriority.addEventListener('change', renderTasks);

    clearAllBtn.addEventListener('click', () => {
        const completedTasks = tasks.filter(t => t.status === 'completed');
        if (completedTasks.length > 0) {
            if (confirm(`Hapus ${completedTasks.length} task yang sudah selesai?`)) {
                tasks = tasks.filter(t => t.status !== 'completed');
                saveTasks();
            }
        } else {
            alert('Tidak ada task yang sudah selesai.');
        }
    });

    // Initial render
    renderTasks();
});
