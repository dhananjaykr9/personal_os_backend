from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import learning_log_model
from ..schemas import learning_log_schema

router = APIRouter()

@router.post("/", response_model=learning_log_schema.LearningLog)
def create_learning_log(log: learning_log_schema.LearningLogCreate, db: Session = Depends(get_db)):
    db_log = learning_log_model.LearningLogModel(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=List[learning_log_schema.LearningLog])
def read_learning_logs(db: Session = Depends(get_db)):
    return db.query(learning_log_model.LearningLogModel).order_by(learning_log_model.LearningLogModel.log_date.desc()).all()

@router.put("/{log_id}", response_model=learning_log_schema.LearningLog)
def update_learning_log(log_id: UUID, log_update: learning_log_schema.LearningLogUpdate, db: Session = Depends(get_db)):
    db_log = db.query(learning_log_model.LearningLogModel).filter(learning_log_model.LearningLogModel.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    update_data = log_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_log, key, value)
    
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/{log_id}")
def delete_learning_log(log_id: UUID, db: Session = Depends(get_db)):
    db_log = db.query(learning_log_model.LearningLogModel).filter(learning_log_model.LearningLogModel.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db.delete(db_log)
    db.commit()
    return {"message": "Log deleted successfully"}
