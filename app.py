from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "./kbo.db"

def load_games_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, date, time, team1, team2, gamecenter_url, stadium,
           score_team1, score_team2, winner
    FROM games
    """)
    rows = cursor.fetchall()

    conn.close()

    games = []
    for r in rows:
        games.append({
            "id": r[0],
            "date": r[1],
            "time": r[2],
            "team1": r[3],
            "score_team1": r[7],
            "score_team2": r[8],
            "team2": r[4],
            "winner": r[9],
            "gamecenter_url": r[5],
            "stadium": r[6]
        })

    return games

@app.route("/")
def index():
    games = load_games_from_db()
    return render_template("index.html", games=games)


@app.route("/review/<int:game_id>")
def review_page(game_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 경기 정보 가져오기
    cursor.execute("""
        SELECT team1, team2, score_team1, score_team2, winner
        FROM games WHERE id = ?
    """, (game_id,))
    row = cursor.fetchone()

    game_info = {
        "team1": row[0],
        "team2": row[1],
        "score_team1": row[2],
        "score_team2": row[3],
        "winner": row[4],
    }

    # 팀1 타자 기록
    cursor.execute("""
        SELECT player_name, at_bats, hits, rbi, run, avg
        FROM batting WHERE game_id = ? AND team = ?
    """, (game_id, row[0]))
    rows_team1 = cursor.fetchall()

    
    batters_team1 = []
    for r in rows_team1:
        batters_team1.append({
            "player_name": r[0],
            "at_bats": r[1],
            "hits": r[2],
            "rbi": r[3],
            "run": r[4],
            "avg": r[5],
        })

    # 팀2 타자 기록
    cursor.execute("""
        SELECT player_name, at_bats, hits, rbi, run, avg
        FROM batting WHERE game_id = ? AND team = ?
    """, (game_id, row[1]))
    rows_team2 = cursor.fetchall()

    batters_team2 = []
    for r in rows_team2:
        batters_team2.append({
            "player_name": r[0],
            "at_bats": r[1],
            "hits": r[2],
            "rbi": r[3],
            "run": r[4],
            "avg": r[5],
        })

    conn.close()

    return render_template(
        "review.html",
        game_id=game_id,
        game_info=game_info,
        batters_team1=batters_team1,
        batters_team2=batters_team2
    )

if __name__ == "__main__":
    app.run(debug=True)