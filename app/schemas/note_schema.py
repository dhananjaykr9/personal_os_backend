from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class NoteBase(BaseModel):
    title: str
    category: Optional[str] = None
    content: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None

class Note(NoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
