import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.uno.game import Game

def test_game_creation():
    player_names = ["Player 1", "Player 2", "Player 3"]
    game = Game(player_names)
    assert len(game.players) == 3
    assert game.players[0].name == "Player 1"
    assert game.players[1].name == "Player 2"
    assert game.players[2].name == "Player 3"

def test_initial_deal():
    player_names = ["Player 1", "Player 2"]
    game = Game(player_names)
    for player in game.players:
        assert len(player.hand) == 7

    # 108 total cards - (2 players * 7 cards) - 1 discard pile card = 93
    assert len(game.deck) == 93
    assert len(game.discard_pile) == 1
