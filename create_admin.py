import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect(r"C:\Users\HP\Downloads\SIS\SIS\student_info.db")
cur = conn.cursor()

hashed = generate_password_hash("admin123")

cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hashed, "admin"))

conn.commit()
conn.close()

print("Admin user created!")

