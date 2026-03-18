from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "todo"
    task_type: Optional[str] = "personal"
    due_date: Optional[date] = None
    category: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    task_type: Optional[str] = None
    due_date: Optional[date] = None
    category: Optional[str] = None

class Task(TaskBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
