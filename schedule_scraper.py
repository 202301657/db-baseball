import requests
from bs4 import BeautifulSoup
import sqlite3

URL = "https://www.koreabaseball.com/Schedule/Schedule.aspx"

def insert_game(data):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO game_schedule
        (game_date, game_time, team1, team2, score, gamecenter_url, stadium)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def scrape_schedule():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    
    rows = soup.select("table tbody tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 7:
            continue

        date = cols[0].text.strip()
        time = cols[1].text.strip()
        game = cols[2].text.strip().split("vs")
        score_raw = cols[2].text.strip()

        team1 = game[0].strip()
        team2 = game[1].strip()

        # score 추출 (예: "4 vs 3")
        score = score_raw[score_raw.find(team1) + len(team1):].strip()

        gamecenter_link = "https://www.koreabaseball.com" + cols[3].find("a")["href"]
        stadium = cols[6].text.strip()

        insert_game((date, time, team1, team2, score, gamecenter_link, stadium))

scrape_schedule()
