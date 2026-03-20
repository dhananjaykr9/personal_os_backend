from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import learning_model
from ..schemas import learning_schema

router = APIRouter()

@router.post("/", response_model=learning_schema.LearningTopic)
def create_topic(topic: learning_schema.LearningTopicCreate, db: Session = Depends(get_db)):
    # Check for existing topic
    existing = db.query(learning_model.LearningTopicModel).filter(learning_model.LearningTopicModel.topic == topic.topic).first()
    if existing:
        # Update existing topic's syllabus if provided
        if topic.syllabus:
            existing.syllabus = topic.syllabus
            db.commit()
            db.refresh(existing)
        return existing
        
    db_topic = learning_model.LearningTopicModel(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.get("/", response_model=List[learning_schema.LearningTopic])
def read_topics(db: Session = Depends(get_db)):
    return db.query(learning_model.LearningTopicModel).all()

@router.patch("/{topic_id}/progress", response_model=learning_schema.LearningTopic)
def update_progress(topic_id: UUID, progress: learning_schema.LearningTopicUpdate, db: Session = Depends(get_db)):
    db_topic = db.query(learning_model.LearningTopicModel).filter(learning_model.LearningTopicModel.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    update_data = progress.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_topic, key, value)
    
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.delete("/{topic_id}")
def delete_topic(topic_id: UUID, db: Session = Depends(get_db)):
    db_topic = db.query(learning_model.LearningTopicModel).filter(learning_model.LearningTopicModel.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db.delete(db_topic)
    db.commit()
    return {"message": "Topic deleted successfully"}
