from collections import Counter
from typing import Collection

def score_upper_section(dice: Collection[int], category: int) -> int:
    """
    Calculate the score for a category in the upper section. For example, the score
    for dice = [1, 1, 2, 2, 3] and category = 2 (twos) would be 4.

    :param dice: the value of each die in a collection
    :param category: 1 for aces, 2 for twos etc
    :return: total score for category, 0 if not valid, ie. no dice equal to category
    """
    return sum(die if die == category else 0 for die in dice)


def score_three_of_a_kind(dice: Collection[int]) -> int:
    for die, count in Counter(dice).most_common(1):
        if count >= 3:
            return die * 3
        return 0


def score_full_house(dice: Collection[int]) -> int:
    counter = Counter(dice)
    if len(counter.keys()) == 2 and min(counter.values()) == 2:
        return sum(counter.elements())
    return 0
