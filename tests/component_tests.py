from gym_yahtzee.component import (
    action_to_dice_roll_map,
    ScoreBox,
    scorebox_to_scoring_function_map,
)

from unittest import TestCase


class ActionTestCase(TestCase):
    def test_scorebox_function_map(self):
        self.assertEqual(scorebox_to_scoring_function_map[ScoreBox.ACES]([1, 1, 1, 1, 1]), 5)  # noqa

    def test_rolling_action_map(self):
        self.assertTupleEqual(action_to_dice_roll_map[0], (True, True, True, True, True))
        self.assertTupleEqual(action_to_dice_roll_map[30], (False, False, False, False, True))  # noqa
