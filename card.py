from __future__ import annotations
from enum import StrEnum, auto


class CardName(StrEnum):
    SODA = "Soda"
    MUSCAT_OTTONEL = "Muscat Ottonel"
    GREY_FRIAR = "Grey Friar"
    ZOLD_VELTELLINI = "Zold Veltellini"
    BREAD_AND_DRIPPING = "Bread & Dripping"
    WATER_SPILL = "Water Spill"
    TIP = "Tip"
    GLASS_BREAK = "Glass Break"
    MIDDLE_FINDER = "Middle Finger"

    @staticmethod
    def all() -> list[str]:
        return [item.value for item in CardName.__members__.values()]


class CardType(StrEnum):
    SODA = auto()
    VINE = auto()
    PUNISHMENT = auto()
    RESIST = auto()


card_type_mapping = {
    CardName.SODA: CardType.SODA,
    CardName.MUSCAT_OTTONEL: CardType.VINE,
    CardName.GREY_FRIAR: CardType.VINE,
    CardName.ZOLD_VELTELLINI: CardType.VINE,
    CardName.BREAD_AND_DRIPPING: CardType.PUNISHMENT,
    CardName.WATER_SPILL: CardType.PUNISHMENT,
    CardName.TIP: CardType.PUNISHMENT,
    CardName.GLASS_BREAK: CardType.PUNISHMENT,
    CardName.MIDDLE_FINDER: CardType.RESIST
}

class Card:

    def __init__(self, name: CardName) -> None:
        self.name = name
        self.type = card_type_mapping[name]

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name    

    @staticmethod
    def get_type_of_name(name: CardName) -> CardType:
        return card_type_mapping[name]
