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


def get_user_ip():
    # Handles proxies/load balancers (e.g. if behind nginx)
    return request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()


def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_ip TEXT NOT NULL UNIQUE,
            wins INTEGER NOT NULL DEFAULT 0,
            losses INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def load_stats(user_ip):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT wins, losses FROM stats WHERE user_ip = ?", (user_ip,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {"wins": 0, "losses": 0}
    return {"wins": row[0], "losses": row[1]}


# ROUTES
@app.route("/")
def index():
    return send_file(HTML_PATH)


@app.route("/data")
def data():
    all_challenges = (
        build_challenge_list(COMBAT_PATH)
        + build_challenge_list(DROP_PATH)
        + build_challenge_list(LOADOUT_PATH)
        + build_challenge_list(COMMUNITY_PATH)
    )
    challenge = random.choice(all_challenges)
    stats = load_stats(get_user_ip())
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
    user_ip = get_user_ip()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create row for this user if it doesn't exist
    cur.execute("""
        INSERT INTO stats (user_ip, wins, losses)
        VALUES (?, 0, 0)
        ON CONFLICT(user_ip) DO NOTHING
    """, (user_ip,))

    if outcome == "y":
        cur.execute("UPDATE stats SET wins = wins + 1 WHERE user_ip = ?", (user_ip,))
    elif outcome == "n":
        cur.execute("UPDATE stats SET losses = losses + 1 WHERE user_ip = ?", (user_ip,))

    conn.commit()

    cur.execute("SELECT wins, losses FROM stats WHERE user_ip = ?", (user_ip,))
    wins, losses = cur.fetchone()
    conn.close()

    return jsonify({"wins": wins, "losses": losses})


# MAIN
init_db()
if __name__ == "__main__":
    app.run()