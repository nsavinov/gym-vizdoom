from os import path as osp
import numpy as np

from gym_vizdoom.envs.constants import (DEFAULT_TEST_MAPS,
                                        DEFAULT_TEST_EXPLORATION_MAP,
                                        DEFAULT_TEST_GOAL_NAMES,
                                        NAVIGATION_STATUS,
                                        DATA_PATH,
                                        MAX_STEP_NAVIGATION,
                                        GOAL_DISTANCE_ALLOWANCE,
                                        REPEAT,
                                        MAX_STEP_EXPLORATION,
                                        EXPLORATION_STATUS,
                                        GOAL_REACHING_REWARD)
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

  def make_exploration_action(self, action_index):
    return 0

  def class_specific_init(self):
    self.load_exploration_frames()
    self.load_goal_frames()
    self.map_index = 0
    self.goal_index = 0

  def class_specific_reset(self):
    self.goal_index = (self.goal_index + 1) % len(self.goal_lmps)
    if self.goal_index == 0:
      self.map_index = (self.map_index + 1) % len(self.maps)

  def get_exploration_frame(self, done):
    return self.exploration_frames[self.step_counter]

  def check_goal_reached(self):
    distance_to_goal = np.linalg.norm(np.array(get_coordinates(self.game)) -
                                      np.array(self.goal_locations[self.goal_index]))
    if distance_to_goal <= GOAL_DISTANCE_ALLOWANCE:
      return True
    return False

  def is_done(self):
    if self.status == NAVIGATION_STATUS:
      if self.step_counter >= MAX_STEP_NAVIGATION:
        return True
      return self.check_goal_reached()
    return False

  def reward_shaping(self, reward):
    if self.status == NAVIGATION_STATUS and self.check_goal_reached():
      return GOAL_REACHING_REWARD
    else:
      return 0


  def get_navigation_goal_frame(self):
    return self.goal_frames[self.goal_index]

  def new_episode(self):
    self.game.set_doom_map(self.maps[self.map_index])
    self.game.new_episode()

  def load_exploration_frames(self):
    self.vizdoom_setup(self.wad)
    self.exploration_frames = load_frames_from_lmp(self.game,
                                                   self.exploration_lmp,
                                                   REPEAT)
    # assert len(self.exploration_frames) >= MAX_STEP_EXPLORATION

  def load_goal_frames(self):
    self.goal_frames = []
    for goal_index in range(len(self.goal_lmps)):
      self.vizdoom_setup(self.wad)
      self.goal_frames += [load_goal_frame_from_lmp(self.game,
                                                    self.goal_lmps[goal_index])]

  def update_status(self):
    if self.status == EXPLORATION_STATUS and (self.step_counter >= MAX_STEP_EXPLORATION or
                                              self.step_counter >= len(self.exploration_frames)):
      self.status = NAVIGATION_STATUS
      self.step_counter = 0
