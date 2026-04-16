"""Modul penyimpanan data menggunakan JSON."""
import json
import os
from typing import List
from models import Task


class TaskStorage:
    """Menyimpan dan mengelola data task dalam file JSON."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self._load()
    
    def _load(self):
        """Load data dari file JSON."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
                self.next_id = 1
    
    def _save(self):
        """Simpan data ke file JSON."""
        data = {
            'tasks': [t.to_dict() for t in self.tasks],
            'next_id': self.next_id
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add(self, task: Task) -> Task:
        """Tambah task baru."""
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self._save()
        return task
    
    def get_all(self) -> List[Task]:
        """Ambil semua task."""
        return self.tasks.copy()
    
    def get_by_id(self, task_id: int) -> Task | None:
        """Ambil task berdasarkan ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update(self, task_id: int, **kwargs) -> bool:
        """Update task berdasarkan ID."""
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self._save()
        return True
    
    def delete(self, task_id: int) -> bool:
        """Hapus task berdasarkan ID."""
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self._save()
        return True
    
    def filter_by_status(self, status: str) -> List[Task]:
        """Filter task berdasarkan status."""
        return [t for t in self.tasks if t.status == status]
    
    def filter_by_priority(self, priority: str) -> List[Task]:
        """Filter task berdasarkan priority."""
        return [t for t in self.tasks if t.priority == priority]
