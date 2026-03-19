import sqlite3
import os

db_path = r'd:\VNIT\personal_life_os\backend\database.db'

def update_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE learning_topics ADD COLUMN syllabus JSON")
        print("Added syllabus to learning_topics")
    except sqlite3.OperationalError as e:
        print(f"Skipping learning_topics: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
