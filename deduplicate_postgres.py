import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def deduplicate():
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("--- Deduplicating learning_topics ---")
        # Keep the one with the most complete syllabus or latest created_at
        # Here we use a common CTE pattern to delete duplicates
        cur.execute("""
            DELETE FROM learning_topics 
            WHERE id NOT IN (
                SELECT id FROM (
                    SELECT id, ROW_NUMBER() OVER (
                        PARTITION BY topic ORDER BY created_at DESC
                    ) as row_num 
                    FROM learning_topics
                ) t WHERE t.row_num = 1
            );
        """)
        print(f"Deleted {cur.rowcount} duplicate topics.")

        print("\n--- Deduplicating roadmap_skills ---")
        cur.execute("""
            DELETE FROM roadmap_skills 
            WHERE id NOT IN (
                SELECT id FROM (
                    SELECT id, ROW_NUMBER() OVER (
                        PARTITION BY skill_name ORDER BY id DESC
                    ) as row_num 
                    FROM roadmap_skills
                ) t WHERE t.row_num = 1
            );
        """)
        print(f"Deleted {cur.rowcount} duplicate skills.")
        
        # Now apply the UNIQUE constraint via ALTER TABLE if not already there
        # Note: In Postgres, we can't easily add UNIQUE IF NOT EXISTS via SQL in one line without a check.
        # But we can try to add it and catch the error or check first.
        
        print("\n--- Applying Unique Constraints ---")
        try:
            cur.execute("ALTER TABLE learning_topics ADD CONSTRAINT unique_topic UNIQUE (topic);")
            print("Constraint 'unique_topic' added.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Constraint 'unique_topic' likely already exists or error: {e}")
            
        try:
            cur.execute("ALTER TABLE roadmap_skills ADD CONSTRAINT unique_skill_name UNIQUE (skill_name);")
            print("Constraint 'unique_skill_name' added.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Constraint 'unique_skill_name' likely already exists or error: {e}")

        conn.commit()
        cur.close()
        conn.close()
        print("\n[SUCCESS] Deduplication and constraint application complete.")

    except Exception as e:
        print(f"[ERROR] Deduplication failed: {e}")

if __name__ == "__main__":
    deduplicate()
