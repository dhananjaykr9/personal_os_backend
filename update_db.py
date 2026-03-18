import sqlite3
import os

db_path = r'd:\VNIT\personal_life_os\backend\database.db'

def update_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE learning_topics ADD COLUMN last_studied_at DATETIME")
        print("Added last_studied_at to learning_topics")
    except sqlite3.OperationalError as e:
        print(f"Skipping learning_topics: {e}")

    try:
        cursor.execute("ALTER TABLE roadmap_skills ADD COLUMN importance VARCHAR DEFAULT 'medium'")
        print("Added importance to roadmap_skills")
    except sqlite3.OperationalError as e:
        print(f"Skipping roadmap_skills: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
