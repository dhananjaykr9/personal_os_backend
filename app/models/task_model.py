from sqlalchemy import Column, String, Date, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium") # low, medium, high
    status = Column(String, default="todo")     # todo, doing, done
    task_type = Column(String, default="personal") # learning, personal, work
    due_date = Column(Date, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
