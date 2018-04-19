import numpy as np
import random
import matplotlib.pyplot as plt

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from vizdoom import DoomGame

# vizdoom
MAP_NAME_TEMPLATE = 'map%02d'
MOVE_FORWARD = [0, 0, 0, 1, 0, 0, 0]
MOVE_BACKWARD = [0, 0, 0, 0, 1, 0, 0]
MOVE_LEFT = [1, 0, 0, 0, 0, 0, 0]
MOVE_RIGHT = [0, 1, 0, 0, 0, 0, 0]
STAY_IDLE = [0, 0, 0, 0, 0, 0, 0]
TURN_LEFT = [0, 0, 0, 0, 0, 1, 0]
TURN_RIGHT = [0, 0, 0, 0, 0, 0, 1]
ACTIONS_LIST = [MOVE_FORWARD, MOVE_BACKWARD, MOVE_LEFT, MOVE_RIGHT, STAY_IDLE, TURN_LEFT, TURN_RIGHT]
ACTION_NAMES = ['MOVE_FORWARD', 'MOVE_BACKWARD', 'MOVE_LEFT', 'MOVE_RIGHT', 'STAY_IDLE', 'TURN_LEFT', 'TURN_RIGHT']
WAIT_BEFORE_START_TICS = 140
VIZDOOM_TO_TF = [1, 2, 0]
ACTION_CLASSES = len(ACTIONS_LIST)
MIN_RANDOM_TEXTURE_MAP_INDEX = 2
MAX_RANDOM_TEXTURE_MAP_INDEX = 401
TRAIN_REPEAT = 4
NET_WIDTH = 160
NET_HEIGHT = 120
NET_CHANNELS = 3
STATE_AFTER_GAME_END = np.zeros((NET_HEIGHT, NET_WIDTH, NET_CHANNELS), dtype=np.uint8)

# general
DEFAULT_CONFIG = '/home/nsavinov/projects/gym-vizdoom/gym_vizdoom/envs/default.cfg'
TRAIN_WAD = '/home/nsavinov/projects/gym-vizdoom/gym_vizdoom/envs/D3_exploration_train.wad_manymaps.wad_exploration.wad'

class VizdoomEnv(gym.Env):
  metadata = {'render.modes': ['human', 'rgb_array']}

  def __init__(self):
    self._vizdoom_setup(TRAIN_WAD)
    self.action_space = spaces.Discrete(ACTION_CLASSES)
    self.observation_space = spaces.Box(np.array([0]), np.array([1]), dtype=np.float32)
    self.episode_reward = 0.0
    self.seed()
    self.reset()

  def seed(self, seed=None):
    if seed is not None:
      self._vizdoom_seed(seed)
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def step(self, action):
    reward = self._make_action(action)
    self.episode_reward += reward
    done = self._is_done()
    current_state = self._get_state() if not done else STATE_AFTER_GAME_END
    self.current_state = current_state
    return current_state, reward, done, {}

  def reset(self):
    print('Episode reward: {}'.format(self.episode_reward))
    self.episode_reward = 0.0
    self.game.set_doom_map(MAP_NAME_TEMPLATE % self.np_random.randint(MIN_RANDOM_TEXTURE_MAP_INDEX,
                                                                      MAX_RANDOM_TEXTURE_MAP_INDEX + 1))
    self.game.new_episode()
    return self._get_state()

  def render(self, mode='rgb_array'):
    if mode == 'rgb_array':
      return self.current_state
    elif mode == 'human':
      plt.figure(1)
      plt.clf()
      plt.imshow(self.render(mode='rgb_array'))
      plt.pause(0.001)
    else:
      super(VizdoomEnv, self).render(mode=mode)

  def _vizdoom_setup(self, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.init()
    self.game = game

  def _vizdoom_seed(self, seed):
    self.game.set_seed(seed)

  def _get_state(self):
    return self.game.get_state().screen_buffer.transpose(VIZDOOM_TO_TF)

  def _make_action(self, action_index):
    return self.game.make_action(ACTIONS_LIST[action_index], TRAIN_REPEAT)

  def _is_done(self):
    return self.game.is_episode_finished()
