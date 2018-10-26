import gym
from gym import spaces

from typing import Optional

import gym_yahtzee.state

import numpy as np

import sys


def get_score(score: Optional[int]) -> str:
    return '' if score is None else str(score)


class YahtzeeSingleEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.state = gym_yahtzee.state.State()
        self.action_space = spaces.Discrete(44)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(6),  # die 1 score
            spaces.Discrete(6),  # die 2 score
            spaces.Discrete(6),  # die 3 score
            spaces.Discrete(6),  # die 4 score
            spaces.Discrete(6),  # die 5 score
            spaces.MultiBinary(14),  # Score Boxes 1-14 active or not
            spaces.Box(low=0, high=105, shape=(1,), dtype=np.uint8),  # upper score
            spaces.Box(low=0, high=35, shape=(1,), dtype=np.uint8),  # upper bonus
            spaces.Box(low=0, high=220, shape=(1,), dtype=np.uint8),  # lower score
        ))

    def sample_action(self):
        return self.state.sample_action()

    def step(self, action):
        reward = self.state.take_action(action)
        return None, reward, self.state.is_finished(), None

    def reset(self):
        self.state = gym_yahtzee.state.State()

    def render(self, mode='human', close=False):
        dice = self.state.dice
        outfile = sys.stdout
        outfile.write(f'Dice: {dice[0]} {dice[1]} {dice[2]} {dice[3]} {dice[4]} '
                      f'Round: {self.state.round}.{self.state.sub_round} '
                      f'Score: {self.state.get_total_score()}\n')
