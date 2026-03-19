import sqlite3
db_path = r'd:\VNIT\personal_life_os\backend\database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("--- learning_topics ---")
cursor.execute("PRAGMA table_info(learning_topics)")
print(cursor.fetchall())
print("\n--- roadmap_skills ---")
cursor.execute("PRAGMA table_info(roadmap_skills)")
print(cursor.fetchall())
conn.close()
