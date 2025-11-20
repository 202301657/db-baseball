import sqlite3

conn = sqlite3.connect("kbo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    team1 TEXT,
    team2 TEXT,
    gamecenter_url TEXT,
    stadium TEXT
);
""")

conn.commit()
conn.close()

print("✔ SQLite 데이터베이스 및 테이블 생성 완료")
