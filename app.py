from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4()) # uuid is the python universal unique identifier library
    game = BoggleGame()
    games[game_id] = game
    # session['current_game_id'] = game_id
    return {"gameId": game_id, "board": game.board}

@app.route("/api/score-word", methods=["POST"])
def score_word():
    """Check if word is legal, and if so, score the word."""
    # games {} holds our gameId and actual board
    # look for our game by id in games
    # game = games[session['current_game_id']]'
    game_id = request.json["gameId"]
    game = games[game_id]

    # look for word in wordlist
    word = request.json["word"]
    if not game.is_word_in_word_list(word):
        return jsonify({"result": "not-word"})
    
    # call the is it findable on the board function
    if not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})





