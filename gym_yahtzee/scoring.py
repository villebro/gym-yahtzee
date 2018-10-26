"""
Scoring functions for lists with five dice. All functions (except upper sectino bonus)
are given a a list of ints representing the number of dots on the face. If the list of
dice is not valid for the scoring function, a zero is retured, indicating that the user
has stricken that score box off the scorecard.
"""
from collections import Counter
from typing import List, Set


def score_upper_section(dice: List[int], face: int) -> int:
    return sum(die if die == face else 0 for die in dice)


def score_x_of_a_kind(dice: List[int], min_same_faces: int) -> int:
    for die, count in Counter(dice).most_common(1):
        if count >= min_same_faces:
            return sum(dice)
    return 0


def score_full_house(dice: List[int], joker_rule: bool = True) -> int:
    successful_score = 25
    counter = Counter(dice)
    if joker_rule:
        if len(counter.keys()) == 1:
            return successful_score
    if len(counter.keys()) == 2 and min(counter.values()) == 2:
        return successful_score
    return 0


def _are_two_sets_equal(a: Set, b: Set) -> bool:
    return a.intersection(b) == a


def score_small_straight(dice: List[int]) -> int:
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4}, dice_set) or \
            _are_two_sets_equal({2, 3, 4, 5}, dice_set) or \
            _are_two_sets_equal({3, 4, 5, 6}, dice_set):
        return 30
    return 0


def score_large_straight(dice: List[int]) -> int:
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4, 5}, dice_set) or \
            _are_two_sets_equal({2, 3, 4, 5, 6}, dice_set):
        return 40
    return 0


def score_yahtzee(dice: List[int]) -> int:
    if len(set(dice)) == 1:
        return 50
    return 0


def score_extra_yahtzee() -> int:
    return 100


def score_chance(dice: List[int]) -> int:
    return sum(dice)


def score_upper_section_bonus(upper_section_score: int) -> int:
    return 35 if upper_section_score >= 63 else 0
