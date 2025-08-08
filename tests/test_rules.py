import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.uno.game import Game
from src.uno.card import Card, Color, CardType

# Helper function to set up a game with a predictable state
def setup_game_for_testing(num_players=2):
    player_names = [f"Player {i+1}" for i in range(num_players)]
    # We create a game, but we will manually override hands and discard pile
    game = Game(player_names)
    game.deck.cards = [] # Clear the deck to control card drawing
    for p in game.players:
        p.hand = [] # Clear hands
    game.discard_pile = []
    return game

def test_skip_card_effect():
    game = setup_game_for_testing(3)
    player1 = game.players[0]

    game.current_player_index = 0
    game.discard_pile.append(Card(Color.RED, CardType.NUMBER, 1))
    game.current_color = Color.RED
    player1.hand.append(Card(Color.RED, CardType.SKIP))

    game.play_turn(card_index=0)

    # Player 1 played, Player 2 was skipped, should now be Player 3's turn (index 2)
    assert game.current_player_index == 2

def test_reverse_card_effect_three_players():
    game = setup_game_for_testing(3)
    player1 = game.players[0]

    game.current_player_index = 0
    game.game_direction = 1 # Clockwise
    game.discard_pile.append(Card(Color.BLUE, CardType.NUMBER, 1))
    game.current_color = Color.BLUE
    player1.hand.append(Card(Color.BLUE, CardType.REVERSE))

    game.play_turn(card_index=0)

    assert game.game_direction == -1
    # Turn moves from P1 (idx 0) backwards to P3 (idx 2)
    assert game.current_player_index == 2

def test_reverse_card_effect_two_players():
    game = setup_game_for_testing(2)
    player1 = game.players[0]

    game.current_player_index = 0
    game.discard_pile.append(Card(Color.GREEN, CardType.NUMBER, 1))
    game.current_color = Color.GREEN
    player1.hand.append(Card(Color.GREEN, CardType.REVERSE))

    game.play_turn(card_index=0)

    # In a 2-player game, reverse acts like a skip, so it's the same player's turn
    assert game.current_player_index == 0

def test_draw_two_effect():
    game = setup_game_for_testing(2)
    player1 = game.players[0]
    player2 = game.players[1]

    game.deck.cards.extend([Card(Color.RED, CardType.NUMBER, 1), Card(Color.BLUE, CardType.NUMBER, 2)])
    game.current_player_index = 0
    game.discard_pile.append(Card(Color.YELLOW, CardType.NUMBER, 5))
    game.current_color = Color.YELLOW
    player1.hand.append(Card(Color.YELLOW, CardType.DRAW_TWO))

    game.play_turn(card_index=0)

    # Player 2 should have drawn 2 cards
    assert len(player2.hand) == 2
    # Player 2's turn is skipped, so it's Player 1's turn again
    assert game.current_player_index == 0

def test_wild_draw_four_illegal_play():
    game = setup_game_for_testing(2)
    player1 = game.players[0]

    game.current_player_index = 0
    game.discard_pile.append(Card(Color.RED, CardType.NUMBER, 5))
    game.current_color = Color.RED

    # Player 1 has a Red card, so playing Wild Draw Four should be illegal
    player1.hand = [
        Card(Color.WILD, CardType.WILD_DRAW_FOUR),
        Card(Color.RED, CardType.NUMBER, 7)
    ]

    with pytest.raises(ValueError, match="Cannot play Wild Draw Four"):
        game.play_turn(card_index=0, chosen_color=Color.BLUE)

def test_uno_penalty_is_applied():
    game = setup_game_for_testing(2)
    player1 = game.players[0]
    player2 = game.players[1]

    game.deck.cards.extend([Card(Color.RED, CardType.NUMBER, 8), Card(Color.BLUE, CardType.NUMBER, 9)])
    game.current_player_index = 0
    game.discard_pile.append(Card(Color.GREEN, CardType.NUMBER, 5))
    game.current_color = Color.GREEN

    # P1 has two cards. Will play one and not call UNO.
    player1.hand.extend([Card(Color.GREEN, CardType.NUMBER, 1), Card(Color.GREEN, CardType.NUMBER, 2)])

    # P1 plays a card, leaving them with one, but doesn't call UNO
    game.play_turn(card_index=0, called_uno=False)

    # It is now P2's turn.
    assert game.current_player_index == 1
    assert len(player1.hand) == 1

    # P2 takes their turn (drawing a card), which should trigger the penalty check for P1.
    game.play_turn(card_index=None)

    # P1 should now have 3 cards (1 + 2 penalty)
    assert len(player1.hand) == 3
