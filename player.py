from operator import attrgetter

from exceptions import NotEnoughMoneyException, MaximumGlassCountReached, GlassIndexException, NoSuchCardException
from card import Card, CardName
from glass import Glass
from hero import HeroName

class Player:

    name: str
    money: int
    cards: list[Card]
    glasses: list[Glass]
    hero: HeroName

    def __init__(self, id: int, name: str, hero: HeroName) -> None:
        self.id = id
        self.index = id - 1
        self.name = name
        self.hero = hero
        self.cards = []
        self.money = 0
        self.glasses = []

    def __repr__(self) -> str:
        return f"Player Name='{self.name}', ID={self.id}, Money={self.money}, CardCount={len(self.cards)}, GlassCount={len(self.glasses)}."

    def add_money(self, amount: int) -> None:
        self.money += amount

    def subtract_money(self, amount: int, allowed_to_go_below_zero: bool=False) -> None:
        if amount > self.money and not allowed_to_go_below_zero:
            raise NotEnoughMoneyException(f"Player '{self.name}' only has {self.money} forints to spend.")
        self.money -= amount
        if self.money < 0:
            self.money = 0

    def draw_card(self, card: Card) -> None:
        self.cards.append(card)
        self.cards.sort(key=attrgetter('type', 'name'))

    def get_card(self, card_name: str) -> Card:
        if card_name not in CardName.all():
            NoSuchCardException(f"There is no card called '{card_name}'.")
        card = next((card for card in self.cards if card.name == card_name), None)
        if card is None:
            raise NoSuchCardException(f"This player does not have a {card_name} card.")
        return card

    def add_glass(self, glass: Glass) -> None:
        if len(self.glasses) == 3:
            raise MaximumGlassCountReached("You have reached the maximum amount of glasses, and can't have more.")
        self.glasses.append(glass)
        self.glasses.sort(key=attrgetter('size'))

    def get_glass(self, index: int) -> Glass:
        if index > len(self.glasses):
            raise GlassIndexException(f"You can't get this glass. There are only {len(self.glasses)} glasses.")
        return self.glasses[index]

    def remove_glass(self, index: int) -> None:
        if index > len(self.glasses):
            raise GlassIndexException(f"You can't get this glass. There are only {len(self.glasses)} glasses.")
        self.glasses.pop(index)

    def sell_glass(self, glass: Glass) -> None:
        self.money += glass.calculate_value()
        self.glasses.remove(glass)

