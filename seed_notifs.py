import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Add the current directory to sys.path to import from 'app'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from app.database import SessionLocal, engine, Base
    from app.models.notification_model import NotificationModel
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def seed():
    # Base.metadata.create_all(bind=engine) # Should already be created by main.py
    db = SessionLocal()
    try:
        # Clear existing
        db.query(NotificationModel).delete()
        
        notifs = [
            NotificationModel(
                title="Orin Protocol Active",
                message="Cognitive uplink established and synchronized.",
                type="success",
                created_at=datetime.utcnow()
            ),
            NotificationModel(
                title="Habit Streak Alert",
                message="Check in your daily habits to maintain momentum.",
                type="warning",
                created_at=datetime.utcnow()
            ),
            NotificationModel(
                title="Pending Objectives",
                message="3 high-priority tasks are awaiting classification.",
                type="info",
                created_at=datetime.utcnow()
            )
        ]
        db.add_all(notifs)
        db.commit()
        print("Successfully seeded notifications.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
