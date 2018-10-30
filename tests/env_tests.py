from gym_yahtzee.envs.yahtzee_env import GameType, YahtzeeSingleEnv
from pyhtzee.classes import Category
from pyhtzee.utils import category_to_action_map


from unittest import TestCase


class YahtzeeSingleEnvTestCase(TestCase):
    def test_sudden_death(self):
        env = YahtzeeSingleEnv(seed=123, game_type=GameType.SUDDEN_DEATH)
        action = category_to_action_map[Category.ACES]
        observation, reward, done, _ = env.step(action)
        self.assertEqual(env.pyhtzee.scores.get(Category.ACES), 2)
        self.assertFalse(done)
        self.assertEqual(observation[0], 1)
        self.assertEqual(observation[1], 0)
        observation, reward, done, _ = env.step(action)
        self.assertEqual(reward, -2)
        self.assertTrue(done)

    def test_retry_on_wrong_action(self):
        env = YahtzeeSingleEnv(seed=123, game_type=GameType.RETRY_ON_WRONG_ACTION)
        action = category_to_action_map[Category.ACES]
        observation, reward, done, _ = env.step(action)
        self.assertEqual(env.pyhtzee.scores.get(Category.ACES), 2)
        self.assertFalse(done)
        self.assertEqual(observation[0], 1)  # round
        self.assertEqual(observation[1], 0)  # sub-round
        observation, reward, done, _ = env.step(action)
        self.assertEqual(reward, 0)
        # rounds unchanged
        self.assertEqual(observation[0], 1)
        self.assertEqual(observation[1], 0)
        self.assertFalse(done)
