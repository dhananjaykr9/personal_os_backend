from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..database import Base

class HabitModel(Base):
    __tablename__ = "habits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_name = Column(String, nullable=False)
    frequency = Column(String, default="daily")
    streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("HabitLogModel", back_populates="habit")

class HabitLogModel(Base):
    __tablename__ = "habit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"))
    completed = Column(Boolean, default=False)
    log_date = Column(Date, default=datetime.utcnow().date)

    habit = relationship("HabitModel", back_populates="logs")

