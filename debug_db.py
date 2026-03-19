import sqlite3
db_path = r'd:\VNIT\personal_life_os\backend\database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT topic, syllabus FROM learning_topics")
rows = cursor.fetchall()
for row in rows:
    print(f"Topic: {row[0]} | Syllabus Null? {row[1] is None}")
conn.close()
