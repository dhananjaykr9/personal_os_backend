from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

class HabitBase(BaseModel):
    habit_name: str
    frequency: Optional[str] = "daily"
    streak: Optional[int] = 0

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    habit_name: Optional[str] = None
    frequency: Optional[str] = None
    streak: Optional[int] = None

class Habit(HabitBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

