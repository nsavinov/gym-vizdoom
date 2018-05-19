from os import path as osp

from gym_vizdoom.envs.constants import (DATA_PATH,
                                        STATE_AFTER_GAME_END,
                                        MAP_NAME_TEMPLATE,
                                        MIN_RANDOM_TEXTURE_MAP_INDEX,
                                        MAX_RANDOM_TEXTURE_MAP_INDEX)
from gym_vizdoom.envs.util import real_get_frame

from gym_vizdoom.envs.navigation_game import NavigationGame


class NavigationTrainGame(NavigationGame):
  def __init__(self,
               dir,
               wad,
               goal_wad,
               initial_skip):
    self.goal_wad = osp.join(osp.dirname(__file__), DATA_PATH, dir, goal_wad)
    super(NavigationTrainGame, self).__init__(dir=dir, wad=wad, initial_skip=initial_skip)

  def class_specific_init(self):
    self.maps = [MAP_NAME_TEMPLATE % index for index in range(MIN_RANDOM_TEXTURE_MAP_INDEX,
                                                              MAX_RANDOM_TEXTURE_MAP_INDEX + 1)]
    self.goal_frames = []
    self.vizdoom_setup(self.goal_wad)
    for map in self.maps:
      self.game.set_doom_map(map)
      self.game.new_episode()
      self.goal_frames += [real_get_frame(self.game)]
    self.map_index = self.np_random.randint(0, len(self.maps))

  def class_specific_reset(self):
    self.map_index = self.np_random.randint(0, len(self.maps))

  def make_exploration_action(self, action_index):
    return self.real_make_action(action_index)

  def get_exploration_frame(self, done):
    return real_get_frame(self.game) if not done else STATE_AFTER_GAME_END

  def get_navigation_goal_frame(self):
    return self.goal_frames[self.map_index]

  def is_done(self):
    return self.game.is_episode_finished()

  def new_episode(self):
    self.game.set_doom_map(self.maps[self.map_index])
    self.game.new_episode()
