from __future__ import annotations
from enum import IntEnum

from card import Card, CardType, CardName
from exceptions import PourDrinkInGlassException


class GlassSize(IntEnum):
    TWO_DECILITRE = 2,
    THREE_DECILITRE = 3,
    FIVE_DECILITRE = 5,

    @classmethod
    def from_size(cls, size: int) -> GlassSize:
        match size:
            case 2:
                return GlassSize.TWO_DECILITRE
            case 3:
                return GlassSize.THREE_DECILITRE
            case 5:
                return GlassSize.FIVE_DECILITRE
            case _:
                raise Exception(f"Invalid glass size: {size}.")

glass_sell_values = {
    tuple([1, 1]): [30, 30, 40],
    tuple([1, 2]): [30, 40, 50],
    tuple([2, 1]): [40, 50, 60],
    tuple([1, 4]): [50, 50, 60],
    tuple([2, 3]): [60, 70, 80],
    tuple([3, 2]): [60, 80, 90],
    tuple([4, 1]): [70, 90, 110],
}      


class Glass:

    def __init__(self, size: GlassSize) -> None:
        self.size = size
        self.cards: list[Card] = []
        self.vine_type: CardName = None

    def __repr__(self) -> str:
        return f"Glass: size={self.size}dl, portions=[{', '.join(sorted(map(str, self.cards)))}]"

    def is_full(self) -> bool:
        return self.size.value == len(self.cards)

    def pour_in_glass(self, card: Card) -> None:
        if card.type != CardType.SODA and card.type != CardType.VINE:
            raise PourDrinkInGlassException("You can't pour this card into the glass!")
        if card.type == CardType.SODA:
            if self.size.value - 1 == self.count_card_in_glass(card):
                raise PourDrinkInGlassException("This glass has reached the maximum allowed soda amount.")
        if card.type == CardType.VINE:
            if any([c.type == CardType.VINE and c.name != card.name for c in self.cards]):
                raise PourDrinkInGlassException("There is already another type of vine in this glass.")
            if self.size.value - 1 == self.count_card_in_glass(card):
                raise PourDrinkInGlassException("This glass has reached the maximum allowed vine amount.")
            if self.vine_type is None:
                self.vine_type = card.name
        self.cards.append(card)

    def remove_one_dl_vine(self) -> None:
        vine_to_remove = next((card for card in self.cards if card.type == CardType.VINE), None)
        if vine_to_remove is None:
            return
        self.cards.remove(vine_to_remove)

    def remove_one_dl_soda(self) -> None:
        soda_to_remove = next((card for card in self.cards if card.type == CardType.SODA), None)
        if soda_to_remove is None:
            return
        self.cards.remove(soda_to_remove)

    def calculate_value(self) -> int:
        if not self.is_full():
            return 0
        soda_portions = len([card for card in self.cards if card.type == CardType.SODA])
        vine_portions = self.size.value - soda_portions
        prices = glass_sell_values[tuple([vine_portions, soda_portions])]
        price_index = [CardName.MUSCAT_OTTONEL, CardName.GREY_FRIAR, CardName.ZOLD_VELTELLINI].index(self.vine_type)
        return prices[price_index]
            
    def count_card_in_glass(self, card: Card) -> int:
        return len([c for c in self.cards if c.type == card.type])