import random
from .card import Card, Color, CardType

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        self.cards = []
        for color in [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]:
            # Add number cards
            self.cards.append(Card(color, CardType.NUMBER, 0))
            for i in range(1, 10):
                self.cards.append(Card(color, CardType.NUMBER, i))
                self.cards.append(Card(color, CardType.NUMBER, i))

            # Add action cards
            for _ in range(2):
                self.cards.append(Card(color, CardType.SKIP))
                self.cards.append(Card(color, CardType.REVERSE))
                self.cards.append(Card(color, CardType.DRAW_TWO))

        # Add wild cards
        for _ in range(4):
            self.cards.append(Card(Color.WILD, CardType.WILD))
            self.cards.append(Card(Color.WILD, CardType.WILD_DRAW_FOUR))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            # In a real game, we would reshuffle the discard pile into the deck
            # For now, we'll raise an exception
            raise DeckEmptyError("Cannot draw a card from an empty deck.")
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)
