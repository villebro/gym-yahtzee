from random import Random
from typing import Dict, Optional

from gym_yahtzee.component import (
    action_to_category_map,
    action_to_dice_roll_map,
    Category,
    SCOREBOX_ACTION_OFFSET,
    category_to_action_map,
    category_to_scoring_function_map,
)
from gym_yahtzee.scoring import score_upper_section_bonus, score_extra_yahtzee


class State:
    def __init__(self, seed: int = None):
        self.scores: Dict[Category, Optional[int]] = {}

        # a game has a total of 12 rounds
        self.round = 0

        # a round consists of max 3 dice rolls + 1 action = 4. Sub-round zero is
        # reserved for two player game when a player has not yet started the round
        self.sub_round = 1

        if seed:
            self.rnd = Random(seed)
        else:
            self.rnd = Random()

        # initialize dice
        self.dice = [0, 0, 0, 0, 0]
        self.roll_dice(True, True, True, True, True)

    def roll_dice(self, d1: bool, d2: bool, d3: bool, d4: bool, d5: bool):
        dice = [d1, d2, d3, d4, d5]
        for i, die in enumerate(dice):
            if die:
                self.dice[i] = self.rnd.choice([1, 2, 3, 4, 5, 6])

    def get_possible_actions(self):
        possible_actions = []

        # determine if rerolling dice is possible; is so, add all possible permutations
        if self.sub_round < 3:
            possible_actions.extend(list(range(31)))

        # See which categories are still unused
        for category in Category:
            if not self.scores.get(category):
                action = category_to_action_map.get(category)
                # Check if the category has an action associated with it
                # (upper section bonus is automatic).
                if action:
                    possible_actions.append(action)

        return possible_actions

    def sample_action(self):
        actions = self.get_possible_actions()
        return self.rnd.sample(actions, 1)[0]

    def take_action(self, action: int) -> int:
        possible_actions = self.get_possible_actions()
        if action not in possible_actions:
            return 0

        # if dice rolling action
        if action < SCOREBOX_ACTION_OFFSET:
            self.sub_round += 1
            self.roll_dice(*action_to_dice_roll_map[action])
            return 0

        # all non-rolling actions lead to the sub-round
        # ending and moving to the next round
        self.round += 1
        self.sub_round = 0

        category = action_to_category_map[action]
        scoring_function = category_to_scoring_function_map[category]
        reward = scoring_function(self.dice)
        self.scores[category] = reward

        # upper section
        if SCOREBOX_ACTION_OFFSET <= action <= SCOREBOX_ACTION_OFFSET + 5:
            upper_scores = [v for k, v in self.scores.items()
                            if int(k) <= int(Category.SIXES)]
            if len(upper_scores) == 6:
                bonus_reward = score_upper_section_bonus(sum(filter(None, upper_scores)))
                self.scores[Category.UPPER_SECTION_BONUS] = bonus_reward
                reward += bonus_reward

        # extra yahtzee
        if category != Category.YAHTZEE and self.is_extra_yahtzee():
            extra_yahtzee_reward = score_extra_yahtzee()
            reward += extra_yahtzee_reward
            extra_yahtzee_score = self.scores.get(Category.EXTRA_YAHTZEES)
            extra_yahtzee_score = extra_yahtzee_score if extra_yahtzee_score else 0
            self.scores[Category.EXTRA_YAHTZEES] = extra_yahtzee_score + extra_yahtzee_reward  # noqa

        return reward

    def is_extra_yahtzee(self):
        if len(set(self.dice)) == 1 and self.scores.get(Category.YAHTZEE):
            return True
        return False

    def is_yahtzee(self):
        return True if len(set(self.dice)) == 1 else False

    def is_finished(self):
        return True if self.round == 13 else False

    def get_total_score(self):
        return sum(filter(None, [v for v in self.scores.values()]))
