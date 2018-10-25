from gym_yahtzee.component import (
    action_to_dice_roll_map,
    action_to_category_map,
    dice_roll_to_action_map,
    category_to_action_map,
    category_to_scoring_function_map,
    Category,
)

from unittest import TestCase


class ActionTestCase(TestCase):
    def test_category_function_map(self):
        self.assertEqual(category_to_scoring_function_map[Category.ACES]([1, 1, 1, 1, 1]), 5)  # noqa
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

    def test_action_and_category_maps(self):
        start_category_1 = Category.ACES
        action_1 = category_to_action_map[start_category_1]
        final_category_1 = action_to_category_map[action_1]
        self.assertEqual(start_category_1, final_category_1)

        start_category_2 = Category.YAHTZEE
        action_2 = category_to_action_map[start_category_2]
        final_category_2 = action_to_category_map[action_2]
        self.assertEqual(start_category_2, final_category_2)
