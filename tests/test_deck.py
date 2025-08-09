from uno.deck import Deck

def test_deck_creation():
    deck = Deck()
    assert len(deck) == 108
