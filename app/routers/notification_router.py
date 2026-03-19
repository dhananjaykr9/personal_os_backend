from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models.notification_model import NotificationModel
from ..schemas.notification_schema import Notification, NotificationCreate

router = APIRouter()

@router.get("/", response_model=List[Notification])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(NotificationModel).order_by(NotificationModel.is_read.asc(), NotificationModel.created_at.desc()).all()

@router.post("/", response_model=Notification)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = NotificationModel(**notification.model_dump())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.put("/{notification_id}/read", response_model=Notification)
def mark_as_read(notification_id: UUID, db: Session = Depends(get_db)):
    db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db_notification.is_read = True
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/")
def clear_notifications(db: Session = Depends(get_db)):
    db.query(NotificationModel).delete()
    db.commit()
    return {"message": "All notifications cleared"}
