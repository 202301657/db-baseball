from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "kbo.db"

def load_games_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT date, time, team1, team2, gamecenter_url, stadium FROM games")
    rows = cursor.fetchall()
    conn.close()

    games = []
    for r in rows:
        games.append({
            "date": r[0],
            "time": r[1],
            "team1": r[2],
            "team2": r[3],
            "gamecenter_url": r[4],
            "stadium": r[5],
        })

    return games

@app.route("/")
def index():
    games = load_games_from_db()
    return render_template("index.html", games=games)

if __name__ == "__main__":
    app.run(debug=True)
