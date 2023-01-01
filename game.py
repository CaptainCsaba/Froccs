from typing import Any, Optional

from player import Player
from card_deck import CardDeck
from glass import GlassSize, Glass
from glass_counter import GlassCounter
from action import Action, SellSpritzer, DrawCards, PurchaseGlasses, UseCards, CardAction, PunishmentCardAction
from exceptions import ActionException, CardUsageException, GameException, GlassIndexException
from card import CardType, CardName
from user_input_handler import UserInput
       

class Game:

    card_deck: CardDeck
    glass_counter: GlassCounter
    players: list[Player]
    number_of_players: int

    def __init__(self) -> None:
        self.card_deck = CardDeck()
        self.glass_counter = GlassCounter()
        self.number_of_players = 0
        self.players = []
        self._create_players()

    def run(self) -> None:
        # TODO: it has 1 extra round after cards are gone
        while len(self.card_deck.cards) > 0:
            for player in self.players:
                self._run_player_round(player)
                
    def _create_players(self) -> None:
        self.number_of_players = UserInput.ask_for_integer("Please enter how many players will play the game.", min=2, max=6)
        registered_names = []
        i = 1
        while self.number_of_players != len(self.players):
            name = UserInput.ask_for_free_text(f"What is the name of player {i}?")
            if name in registered_names:
                print("There is already a player registered with this name!")
                continue
            player = Player(id=i, name=name)
            for _ in range(5):
                player.draw_card(self.card_deck.draw())
            player.add_money(20)
            player.add_glass(self.glass_counter.get_glass_by_type(GlassSize.TWO_DECILITRE))
            player.add_glass(self.glass_counter.get_glass_by_type(GlassSize.THREE_DECILITRE))
            registered_names.append(name)
            self.players.append(player)
            i += 1

    def _run_player_round(self, player: Player) -> None:
        actions_count = 2
        finished_actions = 0
        while actions_count != finished_actions:
            try:
                print(f"{player.name}, select action {finished_actions + 1}.")
                action = self._ask_player_for_action(player, action_index=finished_actions)
                action.execute()
                finished_actions += 1
            except GameException as ex:
                print(ex)

    def _ask_player_for_action(self, player: Player, action_index: int) -> Action:
        action_name = UserInput.ask_to_select("What would you like to do as your action?", options=Action.possible_actions())
        action_type = Action.parse_action(action_name)
        return self._initialize_action(action_type, player, action_index)

    def _initialize_action(self, action: Action, player: Player, action_index: int) -> Action:
        # TODO: move init methodology into actions and separate ersponsibilities
        if action == SellSpritzer:
            if action_index > 0:
                raise ActionException("The spritzer selling action can only be used as your first action!")
            sellable_glasses = [glass for glass in player.glasses if glass.is_full()]
            if len(sellable_glasses) == 0:
                raise ActionException("None of your glasses are full. You can't sell any!")
            target_glass_index = UserInput.ask_to_select("Which glass would you like to sell?", options=list(map(str, sellable_glasses)), return_index=True)
            action_instance = SellSpritzer(player=player, glass=player.get_glass(target_glass_index))
        elif action == DrawCards:
            action_instance = DrawCards(player=player, deck=self.card_deck)
        elif action == PurchaseGlasses:
            # TODO: add buying for second glass if player wants
            buyable_glass_sizes = [f"{glass.size.value}dl" for glass in self.glass_counter.glasses_on_counter]
            target_glass_index = UserInput.ask_to_select("Which glass would you like to buy?", options=buyable_glass_sizes, return_index=True)
            action_instance = PurchaseGlasses(player=player, glass_indexes_on_counter=[target_glass_index], glass_counter=self.glass_counter)
        elif action == UseCards:
            card_use_count = len(player.glasses)
            selected_card_count = 0
            card_actions = []
            while selected_card_count < card_use_count:
                if len(player.cards) == 0:
                    print("You have no more cards to select!")
                    break
                use_another_card = True
                if selected_card_count > 0:
                    use_another_card = UserInput.ask_for_boolean("Do you want to use another card?")
                if not use_another_card:
                    break
                selected_card_name = UserInput.ask_to_select("Please select a card to use.", options=list(map(str, player.cards)))
                card = player.get_card(selected_card_name)
                if card.type == CardType.RESIST:
                    raise CardUsageException("The middle finger card is not usable here!")
                elif card.type == CardType.PUNISHMENT:
                    player_names = [p.name for p in self.players if player.id != p.id]
                    target_player_name =  UserInput.ask_to_select("Who whould you like to use this card on?", options=player_names)
                    target_player = next((p for p in self.players if p.name == target_player_name))
                    if card.name == CardName.TIP:
                        target_glass_index = -1
                    else:
                        target_glass_index = self._select_glass_of_player(player)
                    card_actions.append(PunishmentCardAction(card=card, target_glass_index=target_glass_index, punished_player_index=target_player.index))
                    selected_card_count += 1
                else:
                    glass = self._select_glass_of_player(player)
                    target_glass_index = player.glasses.index(glass)
                    card_actions.append(CardAction(card=card, target_glass_index=target_glass_index))
                    selected_card_count += 1
            action_instance = UseCards(player=player, card_actions=card_actions, all_players=self.players)
        return action_instance

    def _select_glass_of_player(self, player: Player) -> Glass:
        if len(player.glasses) == 0:
            raise GlassIndexException("The target player has no glasses currently.")
        glass_index = UserInput.ask_to_select("Select a glass you would like to use your card on.", options=list(map(str, player.glasses)), return_index=True)
        return player.glasses[glass_index]