"""
Collection of components that are needed for gameplay, including maps that make it
possible to convert actions (e.g. choosing threes on the scorecard) to score boxes
(e.g. full house on the scorecard) and vice versa. Similar maps are also provided
for mapping dice rolling lists (e.g. reroll dice 2, 3 and 4 but keep dice 1 and 5)
to and from actions and scorebox to scoring functions.
"""
from enum import IntEnum
from typing import Callable, Dict, Tuple

from gym_yahtzee.scoring import *


class ScoreBox(IntEnum):
    ACES = 0
    TWOS = 1
    THREES = 2
    FOURS = 3
    FIVES = 4
    SIXES = 5
    THREE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 8
    SMALL_STRAIGHT = 9
    LARGE_STRAIGHT = 10
    YAHTZEE = 11
    CHANCE = 12
    UPPER_SECTION_BONUS = 13


# Mapping from action id to permutations of rerolling of dice. Each unique combination
# of dice rolls is given a unique id, resulting in 32 unique constellations. However,
# keeping all dice is left out, as the player should then choose a score box from the
# scorecard, hence there are 31 unique rerolling patterns. An offset constant is
# provided, as scorebox actions are located after dice rolling actions.
SCOREBOX_ACTION_OFFSET = 31
action_to_dice_roll_map: Dict[int, Tuple[bool, bool, bool, bool, bool]] = {}
dice_roll_to_action_map: Dict[Tuple[bool, bool, bool, bool, bool], int] = {}
for d1 in [1, 0]:
    for d2 in [1, 0]:
        for d3 in [1, 0]:
            for d4 in [1, 0]:
                for d5 in [1, 0]:
                    # make rolling all dice the first action, i.e. zero
                    key = 31 - (d5*2**0 + d4*2**1 + d3*2**2 + d2*2**3 + d1*2**4)
                    value = bool(d1), bool(d2), bool(d3), bool(d4), bool(d5)
                    # not rolling any dice is not a valid action
                    if key < 31:
                        action_to_dice_roll_map[key] = value
                        dice_roll_to_action_map[value] = key


# Mapping from action id to scorebox and vice versa.
action_to_scorebox_map: Dict[int, ScoreBox] = {}
scorebox_to_action_map: Dict[ScoreBox, int] = {}
for i in range(13):
    scorebox = ScoreBox(i)
    action_to_scorebox_map[i + SCOREBOX_ACTION_OFFSET] = scorebox
    scorebox_to_action_map[scorebox] = i + SCOREBOX_ACTION_OFFSET

# Mapping from scorebox to scoring function
scorebox_to_scoring_function_map: Dict[int, Callable[..., int]] = {}
scorebox_to_scoring_function_map[ScoreBox.ACES] = lambda x: score_upper_section(x, 1)
scorebox_to_scoring_function_map[ScoreBox.TWOS] = lambda x: score_upper_section(x, 2)
scorebox_to_scoring_function_map[ScoreBox.THREES] = lambda x: score_upper_section(x, 3)
scorebox_to_scoring_function_map[ScoreBox.FOURS] = lambda x: score_upper_section(x, 4)
scorebox_to_scoring_function_map[ScoreBox.FIVES] = lambda x: score_upper_section(x, 5)
scorebox_to_scoring_function_map[ScoreBox.SIXES] = lambda x: score_upper_section(x, 6)
scorebox_to_scoring_function_map[ScoreBox.THREE_OF_A_KIND] = lambda x: score_x_of_a_kind(x, 3)  # noqa
scorebox_to_scoring_function_map[ScoreBox.FOUR_OF_A_KIND] = lambda x: score_x_of_a_kind(x, 4)  # noqa
scorebox_to_scoring_function_map[ScoreBox.FULL_HOUSE] = lambda x: score_full_house(x)
scorebox_to_scoring_function_map[ScoreBox.SMALL_STRAIGHT] = lambda x: score_small_straight(x)  # noqa
scorebox_to_scoring_function_map[ScoreBox.LARGE_STRAIGHT] = lambda x: score_large_straight(x)  # noqa
scorebox_to_scoring_function_map[ScoreBox.YAHTZEE] = lambda x: score_yahtzee(x)
scorebox_to_scoring_function_map[ScoreBox.CHANCE] = lambda x: score_chance(x)
