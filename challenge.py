import json
import random
import threading
import webbrowser
from pathlib import Path
from flask import Flask, jsonify, request, send_file

COMBAT_PATH  = "./challenges/combat.json"
DROP_PATH    = "./challenges/drop.json"
LOADOUT_PATH = "./challenges/loadout.json"
COMMUNITY_PATH = "./challenges/community.json"
STATS_PATH   = "./stats.json"
HTML_PATH    = "./templates/index.html"

app = Flask(__name__)

# HELPERS
def build_challenge_list(path):
    with open(path) as f:
        return json.load(f)["challenges"]


def load_stats():
    with open(STATS_PATH) as f:
        return json.load(f)


def save_stats(stats):
    with open(STATS_PATH, "w") as f:
        json.dump(stats, f, indent=4)


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
    """Receives win/loss/cancel from the page and saves to stats.json."""
    body = request.get_json()
    outcome = body.get("result")  # "y", "n", or "c"

    stats = load_stats()
    if outcome == "y":
        stats["wins"] += 1
    elif outcome == "n":
        stats["losses"] += 1

    save_stats(stats)
    return jsonify({"wins": stats["wins"], "losses": stats["losses"]})


# MAIN
if __name__ == "__main__":
    threading.Timer(0.8, lambda: webbrowser.open("http://localhost:5000")).start()
    app.run(port=5000)