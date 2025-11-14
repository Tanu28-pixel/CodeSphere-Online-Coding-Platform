import sqlite3

# Connect to database (this creates database.db if it doesn't exist)
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# -------- USERS TABLE --------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

# -------- SAVED CODE TABLE --------
cur.execute("""
CREATE TABLE IF NOT EXISTS code_snippets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    language TEXT,
    code TEXT
)
""")

conn.commit()
conn.close()

print("Database setup completed.")