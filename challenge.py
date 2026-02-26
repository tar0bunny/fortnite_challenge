import json
import random
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, send_file

COMBAT_PATH  = "./challenges/combat.json"
DROP_PATH    = "./challenges/drop.json"
LOADOUT_PATH = "./challenges/loadout.json"
COMMUNITY_PATH = "./challenges/community.json"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "stats.db"
HTML_PATH    = "./templates/index.html"

app = Flask(__name__)

# HELPERS
def build_challenge_list(path):
    with open(path) as f:
        return json.load(f)["challenges"]


def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            wins INTEGER NOT NULL,
            losses INTEGER NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM stats")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO stats (wins, losses) VALUES (0, 0)")

    conn.commit()
    conn.close()


def load_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT wins, losses FROM stats WHERE id = 1")
    wins, losses = cur.fetchone()

    conn.close()
    return {"wins": wins, "losses": losses}


# ROUTES
@app.route("/")
def index():
    return send_file(HTML_PATH)


@app.route("/data")
def data():
    """Sends challenge + stats to the page on load."""
    all_challenges = (
        build_challenge_list(COMBAT_PATH)
        + build_challenge_list(DROP_PATH)
        + build_challenge_list(LOADOUT_PATH)
        + build_challenge_list(COMMUNITY_PATH)
    )
    challenge = random.choice(all_challenges)
    stats = load_stats()
    return jsonify({
        "category":   challenge["id"],
        "text":       challenge["text"],
        "difficulty": challenge["difficulty"],
        "wins":       stats["wins"],
        "losses":     stats["losses"],
    })


@app.route("/result", methods=["POST"])
def result():
    body = request.get_json()
    outcome = body.get("result")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if outcome == "y":
        cur.execute("UPDATE stats SET wins = wins + 1 WHERE id = 1")
    elif outcome == "n":
        cur.execute("UPDATE stats SET losses = losses + 1 WHERE id = 1")

    conn.commit()

    cur.execute("SELECT wins, losses FROM stats WHERE id = 1")
    wins, losses = cur.fetchone()

    conn.close()

    return jsonify({"wins": wins, "losses": losses})


# MAIN
init_db()
if __name__ == "__main__":
    app.run()