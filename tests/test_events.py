import pytest
from unittest.mock import Mock

from uno.game import Game, GameEventType
from uno.card import Card, Color, CardType

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

def test_game_win_event():
    game = setup_game_for_testing(2)
    player1 = game.players[0]

    mock_listener = Mock()
    game.register_listener(GameEventType.GAME_WIN, mock_listener)

    game.current_player_index = 0
    game.discard_pile.append(Card(Color.RED, CardType.NUMBER, 1))
    game.current_color = Color.RED
    player1.hand.append(Card(Color.RED, CardType.NUMBER, 2)) # P1's last card

    game.play_turn(card_index=0)

    mock_listener.assert_called_once()
    mock_listener.assert_called_with(GameEventType.GAME_WIN, winner_index=0)

def test_uno_declared_event():
    game = setup_game_for_testing(2)
    player1 = game.players[0]

    mock_listener = Mock()
    game.register_listener(GameEventType.UNO_DECLARED, mock_listener)

    game.current_player_index = 0
    game.discard_pile.append(Card(Color.BLUE, CardType.NUMBER, 1))
    game.current_color = Color.BLUE
    player1.hand.extend([Card(Color.BLUE, CardType.NUMBER, 2), Card(Color.BLUE, CardType.NUMBER, 3)])

    game.play_turn(card_index=0, called_uno=True)

    mock_listener.assert_called_once()
    mock_listener.assert_called_with(GameEventType.UNO_DECLARED, player_index=0)

def test_get_playable_cards():
    game = setup_game_for_testing(1)
    player1 = game.players[0]

    game.discard_pile.append(Card(Color.RED, CardType.NUMBER, 7))
    game.current_color = Color.RED

    player1.hand = [
        Card(Color.RED, CardType.NUMBER, 1), # Playable (color)
        Card(Color.BLUE, CardType.NUMBER, 7), # Playable (number)
        Card(Color.GREEN, CardType.NUMBER, 3), # Not playable
        Card(Color.WILD, CardType.WILD) # Playable
    ]

    playable_cards = game.get_playable_cards(player1)
    assert playable_cards == [0, 1, 3]

def test_player_must_draw():
    game = setup_game_for_testing(1)
    player1 = game.players[0]

    game.discard_pile.append(Card(Color.RED, CardType.NUMBER, 7))
    game.current_color = Color.RED

    # Hand with no playable cards
    player1.hand = [
        Card(Color.BLUE, CardType.NUMBER, 1),
        Card(Color.GREEN, CardType.SKIP)
    ]
    assert game.player_must_draw(player1) is True

    # Hand with a playable card
    player1.hand.append(Card(Color.RED, CardType.NUMBER, 5))
    assert game.player_must_draw(player1) is False
