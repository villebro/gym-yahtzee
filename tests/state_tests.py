from gym_yahtzee.state import State
from gym_yahtzee import component
from gym_yahtzee.component import (
    dice_roll_to_action_map,
    Category,
    category_to_action_map
)

from unittest import TestCase


class StateTestCase(TestCase):
    def test_dice_values(self):
        state = State()
        for die in state.dice:
            self.assertTrue(1 <= die <= 6)

    def test_rolling_of_dice(self):
        state = State(seed=123)
        self.assertListEqual([1, 3, 1, 4, 3], state.dice)
        action = component.dice_roll_to_action_map[(True, True, True, True, True)]
        reward = state.take_action(action)
        self.assertListEqual([1, 1, 4, 5, 5], state.dice)
        self.assertEqual(reward, 0)
        action = component.dice_roll_to_action_map[(False, False, False, False, True)]
        state.take_action(action)
        self.assertListEqual([1, 1, 4, 5, 3], state.dice)

    def test_full_round_four_threes(self):
        state = State(seed=234)
        self.assertListEqual([3, 3, 1, 5, 4], state.dice)
        action = component.dice_roll_to_action_map[(False, False, True, True, True)]
        state.take_action(action)
        self.assertListEqual([3, 3, 5, 6, 4], state.dice)
        action = component.dice_roll_to_action_map[(False, False, True, True, True)]
        state.take_action(action)
        self.assertListEqual([3, 3, 2, 3, 3], state.dice)
        action = category_to_action_map[Category.THREES]
        reward = state.take_action(action)
        self.assertEqual(reward, 12)
        self.assertEqual(state.scores[Category.THREES], reward)

    def test_full_round_unsuccessful_yahtzee(self):
        state = State(seed=234)
        self.assertListEqual([3, 3, 1, 5, 4], state.dice)
        action = category_to_action_map[Category.YAHTZEE]
        reward = state.take_action(action)
        self.assertEqual(reward, 0)
        self.assertEqual(state.scores[Category.YAHTZEE], reward)

    def test_completing_roung(self):
        state = State(seed=345)
        action = dice_roll_to_action_map[(True, True, True, True, True)]
        state.take_action(action)
        state.take_action(action)
        self.assertListEqual([3, 4, 6, 3, 1], state.dice)

    def test_full_round_successful_yahtzee(self):
        state = State()
        state.dice = [1, 1, 1, 1, 1]
        action = category_to_action_map[Category.YAHTZEE]
        reward = state.take_action(action)
        self.assertEqual(reward, 50)
        self.assertEqual(state.scores[Category.YAHTZEE], reward)

    def test_full_round_successful_chance(self):
        state = State()
        state.dice = [6, 6, 6, 6, 5]
        action = category_to_action_map[Category.CHANCE]
        reward = state.take_action(action)
        self.assertEqual(reward, 29)
        self.assertEqual(state.scores[Category.CHANCE], reward)

    def test_upper_section_bonus(self):
        state = State()
        state.dice = [1, 1, 1, 1, 1]
        state.take_action(category_to_action_map[Category.ACES])
        state.dice = [2, 2, 2, 2, 2]
        state.take_action(category_to_action_map[Category.TWOS])
        state.dice = [3, 3, 3, 3, 3]
        state.take_action(category_to_action_map[Category.THREES])
        state.dice = [4, 4, 4, 4, 4]
        state.take_action(category_to_action_map[Category.FOURS])
        state.dice = [5, 5, 5, 5, 5]
        state.take_action(category_to_action_map[Category.FIVES])
        state.dice = [6, 6, 6, 6, 6]
        action = category_to_action_map[Category.SIXES]
        reward = state.take_action(action)
        self.assertEqual(reward, 65)
        self.assertEqual(state.scores[Category.SIXES], 30)
        self.assertEqual(state.scores[Category.UPPER_SECTION_BONUS], 35)

    def test_perfect_score(self):
        state = State()
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.YAHTZEE])
        state.dice = [1, 1, 1, 1, 1]
        state.take_action(category_to_action_map[Category.ACES])
        state.dice = [2, 2, 2, 2, 2]
        state.take_action(category_to_action_map[Category.TWOS])
        state.dice = [3, 3, 3, 3, 3]
        state.take_action(category_to_action_map[Category.THREES])
        state.dice = [4, 4, 4, 4, 4]
        state.take_action(category_to_action_map[Category.FOURS])
        state.dice = [5, 5, 5, 5, 5]
        state.take_action(category_to_action_map[Category.FIVES])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.SIXES])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.THREE_OF_A_KIND])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.FOUR_OF_A_KIND])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.FULL_HOUSE])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.SMALL_STRAIGHT])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.LARGE_STRAIGHT])
        state.dice = [6, 6, 6, 6, 6]
        state.take_action(category_to_action_map[Category.CHANCE])
        self.assertEqual(state.get_total_score(), 1505)
        self.assertTrue(state.is_finished())
