"""Model data untuk Task."""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


@dataclass
class Task:
    """Representasi sebuah task/tugas."""
    id: int
    title: str
    description: str = ""
    status: str = "pending"  # pending, in_progress, completed
    priority: str = "medium"  # low, medium, high
    created_at: str = ""
    due_date: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Konversi task ke dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Buat task dari dictionary."""
        return cls(**data)
    
    def __str__(self) -> str:
        status_icon = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅"
        }.get(self.status, "⏳")
        
        priority_icon = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }.get(self.priority, "🟡")
        
        return f"[{self.id}] {status_icon} {priority_icon} {self.title}"
