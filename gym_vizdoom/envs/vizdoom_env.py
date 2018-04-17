import numpy as np
import random

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

# general
DEFAULT_RANDOM_SEED = 100
DEFAULT_CONFIG = '/home/nsavinov/projects/gym-vizdoom/gym_vizdoom/envs/default.cfg'
TRAIN_WAD = '/home/nsavinov/projects/gym-vizdoom/gym_vizdoom/envs/D3_exploration_train.wad_manymaps.wad_exploration.wad'

class VizdoomEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    # TODO: improve seeding
    np.random.seed(DEFAULT_RANDOM_SEED)
    random.seed(DEFAULT_RANDOM_SEED)
    self._vizdoom_setup(DEFAULT_RANDOM_SEED, TRAIN_WAD)
    self.action_space = spaces.Discrete(ACTION_CLASSES)
    self.observation_space = spaces.Box(np.array([0]), np.array([1]), dtype=np.float32)

  def step(self, action):
    reward = self._make_action(action)
    done = self._is_done()
    current_state = self._get_state() if not done else None
    return current_state, reward, done, {}

  def reset(self):
    self.game.set_doom_map(MAP_NAME_TEMPLATE % random.randint(MIN_RANDOM_TEXTURE_MAP_INDEX,
                                                              MAX_RANDOM_TEXTURE_MAP_INDEX))
    self.game.new_episode()
    return self._get_state()

  def render(self, mode='human', close=False):
    pass

  def _vizdoom_setup(self, seed, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.set_seed(seed)
    game.init()
    self.game = game

  def _get_state(self):
    return self.game.get_state().screen_buffer.transpose(VIZDOOM_TO_TF)

  def _make_action(self, action_index):
    return self.game.make_action(ACTIONS_LIST[action_index], TRAIN_REPEAT)

  def _is_done(self):
    return self.game.is_episode_finished()
