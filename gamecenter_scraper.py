import requests
from bs4 import BeautifulSoup
import sqlite3

def save_batter(game_id, player, ab, h, hr, rbi):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO batting_stats (game_id, player, ab, h, hr, rbi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (game_id, player, ab, h, hr, rbi))
    conn.commit()
    conn.close()

def save_pitcher(game_id, player, ip, er, so):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pitching_stats (game_id, player, ip, er, so)
        VALUES (?, ?, ?, ?, ?)
    """, (game_id, player, ip, er, so))
    conn.commit()
    conn.close()

def scrape_gamecenter(game_id, url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # 예: 타자 테이블 (사이트 구조 변경되면 수정 필요함)
    batter_rows = soup.select("#tblHitter1 tbody tr")

    for b in batter_rows:
        cols = b.find_all("td")
        if len(cols) < 6:
            continue

        player = cols[0].text.strip()
        ab = int(cols[1].text)
        h = int(cols[2].text)
        hr = int(cols[3].text)
        rbi = int(cols[4].text)

        save_batter(game_id, player, ab, h, hr, rbi)

    # 투수 테이블
    pitcher_rows = soup.select("#tblPitcher1 tbody tr")

    for p in pitcher_rows:
        cols = p.find_all("td")
        if len(cols) < 5:
            continue

        player = cols[0].text.strip()
        ip = cols[1].text
        er = int(cols[2].text)
        so = int(cols[3].text)

        save_pitcher(game_id, player, ip, er, so)
