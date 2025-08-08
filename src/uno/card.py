from enum import Enum

class Color(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    WILD = "wild"

class CardType(Enum):
    NUMBER = "number"
    SKIP = "skip"
    REVERSE = "reverse"
    DRAW_TWO = "+2"
    WILD = "wild"
    WILD_DRAW_FOUR = "+4"

class Card:
    def __init__(self, color: Color, card_type: CardType, value: int = None):
        self.color = color
        self.card_type = card_type
        self.value = value

    def __str__(self):
        if self.card_type == CardType.NUMBER:
            return f"{self.color.value} {self.value}"
        else:
            return f"{self.color.value} {self.card_type.value}"

    def __repr__(self):
        return self.__str__()
