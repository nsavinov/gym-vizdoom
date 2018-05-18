from abc import ABC, abstractmethod
from os import path as osp
import numpy as np

from vizdoom import DoomGame

from gym_vizdoom.envs.constants import (DEFAULT_CONFIG,
                                        ACTIONS_LIST,
                                        REPEAT,
                                        EXPLORATION_STATUS,
                                        NAVIGATION_STATUS,
                                        DATA_PATH,
                                        STATE_AFTER_GAME_END,
                                        EXPLORATION_GOAL,
                                        GOAL_EXTENDED_OBSERVATION_SHAPE,
                                        MAX_STEP_EXPLORATION)
from gym_vizdoom.envs.util import get_frame

class NavigationGame(ABC):
  def __init__(self,
               dir,
               wad):
    self.observation_shape = GOAL_EXTENDED_OBSERVATION_SHAPE
    self.wad = osp.join(osp.dirname(__file__), DATA_PATH, dir, wad)
    self.just_started = True

  def seed(self, seed):
    self.game.set_seed(seed)

  def step(self, action):
    reward = self.make_action(action)
    done = self.is_done()
    state = self.get_state(done)
    info = vars(self)
    return state, reward, done, info

  def reset(self):
    self.step_counter = 0
    self.status = EXPLORATION_STATUS
    if self.just_started:
      self.class_specific_init()
      self.vizdoom_setup(self.wad)
      self.just_started = False
    else:
      self.class_specific_reset()
    self.start_map()
    state = self.get_state(done=False)
    return state

  def start_map(self):
    self.game.set_doom_map(self.maps[self.map_index])
    self.game.new_episode()

  def vizdoom_setup(self, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.init()
    self.game = game

  def make_action(self, action_index):
    if self.status == NAVIGATION_STATUS:
      reward = self.game.make_action(ACTIONS_LIST[action_index], REPEAT)
    else:
      reward = self.make_exploration_action(action_index)
    self.step_counter += 1
    self.update_status()
    return reward

  def get_state(self, done):
    if self.status == NAVIGATION_STATUS:
      frame = get_frame(self.game) if not done else STATE_AFTER_GAME_END
      goal_frame = self.get_goal_frame()
    else:
      frame = self.get_exploration_frame()
      goal_frame = EXPLORATION_GOAL
    state = np.concatenate([frame, goal_frame], axis=2)
    return state

  def update_status(self):
    if self.status == EXPLORATION_STATUS and self.step_counter >= MAX_STEP_EXPLORATION:
      self.status = NAVIGATION_STATUS
      self.step_counter = 0

  @abstractmethod
  def make_exploration_action(self, action_index):
    pass

  @abstractmethod
  def class_specific_init(self):
    pass

  @abstractmethod
  def class_specific_reset(self):
    pass

  @abstractmethod
  def get_exploration_frame(self, done):
    pass

  @abstractmethod
  def is_done(self):
    pass

  @abstractmethod
  def get_goal_frame(self):
    pass
