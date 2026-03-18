from sqlalchemy import Column, String, DateTime, Date, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class MistakeModel(Base):
    __tablename__ = "mistakes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String, nullable=False)
    mistake_content = Column(Text, nullable=False)
    correct_understanding = Column(Text, nullable=True)
    importance = Column(String, default="medium") # low, medium, high
    date = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)
