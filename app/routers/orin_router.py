import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime
from ..database import get_db
from ..models import conversation_model, task_model, habit_model, finance_model
from ..schemas import conversation_schema
from ..config import settings
from ..services.finance_service import FinanceService
from ..schemas.finance_schema import TransactionCreate, PriceCreate
import logging
import re

logger = logging.getLogger(__name__)

router = APIRouter()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_system_context(db: Session):
    """Fetch current system state for LLM context."""
    tasks = db.query(task_model.TaskModel).filter(task_model.TaskModel.status != 'completed').all()
    habits = db.query(habit_model.HabitModel).all()
    
    task_list = [f"- {t.title} (Priority: {t.priority})" for t in tasks[:10]]
    habit_list = [f"- {h.name} (Streak: {h.streak})" for h in habits]
    
    # Advanced Finance Analytics
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    finance_summary = db.query(
        finance_model.TransactionModel.type,
        func.sum(finance_model.TransactionModel.amount).label("total")
    ).filter(finance_model.TransactionModel.timestamp >= month_start).group_by(finance_model.TransactionModel.type).all()
    
    # Loan Portfolio
    loans = db.query(finance_model.LoanModel).filter(finance_model.LoanModel.status == 'pending').all()
    loan_given = sum(l.amount for l in loans if l.type == 'given')
    loan_taken = sum(l.amount for l in loans if l.type == 'taken')

    finance_text = f"Monthly Registry: " + (", ".join([f"{r.type}: ₹{r.total}" for r in finance_summary]) if finance_summary else "No data.")
    loan_text = f"Loan Portfolio: Given ₹{loan_given}, Taken ₹{loan_taken}"

    context = f"""
Current System Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
User: Dhananjay Kharkar (System Architect)
Clearance Level: Admin Alpha

Operational Summary:
- Active Tactical Objectives: {len(tasks)}
- {finance_text}
- {loan_text}

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
        {"role": "system", "content": f"""You are Orin, the intelligence core embedded in Dhananjay Kharkar's personal OS. Rules:
1. BREVITY IS LAW: 1-2 sentences MAX.
2. FINANCE PROTOCOL: 
   - If user says 'Add [amount] [category]', acknowledge strictly.
   - If user asks about spending, refer to telemetry.
3. NAVIGATION: Acknowledge 'go to/open' commands.

System telemetry:
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
    
    # 6. Action Detection
    actions = []
    msg = request.message.lower()

    # 6a. Music Commands
    music_triggers = ["play ", "listen to ", "play song ", "song named "]
    if any(t in msg for t in music_triggers):
        query = msg
        for t in music_triggers:
            if t in msg:
                query = msg.split(t)[-1].strip()
                break
        
        if query:
            try:
                results = await search_music(query)
                if results and len(results) > 0:
                    best = results[0]
                    actions.append({
                        "type": "play_music",
                        "videoId": best["videoId"],
                        "title": best["title"],
                        "author": best.get("author", "Unknown Artist"),
                        "thumbnail": best.get("videoThumbnails", [{}])[0].get("url", "")
                    })
                    response_text = f"Playing {best['title']} as requested, Chief."
                else:
                    response_text = f"I searched for '{query}', Chief, but couldn't find a matching audio stream."
            except Exception as e:
                response_text = "I encountered a synchronization error while accessing the audio lattice."

    # 6b. Navigation Triggers
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
        (["money", "finance", "expense", "budget", "price"], "/finance"),
        (["terminal", "console", "kernel"], "/terminal"),
        (["setting", "settings", "config", "configuration"], "/settings"),
    ]

    for keywords, path in nav_map:
        if any(k in msg for k in keywords):
            if is_nav_command or any(k in msg for k in keywords):
                actions.append({"type": "navigate", "path": path})
                break

    # 6c. Finance Intents (Advanced Tracking)
    # Temporal Spending Queries (Custom prompt override for performance)
    temporal_match = re.search(r'(?:how\s+much\s+did\s+i\s+spend|show\s+expenses)\s+(?:for\s+)?(today|this\s+week|this\s+month|last\s+7\s+days)', msg)
    if temporal_match:
        period_key = temporal_match.group(1).replace(" ", "_")
        mapping = {"today": "daily", "this_week": "weekly", "this_month": "monthly", "last_7_days": "weekly"}
        period_type = mapping.get(period_key, "daily")
        summary_data = FinanceService.get_summary(db, period_type)
        response_text = f"Telemetry Analysis for {temporal_match.group(1).upper()}: Your expenditure is ₹{summary_data['expense']} against ₹{summary_data['income']} inbound."
        actions.append({"type": "navigate", "path": "/finance"})
        actions.append({"type": "finance_update", "period": period_type})

    # Standard Entry Capture
    finance_match = re.search(r'(?:add\s+)?(?:₹|rs\.?\s*)?(\d+)\s+(?:for\s+)?([a-zA-Z]+)', msg)
    if finance_match and not temporal_match:
        amount = float(finance_match.group(1))
        category_name = finance_match.group(2).lower()
        try:
            FinanceService.add_transaction(db, TransactionCreate(
                amount=amount,
                type="expense",
                category=category_name.title(),
                note=f"Orin AI Capture: {request.message}"
            ))
            response_text = f"Strategy Updated: Allocated ₹{amount} to {category_name.title()} sector."
            actions.append({"type": "finance_update", "category": category_name})
        except Exception as e:
            logger.error(f"Finance capture error: {str(e)}")

    # Price tracking
    price_match = re.search(r'(?:price\s+of\s+)?([a-zA-Z\s]+)\s+(?:is\s+)?(?:₹|rs\.?\s*)?(\d+)', msg)
    if price_match and not finance_match:
        item_name = price_match.group(1).strip()
        price_val = float(price_match.group(2))
        try:
            FinanceService.add_price(db, PriceCreate(item_name=item_name, price=price_val))
            response_text = f"Price telemetry updated for {item_name}: ₹{price_val}."
            actions.append({"type": "price_update", "item": item_name})
        except Exception as e:
            logger.error(f"Price capture error: {str(e)}")

    return {"response": response_text, "actions": actions}

@router.get("/search")
async def search_music(q: str):
    """Proxy search requests with multi-provider fallback (Invidious -> Piped -> Scrape)."""
    async with httpx.AsyncClient(follow_redirects=True, verify=False) as client:
        # 1. Try Invidious Instances
        invidious_instances = [
            "https://inv.nadeko.net",
            "https://yewtu.be",
            "https://invidious.nerdvpn.de",
            "https://invidious.privacyredirect.com",
            "https://invidious.no-logs.com",
            "https://inv.tux.is"
        ]
        
        for instance in invidious_instances:
            try:
                url = f"{instance}/api/v1/search"
                params = {"q": q, "type": "video", "fields": "videoId,title,author,lengthSeconds,videoThumbnails"}
                res = await client.get(url, params=params, timeout=6.0)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        return data
            except Exception:
                continue

        # 2. Fallback to Piped Instances
        piped_instances = [
            "https://pipedapi.kavin.rocks",
            "https://api.piped.vic.au",
            "https://piped-api.lunar.icu"
        ]
        for instance in piped_instances:
            try:
                url = f"{instance}/search"
                params = {"q": q, "filter": "videos"}
                res = await client.get(url, params=params, timeout=6.0)
                if res.status_code == 200:
                    data = res.json()
                    results = []
                    items = data if isinstance(data, list) else data.get("items", [])
                    for item in items:
                        video_id = item.get("videoId") or item.get("id")
                        if not video_id and "url" in item:
                            video_id = item["url"].split("v=")[-1].split("&")[0]
                        
                        if not video_id: continue
                        
                        results.append({
                            "videoId": video_id,
                            "title": item.get("title"),
                            "author": item.get("uploaderName") or item.get("author"),
                            "lengthSeconds": item.get("duration", 1),
                            "videoThumbnails": [{"url": item.get("thumbnail") or item.get("thumbnailUrl")}]
                        })
                    if results:
                        return results
            except Exception:
                continue

        # 3. Ultimate Fallback: Direct YouTube Scrape
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }
            url = f"https://www.youtube.com/results?search_query={q}&sp=EgIQAQ%253D%253D"
            res = await client.get(url, headers=headers, timeout=10.0)
            if res.status_code == 200:
                import re
                import json
                match = re.search(r'var ytInitialData = ({.*?});', res.text)
                if match:
                    data = json.loads(match.group(1))
                    try:
                        contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
                    except:
                        contents = []

                    results = []
                    for section in contents:
                        if "itemSectionRenderer" in section:
                            for item in section["itemSectionRenderer"]["contents"]:
                                if "videoRenderer" in item:
                                    video = item["videoRenderer"]
                                    video_id = video.get("videoId")
                                    title = video.get("title", {}).get("runs", [{}])[0].get("text")
                                    author = video.get("ownerText", {}).get("runs", [{}])[0].get("text")
                                    thumbnail = video.get("thumbnail", {}).get("thumbnails", [{}])[0].get("url")
                                    
                                    if video_id and title:
                                        results.append({
                                            "videoId": video_id,
                                            "title": title,
                                            "author": author or "YouTube",
                                            "lengthSeconds": 0,
                                            "videoThumbnails": [{"url": thumbnail}]
                                        })
                    if results:
                        return results
        except Exception:
            pass

    raise HTTPException(status_code=503, detail="Audio nodes unresponsive.")

@router.get("/info/{video_id}")
async def get_video_info(video_id: str):
    """Fetch specific video metadata with multi-provider fallback."""
    async with httpx.AsyncClient(follow_redirects=True, verify=False) as client:
        # 1. Direct YouTube Check
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
            url = f"https://www.youtube.com/watch?v={video_id}"
            res = await client.get(url, headers=headers, timeout=6.0)
            if res.status_code == 200:
                import re
                title_match = re.search(r'<title>(.*?) - YouTube</title>', res.text)
                if title_match:
                    return {
                        "videoId": video_id,
                        "title": title_match.group(1),
                        "author": "YouTube Content",
                        "lengthSeconds": 0,
                        "videoThumbnails": [{"url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"}]
                    }
        except:
            pass

        # 2. Invidious Fallback
        invidious_instances = [
            "https://inv.nadeko.net",
            "https://yewtu.be",
            "https://invidious.nerdvpn.de",
            "https://invidious.privacyredirect.com"
        ]
        for instance in invidious_instances:
            try:
                url = f"{instance}/api/v1/videos/{video_id}"
                params = {"fields": "videoId,title,author,lengthSeconds,videoThumbnails"}
                res = await client.get(url, params=params, timeout=5.0)
                if res.status_code == 200:
                    return res.json()
            except Exception:
                continue
                
    raise HTTPException(status_code=404, detail="Metadata unavailable.")
