from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_PATH = "kbo.db"


# ✅ 경기 리스트 로드 (검색 포함)
def load_games_from_db(search=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT id, date, time, team1, team2, gamecenter_url, stadium,
                   score_team1, score_team2, winner
            FROM games
            WHERE team1 LIKE ?
               OR team2 LIKE ?
               OR date LIKE ?
               OR stadium LIKE ?
        """, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
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
            "team2": r[4],
            "score_team1": r[7],
            "score_team2": r[8],
            "winner": r[9],
            "gamecenter_url": r[5],
            "stadium": r[6]
        })

    return games


# ✅ 메인 페이지 (경기 리스트 + 검색)
@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    games = load_games_from_db(search)
    return render_template("index.html", games=games, search=search)


# ✅ 리뷰 페이지
@app.route("/review/<int:game_id>")
def review_page(game_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ 경기 정보
    cursor.execute("""
        SELECT team1, team2, score_team1, score_team2, winner
        FROM games
        WHERE id = ?
    """, (game_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return "해당 경기 데이터가 없습니다."

    team1_name = row[0]
    team2_name = row[1]

    game_info = {
        "team1": team1_name,
        "team2": team2_name,
        "score_team1": row[2],
        "score_team2": row[3],
        "winner": row[4]
    }

    # ✅ 팀 기록 (team_stats 테이블에서 직접 로드)
    cursor.execute("""
        SELECT team, hits, home_runs, avg, strikeouts,
               stolen_bases, errors, double_plays,
               left_on_base, walks
        FROM team_stats
        WHERE game_id = ?
    """, (game_id,))

    rows = cursor.fetchall()

    team_stats = {}
    for r in rows:
        team_stats[r[0]] = {
            "hits": r[1],
            "home_runs": r[2],
            "avg": r[3],
            "strikeouts": r[4],
            "stolen_bases": r[5],
            "errors": r[6],
            "double_plays": r[7],
            "left_on_base": r[8],
            "walks": r[9]
        }

    # review.html에서 team_stats.team1 / team_stats.team2 형태로 쓰기 위함
    team_stats = {
        "team1": team_stats.get(team1_name, {}),
        "team2": team_stats.get(team2_name, {})
    }

    # ✅ 팀1 타자 기록
    cursor.execute("""
        SELECT player_name, at_bats, hits, rbi, run, avg
        FROM batting
        WHERE game_id = ? AND team = ?
        ORDER BY id ASC
    """, (game_id, team1_name))

    batters_team1 = [
        {
            "player_name": r[0],
            "at_bats": r[1],
            "hits": r[2],
            "rbi": r[3],
            "run": r[4],
            "avg": r[5]
        }
        for r in cursor.fetchall()
    ]

    # ✅ 팀2 타자 기록
    cursor.execute("""
        SELECT player_name, at_bats, hits, rbi, run, avg
        FROM batting
        WHERE game_id = ? AND team = ?
        ORDER BY id ASC
    """, (game_id, team2_name))

    batters_team2 = [
        {
            "player_name": r[0],
            "at_bats": r[1],
            "hits": r[2],
            "rbi": r[3],
            "run": r[4],
            "avg": r[5]
        }
        for r in cursor.fetchall()
    ]

    conn.close()

    return render_template(
        "review.html",
        game_id=game_id,
        game_info=game_info,
        team_stats=team_stats,
        batters_team1=batters_team1,
        batters_team2=batters_team2
    )


# ✅ 서버 실행
if __name__ == "__main__":
    app.run(debug=True)
