import numpy as np

import gym
from gym import error, spaces, utils

from gym_vizdoom.envs.constants import ACTION_CLASSES
from gym_vizdoom.envs.register_games import GAMES


class VizdoomEnv(gym.Env):
  def __init__(self, game_name):
    self.game = GAMES[game_name]
    self.action_space = spaces.Discrete(ACTION_CLASSES)
    self.observation_space = spaces.Box(0, 255, self.game.observation_shape, dtype=np.float32)
    self.seed()

  def seed(self, seed=None):
    return self.game.seed(seed)

  def step(self, action):
    return self.game.step(action)

  def reset(self):
    return self.game.reset()

  def render(self, mode='rgb_array'):
    raise NotImplementedError('Rendering is not implemented!')
