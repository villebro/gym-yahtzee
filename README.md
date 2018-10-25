[![Build Status](https://travis-ci.com/villebro/gym-yahtzee.svg?branch=master)](https://travis-ci.com/villebro/gym-yahtzee)
[![codecov](https://codecov.io/gh/villebro/gym-yahtzee/branch/master/graph/badge.svg)](https://codecov.io/gh/villebro/gym-yahtzee)
[![Requirements Status](https://requires.io/github/villebro/gym-yahtzee/requirements.svg?branch=master)](https://requires.io/github/villebro/gym-yahtzee/requirements/?branch=master)

# gym-yahtzee #

Yahtzee game using OpenAI Gym meant to be used specifically for Reinforcement Learning.

## Example ##

To run a single game run the code below. As Gym doesn't support changing the 
`action_space` during a run, gym-yahtzee provides the function `env.sample_action()` which
only samples from valid actions, e.g. no dice reroll after three rolls. Calling
`env.action_space.sample()` also works, but will take longer to complete.

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

### Updating dependencies ###

```bash
pip-compile -U --output-file requirements.txt setup.py requirements-dev.in
```
