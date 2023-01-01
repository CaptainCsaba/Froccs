from enum import StrEnum
import random


class HeroName(StrEnum):
    MELYIVO_FRED = "Melyivo Fred"
    LOTTYINTOS = "Lottyintos"
    KUV_EVI = "Kuv Evi"
    POHARNOK = "Poharnok"
    RECYCLE_BELA = "Recycle Bela"
    SARKI_JEZUS = "Sarki Jezus"
    SOMMELIER_PITYU = "Sommelier Pityu"
    VIZKOPO_KARESZ = "Vizkopo Karesz"
    BOSKE_A_RETTENTO = "Boske, a Rettento"
    HOLLOSI_ELVTARS = "Hollosi elvtars"
    BUZGOMOCSING = "Buzgomocsing"
    ICUKA = "Icuka"


class HeroManager:

    _selected_heroes: list[HeroName]
    _available_heroes: list[HeroName]

    def __init__(self, player_count: int) -> None:
        self._selected_heroes = []
        self._available_heroes = list(HeroName.__members__.values())
        if player_count == 2:
            # When there are only 2 players, these heroes are unavailable.
            self._available_heroes.remove(HeroName.BUZGOMOCSING)
            self._available_heroes.remove(HeroName.ICUKA)
            self._available_heroes.remove(HeroName.HOLLOSI_ELVTARS)
            self._available_heroes.remove(HeroName.BOSKE_A_RETTENTO)

    def select_random_hero(self) -> HeroName:
        selected_hero = random.choice(self._available_heroes)
        self._selected_heroes.append(selected_hero)
        self._available_heroes.remove(selected_hero)
        return selected_hero