from gym_yahtzee.state import State
from gym_yahtzee.component import ScoreBox, scorebox_to_action_map

from unittest import TestCase


class StateTestCase(TestCase):
    def test_dice_values(self):
        state = State()
        for die in state.dice:
            self.assertTrue(1 <= die <= 6)

    def test_rolling_of_dice(self):
        state = State(seed=123)
        self.assertListEqual([1, 3, 1, 4, 3], state.dice)
        reward = state.take_action(0)
        self.assertListEqual([1, 1, 4, 5, 5], state.dice)
        self.assertEqual(reward, 0)
        state.take_action(30)
        self.assertListEqual([1, 1, 4, 5, 3], state.dice)

    def test_full_round_four_threes(self):
        state = State(seed=234)
        self.assertListEqual([3, 3, 1, 5, 4], state.dice)
        state.take_action(24)
        self.assertListEqual([3, 3, 5, 6, 4], state.dice)
        state.take_action(24)
        self.assertListEqual([3, 3, 2, 3, 3], state.dice)
        action = scorebox_to_action_map[ScoreBox.THREES]
        reward = state.take_action(action)
        self.assertEqual(reward, 12)
        self.assertEqual(state.scores[ScoreBox.THREES], reward)

    def test_full_round_unsuccessful_yahtzee(self):
        state = State(seed=234)
        self.assertListEqual([3, 3, 1, 5, 4], state.dice)
        action = scorebox_to_action_map[ScoreBox.YAHTZEE]
        reward = state.take_action(action)
        self.assertEqual(reward, 0)
        self.assertEqual(state.scores[ScoreBox.YAHTZEE], reward)

    def test_full_round_successful_yahtzee(self):
        state = State()
        state.dice = [1, 1, 1, 1, 1]
        action = scorebox_to_action_map[ScoreBox.YAHTZEE]
        reward = state.take_action(action)
        self.assertEqual(reward, 50)
        self.assertEqual(state.scores[ScoreBox.YAHTZEE], reward)

    def test_full_round_successful_chance(self):
        state = State()
        state.dice = [6, 6, 6, 6, 5]
        action = scorebox_to_action_map[ScoreBox.CHANCE]
        reward = state.take_action(action)
        self.assertEqual(reward, 29)
        self.assertEqual(state.scores[ScoreBox.CHANCE], reward)
