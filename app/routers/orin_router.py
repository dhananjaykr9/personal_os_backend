import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from ..database import get_db
from ..models import conversation_model, task_model, habit_model
from ..schemas import conversation_schema
from ..config import settings

router = APIRouter()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_system_context(db: Session):
    """Fetch current system state for LLM context."""
    today = datetime.utcnow().date()
    tasks = db.query(task_model.TaskModel).filter(task_model.TaskModel.status != 'completed').all()
    habits = db.query(habit_model.HabitModel).all()
    
    task_list = [f"- {t.title} (Priority: {t.priority})" for t in tasks[:10]]
    habit_list = [f"- {h.name} (Streak: {h.streak})" for h in habits]
    
    context = f"""
Current System Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
Active Tasks:
{chr(10).join(task_list) if task_list else "None"}

Habit Status:
{chr(10).join(habit_list) if habit_list else "None"}
"""
    return context

@router.post("/chat", response_model=conversation_schema.OrinResponse)
async def orin_chat(request: conversation_schema.OrinRequest, db: Session = Depends(get_db)):
    # 1. Get Past Memory
    history = db.query(conversation_model.ConversationModel).order_by(conversation_model.ConversationModel.timestamp.desc()).limit(5).all()
    history = history[::-1] # Chronological order
    
    # 2. Build Prompt
    system_context = get_system_context(db)
    messages = [
        {"role": "system", "content": f"You are Orin, a smooth, professional, and proactive AI assistant for Dhananjay's Life OS. Your voice is male and resonant. You have access to real-time system data. Keep responses concise and actionable. {system_context}"}
    ]
    
    for h in history:
        messages.append({"role": h.role, "content": h.content})
        
    messages.append({"role": "user", "content": request.message})
    
    # 3. Call Groq
    if not settings.GROQ_API_KEY:
        # Fallback for dev if no key provided
        response_text = f"I am receiving your command: '{request.message}'. However, my cognitive uplink (Groq API) is not configured. Please set GROQ_API_KEY in the environment."
        return {"response": response_text, "actions": []}

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30.0
            )
            res.raise_for_status()
            data = res.json()
            response_text = data["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")

    # 4. Persistence
    user_msg = conversation_model.ConversationModel(role="user", content=request.message)
    orin_msg = conversation_model.ConversationModel(role="assistant", content=response_text)
    db.add(user_msg)
    db.add(orin_msg)
    db.commit()
    
    # 5. TODO: Detect actions (Simplified for now - can be expanded with function calling)
    actions = []
    if "add task" in request.message.lower() or "new task" in request.message.lower():
        actions.append({"type": "navigate", "path": "/tasks", "params": {"auto_open": True}})
    
    return {"response": response_text, "actions": actions}
