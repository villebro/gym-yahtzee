import gym
from gym import error, spaces, utils
from gym.utils import seeding


class YahtzeeSingleEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(56)
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass
