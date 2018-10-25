import gym
from gym import error, spaces, utils
from gym.utils import seeding

from typing import Optional

import gym_yahtzee.state
from gym_yahtzee.component import Category

import numpy as np

import sys


def get_score(score: Optional[int]) -> str:
    return '' if score is None else score


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

    def step(self, action: int):
        reward = self.state.take_action(action)
        return None, reward, True, None

    def reset(self):
        self.state = gym_yahtzee.state.State()

    def render(self, mode='human', close=False):
        dice = self.state.dice
        turn = self.state.turn
        scores = self.state.scores
        outfile = sys.stdout
        outfile.write(f'Dice: {dice[0]} {dice[1]} {dice[2]} {dice[3]} {dice[4]}\n')
        outfile.write(f'Turn: {turn}\n')
        outfile.write('\n')
        outfile.write(f'Aces: {get_score(scores[Category.ACES])}\n')
        outfile.write(f'Twos: {get_score(scores[Category.TWOS])}\n')
        outfile.write(f'Threes: {get_score(scores[Category.THREES])}\n')
        outfile.write(f'Fours: {get_score(scores[Category.FOURS])}\n')
        outfile.write(f'Fives: {get_score(scores[Category.FIVES])}\n')
        outfile.write(f'Sixes: {get_score(scores[Category.SIXES])}\n')
        outfile.write(f'Bonus: {get_score(scores[Category.UPPER_SECTION_BONUS])}\n')
        outfile.write('\n')
        outfile.write(f'Three of a kind: {get_score(scores[Category.THREE_OF_A_KIND])}\n')
        outfile.write(f'Four of a kind: {get_score(scores[Category.FOUR_OF_A_KIND])}\n')
        outfile.write(f'Full house: {get_score(scores[Category.FULL_HOUSE])}')
        outfile.write(f'Small straight: {get_score(scores[Category.SMALL_STRAIGHT])}\n')
        outfile.write(f'Large straight: {get_score(scores[Category.LARGE_STRAIGHT])}\n')
        outfile.write(f'Yahtzee: {get_score(scores[Category.YAHTZEE])}\n')
        outfile.write(f'Chance: {get_score(scores[Category.CHANCE])}\n')
