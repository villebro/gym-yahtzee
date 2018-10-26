from gym_yahtzee.envs.yahtzee_env import YahtzeeSingleEnv

from unittest import TestCase


class YahtzeeSingleEnvTestCase(TestCase):
    def test_case(self):
        env = YahtzeeSingleEnv()
        env.reset()
        action = env.sample_action()
        observation, reward, done, info = env.step(action)
