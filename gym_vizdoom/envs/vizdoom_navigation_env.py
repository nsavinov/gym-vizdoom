import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_vizdoom.envs import ACTION_CLASSES
from gym_vizdoom.envs.register_navigation_games import register_navigation_games

NAVIGATION_GAMES = register_navigation_games()


class VizdoomNavigationEnv(gym.Env):
  def __init__(self, navigation_game_name):
    self.navigation_game = NAVIGATION_GAMES[navigation_game_name]
    self.action_space = spaces.Discrete(ACTION_CLASSES)
    self.observation_space = spaces.Box(0, 255, self.navigation_game.observation_shape, dtype=np.float32)
    self.episode_reward = 0.0
    self.seed()
    self.reset()

  def seed(self, seed=None):
    if seed is not None:
      self.navigation_game.seed(seed)
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def step(self, action):
    return self.navigation_game.step(action)

  def reset(self):
    return self.navigation_game.reset()

  def render(self, mode='rgb_array'):
    raise NotImplementedError('Rendering is not implemented!')

