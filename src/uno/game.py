from .deck import Deck
from .player import Player
from .card import Card, Color, CardType

class Game:
    def __init__(self, player_names: list[str]):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.deck.shuffle()
        self.discard_pile = []
        self.current_player_index = 0
        self.game_direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self._deal_initial_cards()
        self._start_discard_pile()

    def _deal_initial_cards(self):
        for _ in range(7):
            for player in self.players:
                player.add_card_to_hand(self.deck.draw_card())

    def _start_discard_pile(self):
        # The first card cannot be a wild +4
        card = self.deck.draw_card()
        while card.card_type == CardType.WILD_DRAW_FOUR:
            self.deck.cards.append(card)
            self.deck.shuffle()
            card = self.deck.draw_card()

        self.discard_pile.append(card)

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + self.game_direction) % len(self.players)

    def is_game_over(self) -> bool:
        for player in self.players:
            if not player.hand:
                return True
        return False

    def get_winner(self) -> Player | None:
        for player in self.players:
            if not player.hand:
                return player
        return None
