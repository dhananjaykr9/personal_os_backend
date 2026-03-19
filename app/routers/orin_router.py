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

    # 6a. Music Commands (Phase 55 Integration)
    music_triggers = ["play ", "listen to ", "play song ", "song named "]
    if any(t in msg for t in music_triggers):
        # Extract query: remove the trigger phrase
        query = msg
        for t in music_triggers:
            if t in msg:
                query = msg.split(t)[-1].strip()
                break
        
        if query:
            try:
                # Reuse the high-resilience search logic
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
                print(f"DEBUG: Voice Search Error: {str(e)}")
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
        (["terminal", "console", "kernel"], "/terminal"),
        (["setting", "settings", "config", "configuration"], "/settings"),
    ]

    for keywords, path in nav_map:
        if any(k in msg for k in keywords):
            if is_nav_command or any(k in msg for k in keywords):  # navigate on keyword match
                actions.append({"type": "navigate", "path": path})
                break

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
                print(f"DEBUG: Trying Invidious search -> {instance}")
                res = await client.get(url, params=params, timeout=6.0)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"DEBUG: Invidious Success -> {instance}")
                        return data
                print(f"DEBUG: Invidious Fail ({res.status_code}) -> {instance}")
            except Exception as e:
                print(f"DEBUG: Invidious Error ({str(e)}) -> {instance}")
                continue

        # 2. Fallback to Piped Instances
        print("DEBUG: Falling back to Piped APIs...")
        piped_instances = [
            "https://pipedapi.kavin.rocks",
            "https://api.piped.vic.au",
            "https://piped-api.lunar.icu",
            "https://pipedapi.tokhmi.xyz",
            "https://pipedapi.drgns.space",
            "https://pipedapi.oxit.at",
            "https://api.piped.privacydev.net"
        ]
        for instance in piped_instances:
            try:
                url = f"{instance}/search"
                params = {"q": q, "filter": "videos"}
                print(f"DEBUG: Trying Piped search -> {instance}")
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
                        print(f"DEBUG: Piped Success -> {instance}")
                        return results
                print(f"DEBUG: Piped Fail ({res.status_code}) -> {instance}")
            except Exception as e:
                print(f"DEBUG: Piped Error ({str(e)}) -> {instance}")
                continue

        # 3. Ultimate Fallback: Direct YouTube Scrape (Residential IP)
        print("DEBUG: Falling back to Direct YouTube Scrape...")
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
                        try:
                            contents = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["expandableTabRenderer"]["content"]["sectionListRenderer"]["contents"]
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
                        print("DEBUG: Direct Scrape Success")
                        return results
                print("DEBUG: Direct Scrape Fail (Structure mismatch)")
        except Exception as e:
            print(f"DEBUG: Direct Scrape Error ({str(e)})")

    raise HTTPException(status_code=503, detail="Audio nodes unresponsive. YouTube is currently restricting automated access.")

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

        # 3. Piped Fallback
        piped_instances = [
            "https://pipedapi.kavin.rocks",
            "https://api.piped.vic.au",
            "https://piped-api.lunar.icu"
        ]
        for instance in piped_instances:
            try:
                url = f"{instance}/streams/{video_id}"
                res = await client.get(url, timeout=5.0)
                if res.status_code == 200:
                    data = res.json()
                    return {
                        "videoId": video_id,
                        "title": data.get("title"),
                        "author": data.get("uploader"),
                        "lengthSeconds": data.get("duration", 0),
                        "videoThumbnails": [{"url": data.get("thumbnailUrl")}]
                    }
            except Exception:
                continue
                
    raise HTTPException(status_code=404, detail="Metadata unavailable for this video stream.")
