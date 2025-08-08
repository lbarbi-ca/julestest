import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.uno.deck import Deck

def test_deck_creation():
    deck = Deck()
    assert len(deck) == 108
