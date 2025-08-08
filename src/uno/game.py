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
        self.current_color = None
        self._deal_initial_cards()
        self._start_discard_pile()

    def _deal_initial_cards(self):
        for _ in range(7):
            for player in self.players:
                player.add_card_to_hand(self.draw_card_from_deck())

    def _start_discard_pile(self):
        # The first card cannot be a wild card. This is a simplification for now.
        card = self.draw_card_from_deck()
        while card.color == Color.WILD:
            self.deck.cards.append(card) # Put it back in the deck
            self.deck.shuffle()
            card = self.draw_card_from_deck()

        self.discard_pile.append(card)
        self.current_color = card.color

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

    def reshuffle_discard_pile(self):
        """
        Reshuffles the discard pile back into the deck, leaving the top card.
        """
        if len(self.discard_pile) <= 1:
            return

        top_card = self.discard_pile.pop()
        self.deck.cards.extend(self.discard_pile)
        self.deck.shuffle()
        self.discard_pile = [top_card]

    def draw_card_from_deck(self):
        """
        Draws a card from the deck, reshuffling if necessary.
        """
        card = self.deck.draw_card()
        if card is None:
            self.reshuffle_discard_pile()
            card = self.deck.draw_card()
        return card

    def get_top_card(self) -> Card | None:
        return self.discard_pile[-1] if self.discard_pile else None

    def is_card_playable(self, card: Card) -> bool:
        top_card = self.get_top_card()
        if not top_card:
            return True

        if card.color == Color.WILD:
            return True

        if self.current_color:
            if card.color == self.current_color:
                return True

        if top_card.color != Color.WILD:
            if top_card.card_type == CardType.NUMBER and card.card_type == CardType.NUMBER and card.value == top_card.value:
                return True
            if top_card.card_type != CardType.NUMBER and card.card_type == top_card.card_type:
                return True

        return False

    def play_turn(self, card_index: int | None, chosen_color: Color = None, called_uno: bool = False):
        # UNO Penalty Check for the *previous* player
        prev_player_index = (self.current_player_index - self.game_direction + len(self.players)) % len(self.players)
        prev_player = self.players[prev_player_index]
        if len(prev_player.hand) == 1 and not prev_player.uno_status:
            # Player is penalized for not calling UNO
            prev_player.add_card_to_hand(self.draw_card_from_deck())
            prev_player.add_card_to_hand(self.draw_card_from_deck())
            prev_player.uno_status = False  # Status is reset after penalty

        player = self.get_current_player()

        if card_index is not None:
            # --- Logic for PLAYING a card ---
            if card_index < 0 or card_index >= len(player.hand):
                raise IndexError("Invalid card index.")
            card_to_play = player.hand[card_index]
            if not self.is_card_playable(card_to_play):
                raise ValueError("Card is not playable.")
            card_type = card_to_play.card_type
            if card_type == CardType.WILD_DRAW_FOUR:
                if self.current_color is not None:
                    has_matching_color_card = any(c.color == self.current_color for c in player.hand)
                    if has_matching_color_card:
                        raise ValueError("Cannot play Wild Draw Four when you have a card of the current color.")

            # Execute the play
            card = player.play_card_from_hand(card_index)

            # Set UNO status after playing
            if len(player.hand) == 1:
                player.uno_status = called_uno
            else:
                player.uno_status = False # Always reset if not 1 card

            self.discard_pile.append(card)

            # Update color
            if card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]:
                if chosen_color is None or chosen_color == Color.WILD:
                    raise ValueError("A valid color must be chosen when playing a wild card.")
                self.current_color = chosen_color
            else:
                self.current_color = card.color

            # Apply card effects and advance turn
            if card_type == CardType.REVERSE:
                self.game_direction *= -1
                if len(self.players) == 2:
                    return
            elif card_type == CardType.SKIP:
                self.next_player()
            elif card_type == CardType.DRAW_TWO:
                next_player_index = (self.current_player_index + self.game_direction) % len(self.players)
                player_to_penalize = self.players[next_player_index]
                for _ in range(2):
                    player_to_penalize.add_card_to_hand(self.draw_card_from_deck())
                self.next_player()
            elif card_type == CardType.WILD_DRAW_FOUR:
                next_player_index = (self.current_player_index + self.game_direction) % len(self.players)
                player_to_penalize = self.players[next_player_index]
                for _ in range(4):
                    player_to_penalize.add_card_to_hand(self.draw_card_from_deck())
                self.next_player()

            self.next_player()

        else:
            # --- Logic for DRAWING a card ---
            drawn_card = self.draw_card_from_deck()
            if drawn_card:
                player.add_card_to_hand(drawn_card)

            player.uno_status = False # Drawing always resets uno status

            # Simplified rule: turn ends after drawing.
            self.next_player()
