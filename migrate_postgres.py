import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

def migrate():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Add syllabus column if not exists
        print("Checking for syllabus column in learning_topics...")
        cur.execute("ALTER TABLE learning_topics ADD COLUMN IF NOT EXISTS syllabus JSONB;")
        
        conn.commit()
        print("[OK] Column 'syllabus' added/verified in learning_topics.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[FAIL] Migration error: {e}")

if __name__ == "__main__":
    migrate()
