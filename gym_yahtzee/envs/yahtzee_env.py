import gym
from gym import error, spaces, utils
from gym.utils import seeding

import gym_yahtzee.state

import numpy as np

import sys


class YahtzeeSingleEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    state = gym_yahtzee.state.State()

    def __init__(self):
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

    def step(self, action: int):
        reward = self.state.take_action(action)

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        dice = self.state.dice
        outfile = sys.stdout
        outfile.write(f'Dice {dice[0]} {dice[1]} {dice[2]} {dice[3]} {dice[4]} \n')
        outfile.write('Dice rolls ' + '\n')
        outfile.write('\n')
        outfile.write('Aces ' + '\n')
        outfile.write('Twos ' + '\n')
        outfile.write('Threes ' + '\n')
        outfile.write('Fours ' + '\n')
        outfile.write('Fives ' + '\n')
        outfile.write('Sixes ' + '\n')
        outfile.write('Bonus ' + '\n')
        outfile.write('\n')
        outfile.write('Three of a kind ' + '\n')
        outfile.write('Four of a kind ' + '\n')
        outfile.write('Full house ' + '\n')
        outfile.write('Small straight ' + '\n')
        outfile.write('Large straight ' + '\n')
        outfile.write('Yahtzee ' + '\n')
        outfile.write('Chance ' + '\n')
