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
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_system_context(db: Session):
    """Fetch current system state for LLM context."""
    tasks = db.query(task_model.TaskModel).filter(task_model.TaskModel.status != 'completed').all()
    habits = db.query(habit_model.HabitModel).all()
    
    task_list = [f"- {t.title} (Priority: {t.priority})" for t in tasks[:10]]
    habit_list = [f"- {h.name} (Streak: {h.streak})" for h in habits]
    
    context = f"""
Current System Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
User: Dhananjay Kharkar (System Architect)
Clearance Level: Admin Alpha

Operational Summary:
- Active Tactical Objectives: {len(tasks)}
- Core Habit Streaks: {sum(h.streak for h in habits) if habits else 0}

Neural Nodes (Tasks):
{chr(10).join(task_list) if task_list else "- System clear: No pending objectives."}

Biological Sync (Habits):
{chr(10).join(habit_list) if habit_list else "- Sync active: No habits logged."}
"""
    return context

@router.post("/chat", response_model=conversation_schema.OrinResponse)
async def orin_chat(request: conversation_schema.OrinRequest, db: Session = Depends(get_db)):
    # 1. Check API Key
    api_key = settings.GROQ_API_KEY or os.environ.get("GROQ_API_KEY", "")
    if not api_key or api_key.strip() == "":
        response_text = f"I am receiving your command: '{request.message}'. However, my cognitive uplink (Groq API) is not configured. Please set GROQ_API_KEY in the .env file."
        return {"response": response_text, "actions": []}

    # 2. Get Past Memory
    history = db.query(conversation_model.ConversationModel).order_by(conversation_model.ConversationModel.timestamp.desc()).limit(5).all()
    history = history[::-1]  # Chronological order
    
    # 3. Build Prompt
    system_context = get_system_context(db)
    messages = [
        {"role": "system", "content": f"""You are Orin, the intelligence core embedded in Dhananjay Kharkar's personal OS. Rules you MUST follow:
1. BREVITY IS LAW: Respond in 1-2 sentences MAXIMUM. Never exceed 30 words. No lists, no elaboration.
2. DIRECT ANSWERS ONLY: Answer exactly what was asked. Nothing more.
3. PERSONA: You are a silent, efficient AI system. Address the user as 'Chief' only when greeting.
4. NAVIGATION: If the user says 'go to', 'open', 'show me', 'navigate to' any page - acknowledge with 1 short sentence.
5. NO UNSOLICITED INFO: Never volunteer data not asked for.

System telemetry (use ONLY if directly asked):
{system_context}"""}
    ]
    
    for h in history:
        messages.append({"role": h.role, "content": h.content})
        
    messages.append({"role": "user", "content": request.message})
    
    # 4. Call Groq API
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30.0
            )
            
            if res.status_code != 200:
                error_body = res.text
                logger.error(f"Groq API returned {res.status_code}: {error_body}")
                raise HTTPException(status_code=500, detail=f"Groq API error {res.status_code}: {error_body[:200]}")
            
            data = res.json()
            response_text = data["choices"][0]["message"]["content"]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Orin cognitive uplink failure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cognitive uplink failure: {str(e)}")

    # 5. Persist to Memory
    try:
        user_msg = conversation_model.ConversationModel(role="user", content=request.message)
        orin_msg = conversation_model.ConversationModel(role="assistant", content=response_text)
        db.add(user_msg)
        db.add(orin_msg)
        db.commit()
    except Exception as e:
        logger.warning(f"Failed to persist conversation: {str(e)}")
    
    # 6. Action Detection - Comprehensive Navigation Map
    actions = []
    msg = request.message.lower()

    # Navigation trigger keywords
    nav_triggers = ["go to", "open", "show", "navigate", "take me", "switch to", "load"]
    is_nav_command = any(t in msg for t in nav_triggers)

    nav_map = [
        (["dashboard", "home", "main"], "/"),
        (["task", "tasks", "objective", "objectives", "to do", "todo"], "/tasks"),
        (["habit", "habits", "streak", "bio-sync"], "/habits"),
        (["note", "notes", "insight", "archive"], "/notes"),
        (["learn", "learning", "skill", "skills", "knowledge"], "/learning"),
        (["road", "roadmap", "milestone", "milestones", "timeline"], "/roadmap"),
        (["analytic", "analytics", "stats", "statistics", "report"], "/analytics"),
        (["terminal", "console", "kernel"], "/terminal"),
        (["setting", "settings", "config", "configuration"], "/settings"),
    ]

    for keywords, path in nav_map:
        if any(k in msg for k in keywords):
            if is_nav_command or any(k in msg for k in keywords):  # navigate on keyword match
                actions.append({"type": "navigate", "path": path})
                break

    return {"response": response_text, "actions": actions}
