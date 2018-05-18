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
                                        MAX_STEP_NAVIGATION,
                                        GOAL_EXTENDED_OBSERVATION_SHAPE)
from gym_vizdoom.envs.util import get_state

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
    reward = self._make_action(action)
    done = self._is_done()
    state = self._get_state(done)
    info = vars(self)
    return state, reward, done, info

  def reset(self):
    self.step_counter = 0
    self.status = EXPLORATION_STATUS
    if self.just_started:
      self._just_started_setup()
      self._vizdoom_setup(self.wad)
      self.just_started = False
    else:
      self._running_update()
    self._start_map()
    state = self._get_state(done=False)
    return state

  def _start_map(self):
    self.game.set_doom_map(self.maps[self.map_index])
    self.game.new_episode()

  def _vizdoom_setup(self, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.init()
    self.game = game

  def _make_action(self, action_index):
    if self.status == NAVIGATION_STATUS:
      reward = self.game.make_action(ACTIONS_LIST[action_index], REPEAT)
    else:
      reward = self._make_exploration_action(action_index)
    self.step_counter += 1
    self._update_status()
    return reward

  def _get_state(self, done):
    if self.status == NAVIGATION_STATUS:
      state = self._get_navigation_state(done)
    else:
      state = self._get_exploration_state(done)
    return state

  def _get_navigation_state(self, done):
    frame = get_state(self.game) if not done else STATE_AFTER_GAME_END
    goal_frame = self._get_goal_frame()
    return np.concatenate([frame, goal_frame], axis=2)

  @abstractmethod
  def _make_exploration_action(self, action_index):
    pass

  @abstractmethod
  def _just_started_setup(self):
    pass

  @abstractmethod
  def _running_update(self):
    pass

  @abstractmethod
  def _load_goal_frames(self):
    pass

  @abstractmethod
  def _get_exploration_state(self, done):
    pass

  @abstractmethod
  def _is_done(self):
    pass

  @abstractmethod
  def _update_status(self):
    pass

  @abstractmethod
  def _get_goal_frame(self):
    pass
