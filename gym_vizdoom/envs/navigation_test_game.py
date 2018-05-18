from os import path as osp
import numpy as np

from gym_vizdoom.envs.constants import (DEFAULT_TEST_MAPS,
                                        DEFAULT_TEST_EXPLORATION_MAP,
                                        DEFAULT_TEST_GOAL_NAMES,
                                        EXPLORATION_STATUS,
                                        NAVIGATION_STATUS,
                                        DATA_PATH,
                                        EXPLORATION_GOAL,
                                        MAX_STEP_NAVIGATION,
                                        GOAL_DISTANCE_ALLOWANCE,
                                        REPEAT)
from gym_vizdoom.envs.util import (get_coordinates,
                                   load_frames_from_lmp,
                                   load_goal_frame_from_lmp)
from gym_vizdoom.envs.navigation_game import NavigationGame


class NavigationTestGame(NavigationGame):
  def __init__(self,
               dir,
               wad,
               exploration_lmp,
               goal_lmps,
               goal_locations,
               box,
               maps=DEFAULT_TEST_MAPS,
               exploration_map=DEFAULT_TEST_EXPLORATION_MAP,
               goal_names=DEFAULT_TEST_GOAL_NAMES):
    self.exploration_lmp = osp.join(osp.dirname(__file__), DATA_PATH, dir, exploration_lmp)
    self.goal_lmps = [osp.join(osp.dirname(__file__), DATA_PATH, dir, value) for value in goal_lmps]
    self.maps = maps
    self.exploration_map = exploration_map
    self.goal_locations = goal_locations
    self.goal_names = goal_names
    self.box = box
    super(NavigationTestGame, self).__init__(dir=dir, wad=wad)

  def _load_exploration_frames(self):
    self._vizdoom_setup(self.wad)
    self.exploration_frames = load_frames_from_lmp(self.game,
                                                   self.exploration_lmp,
                                                   REPEAT)

  def _make_exploration_action(self, action_index):
    return 0

  def _just_started_setup(self):
    self._load_exploration_frames()
    self._load_goal_frames()
    self.map_index = 0
    self.goal_index = 0

  def _running_update(self):
    self.goal_index = (self.goal_index + 1) % len(self.goal_lmps)
    if self.goal_index == 0:
      self.map_index = (self.map_index + 1) % len(self.maps)

  def _load_goal_frames(self):
    self.goal_frames = []
    for goal_index in range(len(self.goal_lmps)):
      self._vizdoom_setup(self.wad)
      self.goal_frames += [load_goal_frame_from_lmp(self.game,
                                                    self.goal_lmps[goal_index])]

  def _get_exploration_state(self, done):
    frame = self.exploration_frames[self.step_counter]
    goal_frame = EXPLORATION_GOAL
    return np.concatenate([frame, goal_frame], axis=2)

  def _is_done(self):
    if self.status == NAVIGATION_STATUS:
      if self.step_counter >= MAX_STEP_NAVIGATION:
        return True
      distance_to_goal = np.linalg.norm(np.array(get_coordinates(self.game)) -
                                        np.array(self.goal_locations[self.goal_index]))
      if distance_to_goal <= GOAL_DISTANCE_ALLOWANCE:
        print('Goal reached!')
        return True
    return False

  def _update_status(self):
    if self.status == EXPLORATION_STATUS and self.step_counter >= len(self.exploration_frames):
      self.status = NAVIGATION_STATUS
      self.step_counter = 0

  def _get_goal_frame(self):
    return self.goal_frames[self.goal_index]
