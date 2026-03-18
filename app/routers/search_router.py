from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from ..models import task_model, note_model, habit_model, learning_model, milestone_model

router = APIRouter()

@router.get("/")
def global_search(q: str = "", db: Session = Depends(get_db)):
    if not q or len(q) < 2:
        return []

    results = []
    search_term = f"%{q}%"
    q_lower = q.lower()

    # Static Navigation Routes
    routes = [
        {"title": "Dashboard", "subtitle": "System Overview & Stats", "path": "/", "type": "nav"},
        {"title": "Objectives", "subtitle": "Task Management & Tactical Goals", "path": "/tasks", "type": "nav"},
        {"title": "Habits", "subtitle": "Bio-Sync & Consistency Tracking", "path": "/habits", "type": "nav"},
        {"title": "Roadmap", "subtitle": "Skill Tree & Career Evolution", "path": "/roadmap", "type": "nav"},
        {"title": "Learning", "subtitle": "Daily Study Logs & Research", "path": "/learning", "type": "nav"},
        {"title": "Mistake Registry", "subtitle": "Post-Mortem Analysis", "path": "/learning?tab=mistakes", "type": "nav"},
        {"title": "Neural Notes", "subtitle": "Knowledge Archive", "path": "/notes", "type": "nav"},
        {"title": "Analytics", "subtitle": "System Performance Metrics", "path": "/analytics", "type": "nav"},
        {"title": "Kernel Console", "subtitle": "Low-level System Access", "path": "/terminal", "type": "nav"},
        {"title": "Settings", "subtitle": "System Configuration", "path": "/settings", "type": "nav"},
    ]

    for route in routes:
        if q_lower in route["title"].lower() or q_lower in route["subtitle"].lower():
            results.append({
                "id": route["path"],
                "type": "nav",
                "title": route["title"],
                "subtitle": route["subtitle"],
                "path": route["path"]
            })

    # Search Tasks
    tasks = db.query(task_model.TaskModel).filter(
        task_model.TaskModel.title.ilike(search_term) | 
        task_model.TaskModel.description.ilike(search_term)
    ).limit(5).all()
    for t in tasks:
        results.append({
            "id": str(t.id),
            "type": "task",
            "title": t.title,
            "subtitle": f"Priority: {t.priority} | Status: {t.status}",
            "path": "/tasks"
        })

    # Search Notes
    notes = db.query(note_model.NoteModel).filter(
        note_model.NoteModel.title.ilike(search_term) | 
        note_model.NoteModel.content.ilike(search_term)
    ).limit(5).all()
    for n in notes:
        results.append({
            "id": str(n.id),
            "type": "note",
            "title": n.title,
            "subtitle": f"Category: {n.category}",
            "path": "/notes"
        })

    # Search Habits
    habits = db.query(habit_model.HabitModel).filter(
        habit_model.HabitModel.habit_name.ilike(search_term)
    ).limit(5).all()
    for h in habits:
        results.append({
            "id": str(h.id),
            "type": "habit",
            "title": h.habit_name,
            "subtitle": f"Streak: {h.streak} | {h.frequency}",
            "path": "/habits"
        })

    # Search Learning Topics
    topics = db.query(learning_model.LearningTopicModel).filter(
        learning_model.LearningTopicModel.topic.ilike(search_term)
    ).limit(5).all()
    for lt in topics:
        results.append({
            "id": str(lt.id),
            "type": "learning",
            "title": lt.topic,
            "subtitle": f"Progress: {lt.completion_percentage}% | {lt.status}",
            "path": "/learning"
        })

    # Search Milestones
    milestones = db.query(milestone_model.MilestoneModel).filter(
        milestone_model.MilestoneModel.title.ilike(search_term) |
        milestone_model.MilestoneModel.description.ilike(search_term)
    ).limit(5).all()
    for m in milestones:
        results.append({
            "id": str(m.id),
            "type": "milestone",
            "title": m.title,
            "subtitle": f"Target: {m.target_date}",
            "path": "/roadmap"
        })

    return results
