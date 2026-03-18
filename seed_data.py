import requests
import uuid
from datetime import datetime, date, timedelta

BASE_URL = "http://localhost:8000/api"

def populate():
    # Tasks
    tasks = [
        {"title": "Implement ETL pipeline", "description": "Use Python and SQL", "priority": "high", "due_date": str(date.today()), "category": "work"},
        {"title": "Learn Window Functions", "description": "Practice ranking and offsets", "priority": "medium", "due_date": str(date.today() + timedelta(days=1)), "category": "learning"},
        {"title": "Design Database Schema", "description": "Life OS core tables", "priority": "high", "due_date": str(date.today() - timedelta(days=1)), "category": "project"}
    ]
    for t in tasks: requests.post(f"{BASE_URL}/tasks/", json=t)

    # Learning
    topics = [
        {"topic": "Apache Airflow", "category": "Data Engineering", "completion_percentage": 45, "hours_spent": 12.5, "status": "learning"},
        {"topic": "PostgreSQL Performance", "category": "Database", "completion_percentage": 80, "hours_spent": 20.0, "status": "learning"}
    ]
    for t in topics: requests.post(f"{BASE_URL}/learning/", json=t)

    # Roadmap
    skills = [
        {"skill_name": "SQL Window Functions", "category": "SQL", "difficulty": "intermediate", "status": "completed"},
        {"skill_name": "Spark Optimization", "category": "Data Engineering", "difficulty": "advanced", "status": "not_started"},
        {"skill_name": "Docker for DE", "category": "Cloud", "difficulty": "basic", "status": "learning"}
    ]
    for s in skills: requests.post(f"{BASE_URL}/roadmap/", json=s)

    # Habits
    habits = [
        {"habit_name": "Coding", "frequency": "daily", "streak": 15},
        {"habit_name": "Reading DE Blogs", "frequency": "daily", "streak": 8}
    ]
    for h in habits: requests.post(f"{BASE_URL}/habits/", json=h)

    # Notes
    notes = [
        {"title": "ETL Best Practices", "category": "Engineering", "content": "Always validate source data before transformation..."},
        {"title": "Python for Data", "category": "Python", "content": "Use pandas for small datasets, spark for large ones."}
    ]
    for n in notes: requests.post(f"{BASE_URL}/notes/", json=n)

if __name__ == "__main__":
    populate()
