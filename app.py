from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "kbo.db"

def load_games_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, date, time, team1, team2, gamecenter_url, stadium FROM games")
    rows = cursor.fetchall()
    conn.close()

    games = []
    for r in rows:
        games.append({
            "id": r[0],
            "date": r[1],
            "time": r[2],
            "team1": r[3],
            "team2": r[4],
            "gamecenter_url": r[5],
            "stadium": r[6],
        })

    return games

@app.route("/")
def index():
    games = load_games_from_db()
    return render_template("index.html", games=games)


@app.route("/review/<int:game_id>")
def review_page(game_id):
    # DB에서 해당 경기 타자 기록 불러오기
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_name, at_bats, hits, rbi, run, avg
        FROM batting
        WHERE game_id = ?
    """, (game_id,))

    rows = cursor.fetchall()
    conn.close()

    batters = []
    for r in rows:
        batters.append({
            "player_name": r[0],
            "at_bats": r[1],
            "hits": r[2],
            "rbi": r[3],
            "run": r[4],
            "avg": r[5]
        })

    return render_template("review.html", batters=batters, game_id=game_id)

if __name__ == "__main__":
    app.run(debug=True)