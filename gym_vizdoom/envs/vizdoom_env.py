import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class VizdoomEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.action_space = spaces.Discrete(2)
    self.observation_space = spaces.Box(np.array([0]), np.array([1]), dtype=np.float32)

  def step(self, action):
    pass

  def reset(self):
    pass

  def render(self, mode='human', close=False):
    pass
