from collections import defaultdict
from enum import Enum
import logging
import sys
from typing import Dict, Optional, Sequence

from gym import Env, spaces

import numpy as np

from pyhtzee import Pyhtzee
from pyhtzee.classes import Category, PyhtzeeException, Rule


log = logging.getLogger(__name__)


class GameType(Enum):
    SUDDEN_DEATH = 0,
    RETRY_ON_WRONG_ACTION = 1


def get_score(score: Optional[int]) -> int:
    return score if score is not None else -1


def get_dice_face_counts(dice: Sequence[int]) -> Dict[int, int]:
    faces: Dict[int, int] = defaultdict(int)
    for die in dice:
        faces[die] += 1
    return faces


class YahtzeeSingleEnv(Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,
                 rule: Rule = Rule.YAHTZEE_FREE_CHOICE_JOKER,
                 game_type: GameType = GameType.RETRY_ON_WRONG_ACTION,
                 seed=None):
        self.pyhtzee = Pyhtzee(seed=seed)
        self.rule = rule
        self.game_type = game_type
        self.action_space = spaces.Discrete(44)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(13),  # round
            spaces.Discrete(4),  # sub-round
            spaces.Box(low=1, high=6, shape=(1,), dtype=np.uint8),  # die 1
            spaces.Box(low=1, high=6, shape=(1,), dtype=np.uint8),  # die 2
            spaces.Box(low=1, high=6, shape=(1,), dtype=np.uint8),  # die 3
            spaces.Box(low=1, high=6, shape=(1,), dtype=np.uint8),  # die 4
            spaces.Box(low=1, high=6, shape=(1,), dtype=np.uint8),  # die 5
            spaces.Box(low=0, high=5, shape=(1,), dtype=np.uint8),  # face 1 count
            spaces.Box(low=0, high=5, shape=(1,), dtype=np.uint8),  # face 2 count
            spaces.Box(low=0, high=5, shape=(1,), dtype=np.uint8),  # face 3 count
            spaces.Box(low=0, high=5, shape=(1,), dtype=np.uint8),  # face 4 count
            spaces.Box(low=0, high=5, shape=(1,), dtype=np.uint8),  # face 5 count
            spaces.Box(low=0, high=5, shape=(1,), dtype=np.uint8),  # face 6 count
            spaces.Box(low=-1, high=5, shape=(1,), dtype=np.int16),  # aces
            spaces.Box(low=-1, high=10, shape=(1,), dtype=np.int16),  # twos
            spaces.Box(low=-1, high=15, shape=(1,), dtype=np.int16),  # threes
            spaces.Box(low=-1, high=20, shape=(1,), dtype=np.int16),  # fours
            spaces.Box(low=-1, high=25, shape=(1,), dtype=np.int16),  # fives
            spaces.Box(low=-1, high=30, shape=(1,), dtype=np.int16),  # sixes
            spaces.Box(low=-1, high=30, shape=(1,), dtype=np.int16),  # three of a kind
            spaces.Box(low=-1, high=30, shape=(1,), dtype=np.int16),  # four of a kind
            spaces.Box(low=-1, high=25, shape=(1,), dtype=np.int16),  # full house
            spaces.Box(low=-1, high=30, shape=(1,), dtype=np.int16),  # small straight
            spaces.Box(low=-1, high=40, shape=(1,), dtype=np.int16),  # large straight
            spaces.Box(low=-1, high=30, shape=(1,), dtype=np.int16),  # chance
            spaces.Box(low=-1, high=50, shape=(1,), dtype=np.int16),  # yahtzee
            spaces.Box(low=-1, high=35, shape=(1,), dtype=np.int16),  # upper bonus
            spaces.Box(low=-1, high=1200, shape=(1,), dtype=np.int16),  # yahtzee bonus
        ))

    def get_observation_space(self):
        pyhtzee = self.pyhtzee
        faces = get_dice_face_counts(pyhtzee.dice)
        return (
            pyhtzee.round,
            pyhtzee.sub_round,
            pyhtzee.dice[0],
            pyhtzee.dice[1],
            pyhtzee.dice[2],
            pyhtzee.dice[3],
            pyhtzee.dice[4],
            faces[1],
            faces[2],
            faces[3],
            faces[4],
            faces[5],
            faces[6],
            get_score(pyhtzee.scores.get(Category.ACES)),
            get_score(pyhtzee.scores.get(Category.TWOS)),
            get_score(pyhtzee.scores.get(Category.THREES)),
            get_score(pyhtzee.scores.get(Category.FOURS)),
            get_score(pyhtzee.scores.get(Category.FIVES)),
            get_score(pyhtzee.scores.get(Category.SIXES)),
            get_score(pyhtzee.scores.get(Category.THREE_OF_A_KIND)),
            get_score(pyhtzee.scores.get(Category.FOUR_OF_A_KIND)),
            get_score(pyhtzee.scores.get(Category.FULL_HOUSE)),
            get_score(pyhtzee.scores.get(Category.SMALL_STRAIGHT)),
            get_score(pyhtzee.scores.get(Category.LARGE_STRAIGHT)),
            get_score(pyhtzee.scores.get(Category.CHANCE)),
            get_score(pyhtzee.scores.get(Category.YAHTZEE)),
            get_score(pyhtzee.scores.get(Category.UPPER_SECTION_BONUS)),
            get_score(pyhtzee.scores.get(Category.YAHTZEE_BONUS)),
        )

    def sample_action(self):
        action = self.pyhtzee.sample_action()
        log.info(f'Sampled action: {action}')
        return action

    def step(self, action: int):
        pyhtzee = self.pyhtzee
        try:
            reward = pyhtzee.take_action(action)
            finished = pyhtzee.is_finished()
        except PyhtzeeException:
            if self.game_type == GameType.SUDDEN_DEATH:
                log.info('Invalid action, terminating round.')
                reward = -pyhtzee.get_total_score()
                finished = True
            else:  # retry on wrong action
                log.info('Invalid action, step ignored.')
                reward = 0
                finished = False

        log.info(f'Finished step. Reward: {reward}, Finished: {finished}')
        return self.get_observation_space(), reward, finished, {}

    def reset(self):
        self.pyhtzee = Pyhtzee()

    def render(self, mode='human', close=False):
        dice = self.pyhtzee.dice
        outfile = sys.stdout
        outfile.write(f'Dice: {dice[0]} {dice[1]} {dice[2]} {dice[3]} {dice[4]} '
                      f'Round: {self.pyhtzee.round}.{self.pyhtzee.sub_round} '
                      f'Score: {self.pyhtzee.get_total_score()}\n')
