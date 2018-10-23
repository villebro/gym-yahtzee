from gym_yahtzee.component import (
    dice_rolling_map,
    ScoreBox,
    scorebox_to_scoring_function_map,
)

from unittest import TestCase


class ActionTestCase(TestCase):
    def test_scorebox_function_map(self):
        self.assertEqual(scorebox_to_scoring_function_map[ScoreBox.ACES]([1, 1, 1, 1, 1]), 5)  # noqa

    def test_rolling_action_map(self):
        self.assertListEqual(dice_rolling_map[0], [1, 1, 1, 1, 1])
        self.assertListEqual(dice_rolling_map[30], [0, 0, 0, 0, 1])
