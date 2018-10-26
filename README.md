[![Build Status](https://travis-ci.com/villebro/gym-yahtzee.svg?branch=master)](https://travis-ci.com/villebro/gym-yahtzee)
[![codecov](https://codecov.io/gh/villebro/gym-yahtzee/branch/master/graph/badge.svg)](https://codecov.io/gh/villebro/gym-yahtzee)
[![Requirements Status](https://requires.io/github/villebro/gym-yahtzee/requirements.svg?branch=master)](https://requires.io/github/villebro/gym-yahtzee/requirements/?branch=master)
[![PyPI version](https://img.shields.io/pypi/v/gym-yahtzee.svg)](https://badge.fury.io/py/gym-yahtzee)
[![PyPI](https://img.shields.io/pypi/pyversions/gym-yahtzee.svg)](https://www.python.org/downloads/)
# gym-yahtzee #

Yahtzee game using OpenAI Gym meant to be used specifically for Reinforcement Learning.
The rules are a loose interpretation of the free choice Joker rule, where an extra yahtzee 
cannot be substituted for a straight, where upper section usage isn't enforced for extra 
yahtzees. The maximum score is 1505, as opposed to 1375 using traditional forced choice
Joker rules. In practice this doesn't affect gameplay significantly.

## Example ##

To run a single game try the code below. As Gym doesn't support changing the 
`action_space` during a run, gym-yahtzee provides the function `env.sample_action()` which
only samples from valid actions, e.g. no dice reroll after three rolls. Calling
`env.action_space.sample()` also works, but will take longer to complete. Calling an
invalid action results in a reward of zero and replaying the round.

```python
from gym_yahtzee.envs.yahtzee_env import YahtzeeSingleEnv
import gym

env: YahtzeeSingleEnv = gym.make('yahtzee-single-v0')
env.reset()
for t in range(1000):
    env.render()
    action = env.sample_action()
    observation, reward, done, info = env.step(action)
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break
```

## Developers guide ##

Pipenv is recommended for setting up a development environment. Prior to installing
`pipenv`, creating a `.env` file with the following contents is recommended:

```
PYTHONPATH=.
```

To install pipenv and the required dependencies run the following commands:

```bash
pip install pipenv
pipenv install -r requirements.txt
pipenv shell
```

### Updating dependencies ###

`requirements.txt` is dynamically generated using `pip-compile`. To regenerate the
`requirements.txt`file run the following command:

```bash
pip-compile -U --output-file requirements.txt setup.py requirements-dev.in
```
