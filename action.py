from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from player import Player
from glass import Glass
from card import Card, CardName, CardType
from card_deck import CardDeck
from glass_counter import GlassCounter
from exceptions import GlassPurchaseException, CardUsageException, PlayerIndexError, NoSuchActionException
from hero import HeroName
from hero_ability import HeroAbility


class Action(ABC):

    @abstractmethod
    def __init__(self, player: Player) -> None:
        self.player = player

    @abstractmethod
    def execute(self) -> None:
        pass

    @staticmethod
    def possible_actions() -> list[str]:
        return list(action_mapping.keys())

    staticmethod
    def parse_action(name: str) -> Action:
        action = action_mapping.get(name, None)
        if action is None:
            raise NoSuchActionException(f"There is no action called: '{name}'.")
        return action


class SellSpritzer(Action):

    def __init__(self, player: Player, glass: Glass, glass_counter: GlassCounter) -> None:
        super().__init__(player)
        self.glass = glass
        self.glass_counter = glass_counter

    def execute(self) -> None:
        self.player.sell_glass(self.glass)
        if self.player.hero == HeroName.MELYIVO_FRED:
            HeroAbility.melyivo_fred(self.player, self.glass, self.glass_counter)


class DrawCards(Action):

    def __init__(self, player: Player, deck: CardDeck) -> None:
        super().__init__(player)
        self.deck = deck

    def execute(self) -> None:
        draw_count = 2
        for _ in range(draw_count):
            self.player.draw_card(self.deck.draw())


class PurchaseGlasses(Action):

    def __init__(self, player: Player, glass_indexes_on_counter: list[int], glass_counter: GlassCounter) -> None:
        super().__init__(player)
        self.amount = len(glass_indexes_on_counter)
        self.glass_indexes_on_counter = sorted(glass_indexes_on_counter, reverse=True)
        self.glass_counter = glass_counter

    def execute(self) -> None:
        if self.amount > 3 - len(self.player.glasses):
            raise GlassPurchaseException("You have reached the maximum amount of glasses, and can't have more.")
        if self.amount > 2:
            raise GlassPurchaseException("You are only allowed to buy the maximum of two glasses!")
        if self.player.money < 10:
            raise GlassPurchaseException("You don't have enough money to buy this glass!")
        for index in self.glass_indexes_on_counter:
            self.player.add_glass(self.glass_counter.purchase_glass(index))
            self.player.subtract_money(amount=10)


@dataclass
class CardAction:
    card: Card
    target_glass_index: int

@dataclass
class PunishmentCardAction(CardAction):
    punished_player_index: int



class UseCards(Action):

    def __init__(self, player: Player, card_actions: list[CardAction], all_players: list[Player]) -> None:
        super().__init__(player)
        self.card_actions = card_actions
        self.all_players = all_players

    def execute(self) -> None:
        if len(self.card_actions) > len(self.player.glasses):
            raise CardUsageException(f"You can only use {len(self.player.glasses)} in this turn. (The amount of glasses you have.)")
        for card_action in self.card_actions:
            card = card_action.card
            if card.name == CardName.MIDDLE_FINDER:
                raise CardUsageException("The Middle Finger card is not usable here.")
            elif card.type == CardType.SODA or card.type == CardType.VINE:
                self._fill_glass(card_action)
            elif card.type == CardType.PUNISHMENT:
                self._punish_player(card_action)

    def _fill_glass(self, card_action: CardAction) -> None:
        glass = self.player.get_glass(card_action.target_glass_index)
        glass.pour_in_glass(card_action.card)

    def _punish_player(self, card_action: CardAction) -> None:
        if card_action.punished_player_index < 0:
            raise PlayerIndexError("No punished player was selected.")
        if card_action.punished_player_index > len(self.all_players) - 1:
            raise PlayerIndexError("Target player not found.")
        target_player = self.all_players[card_action.punished_player_index]
        match card_action.card.name:
            case CardName.WATER_SPILL:
                glass = target_player.get_glass(card_action.target_glass_index)
                glass.remove_one_dl_soda()
            case CardName.BREAD_AND_DRIPPING:
                glass = target_player.get_glass(card_action.target_glass_index)
                glass.remove_one_dl_vine()
            case CardName.GLASS_BREAK:
                target_player.remove_glass(card_action.target_glass_index)
            case CardName.TIP:
                target_player.subtract_money(20, allowed_to_go_below_zero=True)
            case _:
                raise Exception(f"Unknown punishment card: {card_action.card.name}.")


action_mapping = {
    "sell spritzer": SellSpritzer,
    "draw card": DrawCards,
    "purchase glasses": PurchaseGlasses,
    "use cards": UseCards
}