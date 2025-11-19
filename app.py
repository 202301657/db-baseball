from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def schedule():
    conn = get_db()
    games = conn.execute("SELECT * FROM game_schedule ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("schedule.html", games=games)

@app.route("/review/<int:game_id>")
def review(game_id):
    conn = get_db()
    game = conn.execute("SELECT * FROM game_schedule WHERE id=?", (game_id,)).fetchone()
    batting = conn.execute("SELECT * FROM batting_stats WHERE game_id=?", (game_id,)).fetchall()
    pitching = conn.execute("SELECT * FROM pitching_stats WHERE game_id=?", (game_id,)).fetchall()
    conn.close()

    return render_template("review.html",
                           game=game,
                           batting=batting,
                           pitching=pitching)
    
if __name__ == "__main__":
    app.run(debug=True)
