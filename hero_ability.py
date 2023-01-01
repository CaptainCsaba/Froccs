from operator import attrgetter

from glass import Glass
from glass_counter import GlassCounter
from player import Player


class HeroAbility:

    def melyivo_fred(player: Player, sold_spritzer: Glass, glass_counter: GlassCounter) -> None:
        if not sold_spritzer.size.value == 5:
            return
        smallest_glass = min(glass_counter.glasses_on_counter ,key=attrgetter('size.value'))
        player.add_glass(smallest_glass)