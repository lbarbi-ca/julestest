from .card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.uno_status = False

    def add_card_to_hand(self, card: Card):
        self.hand.append(card)

    def play_card_from_hand(self, card_index: int) -> Card:
        return self.hand.pop(card_index)

    def __str__(self):
        return f"Player {self.name}"

    def __repr__(self):
        return self.__str__()
