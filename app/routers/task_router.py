from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import task_model
from ..schemas import task_schema

router = APIRouter()

@router.post("/", response_model=task_schema.Task)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    db_task = task_model.TaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[task_schema.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(task_model.TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=task_schema.Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = db.query(task_model.TaskModel).filter(task_model.TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=task_schema.Task)
def update_task(task_id: UUID, task: task_schema.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(task_model.TaskModel).filter(task_model.TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}/status", response_model=task_schema.Task)
def update_task_status(task_id: UUID, status: str, db: Session = Depends(get_db)):
    db_task = db.query(task_model.TaskModel).filter(task_model.TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.status = status
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = db.query(task_model.TaskModel).filter(task_model.TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
