from gym_yahtzee.component import (
    action_to_dice_roll_map,
    action_to_scorebox_map,
    dice_roll_to_action_map,
    scorebox_to_action_map,
    scorebox_to_scoring_function_map,
    ScoreBox,
)

from unittest import TestCase


class ActionTestCase(TestCase):
    def test_scorebox_function_map(self):
        self.assertEqual(scorebox_to_scoring_function_map[ScoreBox.ACES]([1, 1, 1, 1, 1]), 5)  # noqa
        self.assertTupleEqual(action_to_dice_roll_map[30], (False, False, False, False, True))  # noqa

    def test_rolling_action_map(self):
        start_action_1 = 0
        dice_roll_1 = action_to_dice_roll_map[start_action_1]
        final_action_1 = dice_roll_to_action_map[dice_roll_1]
        self.assertEqual(start_action_1, final_action_1)

        start_action_2 = 30
        dice_roll_2 = action_to_dice_roll_map[start_action_2]
        final_action_2 = dice_roll_to_action_map[dice_roll_2]
        self.assertEqual(start_action_2, final_action_2)

    def test_action_and_scorebox_maps(self):
        start_scorebox_1 = ScoreBox.ACES
        action_1 = scorebox_to_action_map[start_scorebox_1]
        final_scorebox_1 = action_to_scorebox_map[action_1]
        self.assertEqual(start_scorebox_1, final_scorebox_1)

        start_scorebox_2 = ScoreBox.YAHTZEE
        action_2 = scorebox_to_action_map[start_scorebox_2]
        final_scorebox_2 = action_to_scorebox_map[action_2]
        self.assertEqual(start_scorebox_2, final_scorebox_2)
