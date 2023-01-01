import random

from glass import Glass, GlassSize
from exceptions import GlassPurchaseException


glass_counts = {
    GlassSize.TWO_DECILITRE: 9,
    GlassSize.THREE_DECILITRE: 9,
    GlassSize.FIVE_DECILITRE: 8,
}

# TODO: count glass cards as their count is not stated anywhere


class GlassCounter:

    all_glasses: list[Glass]
    glasses_on_counter: list[Glass]

    def __init__(self) -> None:
        self.all_glasses = []
        self.glasses_on_counter = []
        self.clean_all_glasses()

    def clean_all_glasses(self) -> None:
        self.all_glasses = []
        for glass_size, glass_count in glass_counts.items():
            for _ in range(glass_count):
                self.all_glasses.append(Glass(size=glass_size))
        random.shuffle(self.all_glasses)
        self.glasses_on_counter = [self.all_glasses.pop(0), self.all_glasses.pop(0), self.all_glasses.pop(0)]

    def purchase_glass(self, counter_index: int) -> Glass:
        if counter_index > 2:
            raise GlassPurchaseException("There are only 3 glasses on the counter. You can't purchase by this index.")
        purchased_glass = self.glasses_on_counter.pop(counter_index)
        if len(self.all_glasses) > 0:
            self.glasses_on_counter.append(self.all_glasses.pop(0))
        else:
            self.clean_all_glasses()
        return purchased_glass

    def get_glass_by_type(self, type: GlassSize) -> Glass:
        glass_indexes_of_type = [self.all_glasses.index(glass) for glass in self.all_glasses if glass.size == type.value]
        glass_to_get = random.choice(glass_indexes_of_type)
        return self.all_glasses.pop(glass_to_get)