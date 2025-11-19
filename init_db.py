import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS game_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_date TEXT,
    game_time TEXT,
    team1 TEXT,
    team2 TEXT,
    score TEXT,
    gamecenter_url TEXT,
    stadium TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS batting_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player TEXT,
    ab INTEGER,
    h INTEGER,
    hr INTEGER,
    rbi INTEGER,
    FOREIGN KEY(game_id) REFERENCES game_schedule(id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pitching_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player TEXT,
    ip TEXT,
    er INTEGER,
    so INTEGER,
    FOREIGN KEY(game_id) REFERENCES game_schedule(id)
)
""")

conn.commit()
conn.close()

print("DB 초기화 완료!")
