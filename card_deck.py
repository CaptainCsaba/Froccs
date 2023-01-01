import random

from card import Card, CardName
from exceptions import CardDeckIsEmptyException

card_counts = {
    CardName.SODA: 35,
    CardName.MUSCAT_OTTONEL: 22,
    CardName.GREY_FRIAR: 16,
    CardName.ZOLD_VELTELLINI: 10,
    CardName.BREAD_AND_DRIPPING: 5,
    CardName.WATER_SPILL: 5,
    CardName.TIP: 5,
    CardName.GLASS_BREAK: 4,
    CardName.MIDDLE_FINDER: 4
}

# TODO: count punishment card counts as it is not stated anywhere

class CardDeck:

    cards: list[Card]

    def __init__(self) -> None:
        self.cards = []
        for card_name, card_count in card_counts.items():
            for _ in range(card_count):
                self.cards.append(Card(name=card_name))
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise CardDeckIsEmptyException("There are no more cards left in the deck!")
        return self.cards.pop(0)