from gym_yahtzee import rules
from unittest import TestCase


class RulesTestCase(TestCase):
    def test_upper_section(self):
        self.assertEqual(rules.score_upper_section([1, 1, 1, 2, 3], 1), 3)
        self.assertEqual(rules.score_upper_section([2, 1, 2, 2, 4], 2), 6)
        self.assertEqual(rules.score_upper_section([1, 1, 1, 2, 3], 6), 0)

    def test_three_of_a_kind(self):
        self.assertEqual(rules.score_three_of_a_kind([1, 1, 1, 2, 2]), 3)
        self.assertEqual(rules.score_three_of_a_kind([2, 2, 2, 3, 2]), 6)
        self.assertEqual(rules.score_three_of_a_kind([1, 2, 2, 3, 6]), 0)
        self.assertEqual(rules.score_three_of_a_kind([6, 6, 6, 6, 6]), 18)

    def test_full_house(self):
        self.assertEqual(rules.score_full_house([1, 1, 1, 2, 2]), 7)
        self.assertEqual(rules.score_full_house([1, 1, 1, 2, 3]), 0)
