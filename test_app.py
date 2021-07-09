from flask.json import jsonify
from boggle import BoggleGame
from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form id="newWordForm">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            game_json = response.get_json()

            self.assertIsInstance(game_json["gameId"], str)
            self.assertIsInstance(game_json["board"], list)
            self.assertIsInstance(games[game_json["gameId"]], BoggleGame)

    def test_score_word(self):
        """Test if a word is in the word_list on on the board"""

        with self.client as client:
            new_game_response = client.get('/api/new-game')
            new_game_json = new_game_response.get_json()
            gameId = new_game_json["gameId"]
            games[gameId].board = [["C", "A", "T", "X", "Z"],
                                    ["X", "X", "Z", "X", "X"],
                                    ["Y", "Z", "X"," Z", "Y"],
                                    ["X", "X", "Z", "X", "X"],
                                    ["Y", "Z", "X"," Z", "Y"]]

            score_word_response0 = client.post('/api/score-word', json={
                                            "gameId" : gameId,
                                            "word" : "HELLO"})
            score_word_response1 = client.post('/api/score-word', json={
                                            "gameId" : gameId,
                                            "word" : "CAT"})
            score_word_response2 = client.post('/api/score-word', json={
                                            "gameId" : gameId,
                                            "word" : "XXZ"})

            self.assertEqual(score_word_response0.json, {"result": "not-on-board"})
            self.assertEqual(score_word_response1.json, {"result": "ok"})
            self.assertEqual(score_word_response2.json, {"result": "not-word"})


            
            
            
