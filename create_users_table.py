import sqlite3


conn = sqlite3.connect(r"C:\Users\HP\Downloads\SIS\SIS\student_info.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);
""")

conn.commit()
conn.close()

print("Users table created successfully!")


