from sqlalchemy import Column, String, Float, DateTime, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..database import Base

class LearningLogModel(Base):
    __tablename__ = "learning_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("learning_topics.id"), nullable=True)
    topic_name = Column(String, nullable=False) # Store name directly for simplicity or if topic_id is null
    hours_studied = Column(Float, default=0.0)
    what_learned = Column(Text, nullable=True)
    difficulty = Column(String, default="medium") # easy, medium, hard
    log_date = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)
