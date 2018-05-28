from abc import ABC, abstractmethod
from os import path as osp
import numpy as np

from gym.utils import seeding

from vizdoom import DoomGame

from gym_vizdoom.envs.constants import (DEFAULT_CONFIG,
                                        ACTIONS_LIST,
                                        REPEAT,
                                        EXPLORATION_STATUS,
                                        NAVIGATION_STATUS,
                                        DATA_PATH,
                                        STATE_AFTER_GAME_END,
                                        EXPLORATION_GOAL_FRAME,
                                        GOAL_EXTENDED_OBSERVATION_SHAPE,
                                        MAX_STEP_EXPLORATION,
                                        STAY_IDLE)
from gym_vizdoom.envs.util import real_get_frame

class NavigationGame(ABC):
  def __init__(self,
               dir,
               wad,
               initial_skip=0):
    self.initial_skip = initial_skip // REPEAT
    self.observation_shape = GOAL_EXTENDED_OBSERVATION_SHAPE
    self.wad = osp.join(osp.dirname(__file__), DATA_PATH, dir, wad)
    self.just_started = True
    self.just_started_seed = None

  def seed(self, seed):
    if seed is not None:
      if not self.just_started:
        self.game.set_seed(seed)
      else:
        self.just_started_seed = seed
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def step(self, action):
    reward = self.make_action(action)
    done = self.is_done()
    state = self.get_state(done)
    info = vars(self).copy()
    info.pop('game', None) # infos for openai baselines need to be picklable, game is not
    return state, self.reward_shaping(reward), done, info

  def reset(self):
    self.step_counter = 0
    self.status = EXPLORATION_STATUS
    if self.just_started:
      self.class_specific_init()
      self.vizdoom_setup(self.wad)
      if self.just_started_seed:
        self.game.set_seed(self.just_started_seed)
      self.just_started = False
    else:
      self.class_specific_reset()
    self.new_episode()
    for _ in range(self.initial_skip):
      self.stay_idle()
    state = self.get_state(done=False)
    return state

  def stay_idle(self):
    self.game.make_action(STAY_IDLE, REPEAT)

  def vizdoom_setup(self, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.init()
    self.game = game

  def make_action(self, action_index):
    if self.status == NAVIGATION_STATUS:
      reward = self.make_navigation_action(action_index)
    else:
      reward = self.make_exploration_action(action_index)
    self.step_counter += 1
    self.update_status()
    return reward

  def make_navigation_action(self, action_index):
    return self.real_make_action(action_index)

  def real_make_action(self, action_index):
    return self.game.make_action(ACTIONS_LIST[action_index], REPEAT)

  def get_state(self, done):
    if self.status == NAVIGATION_STATUS:
      frame = self.get_navigation_frame(done)
      goal_frame = self.get_navigation_goal_frame()
    else:
      frame = self.get_exploration_frame(done)
      goal_frame = EXPLORATION_GOAL_FRAME
    state = np.concatenate([frame, goal_frame], axis=2)
    return state

  def get_navigation_frame(self, done):
    return real_get_frame(self.game) if not done else STATE_AFTER_GAME_END

  def update_status(self):
    if self.status == EXPLORATION_STATUS and self.step_counter >= MAX_STEP_EXPLORATION:
      self.status = NAVIGATION_STATUS
      self.step_counter = 0

  @abstractmethod
  def reward_shaping(self, reward):
    pass

  @abstractmethod
  def class_specific_init(self):
    pass

  @abstractmethod
  def class_specific_reset(self):
    pass

  @abstractmethod
  def make_exploration_action(self, action_index):
    pass

  @abstractmethod
  def get_exploration_frame(self, done):
    pass

  @abstractmethod
  def get_navigation_goal_frame(self):
    pass

  @abstractmethod
  def is_done(self):
    pass

  @abstractmethod
  def new_episode(self):
    pass
