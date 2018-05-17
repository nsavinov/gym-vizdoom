from os import path as osp
import numpy as np

from vizdoom import DoomGame

from gym_vizdoom.envs import (NET_HEIGHT,
                              NET_WIDTH,
                              NET_CHANNELS,
                              DEFAULT_CONFIG,
                              ACTIONS_LIST,
                              VIZDOOM_TO_TF,
                              REPEAT)

STATE_AFTER_GAME_END = np.zeros((NET_HEIGHT, NET_WIDTH, NET_CHANNELS), dtype=np.uint8)
EXPLORATION_GOAL = np.zeros((NET_HEIGHT, NET_WIDTH, NET_CHANNELS), dtype=np.uint8) - 1
MAX_STEP_NAVIGATION = 5000 // REPEAT
GOAL_DISTANCE_ALLOWANCE = 63

DATA_PATH = 'data'
DEFAULT_MAPS = ['map02', 'map03', 'map04', 'map05']
DEFAULT_EXPLORATION_MAP = 'map06'
DEFAULT_GOAL_NAMES = ['tall_red_pillar',
                      'candelabra',
                      'tall_blue_torch',
                      'short_green_pillar']


def get_state(game):
  return game.get_state().screen_buffer.transpose(VIZDOOM_TO_TF)

def load_frames_from_lmp(game, lmp, skip):
  game.replay_episode(lmp)
  frames = []
  counter = 0
  while not game.is_episode_finished():
    frame = get_state(game)
    if counter % skip == 0:
      frames.append(frame)
    game.advance_action()
    counter += 1
  return frames

def load_goal_frame_from_lmp(game, lmp):
  frames = load_frames_from_lmp(game, lmp, 1)
  return frames[-1]

EXPLORATION_STATUS = 0
NAVIGATION_STATUS = 1

class NavigationGame:
  def __init__(self,
               dir,
               wad,
               exploration_lmp,
               goal_lmps,
               goal_locations,
               box,
               maps=DEFAULT_MAPS,
               exploration_map=DEFAULT_EXPLORATION_MAP,
               goal_names=DEFAULT_GOAL_NAMES):
    self.observation_shape = [NET_HEIGHT, NET_WIDTH, 2 * NET_CHANNELS]
    self.wad = osp.join(osp.dirname(__file__), DATA_PATH, dir, wad)
    self.exploration_lmp = osp.join(osp.dirname(__file__), DATA_PATH, dir, exploration_lmp)
    self.goal_lmps = [osp.join(osp.dirname(__file__), DATA_PATH, dir, value) for value in goal_lmps]
    self.maps = maps
    self.exploration_map = exploration_map
    self.goal_locations = goal_locations
    self.goal_names = goal_names
    self.box = box
    self._load_exploration_frames()
    self._load_goal_frames()
    self._vizdoom_setup(self.wad)
    self.just_started = True

  def seed(self, seed):
    self.game.set_seed(seed)

  def reset(self):
    self.step_counter = 0
    self.status = EXPLORATION_STATUS
    if self.just_started:
      self.map_index = 0
      self.goal_index = 0
      self.just_started = False
    else:
      self.goal_index = (self.goal_index + 1) % len(self.goal_lmps)
      if self.goal_index == 0:
        self.map_index = (self.map_index + 1) % len(self.maps)
    self._start_map()
    state = self._get_state(done=False)
    return state

  def step(self, action):
    reward = self._make_action(action)
    self.step_counter += 1
    self._update_status()
    done = self._is_done()
    state = self._get_state(done)
    info = vars(self)
    info['coordinates'] = self._get_coordinates(done)
    return state, reward, done, info
    pass

  def _start_map(self):
    self.game.set_doom_map(self.maps[self.map_index])
    self.game.new_episode()

  def _get_coordinates(self, done):
    if not done:
      return self.game.get_state().game_variables[:2]
    else:
      return None

  def _load_exploration_frames(self):
    self._vizdoom_setup(self.wad)
    self.exploration_frames = load_frames_from_lmp(self.game, self.exploration_lmp, REPEAT)

  def _load_goal_frames(self):
    self.goal_frames = []
    for goal_index in range(len(self.goal_lmps)):
      self._vizdoom_setup(self.wad)
      self.goal_frames += [load_goal_frame_from_lmp(self.game, self.goal_lmps[goal_index])]

  def _vizdoom_setup(self, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.init()
    self.game = game

  def _get_state(self, done):
    if self.status == NAVIGATION_STATUS:
      frame = get_state(self.game) if not done else STATE_AFTER_GAME_END
      goal_frame = self._get_goal_frame()
    else:
      frame = self.exploration_frames[self.step_counter]
      goal_frame = EXPLORATION_GOAL
    state = np.concatenate([frame, goal_frame], axis=2)
    return state

  def _make_action(self, action_index):
    if self.status == NAVIGATION_STATUS:
      return self.game.make_action(ACTIONS_LIST[action_index], REPEAT)

  def _is_done(self):
    if self.status == NAVIGATION_STATUS and (self.step_counter >= MAX_STEP_NAVIGATION):
      return True
    distance_to_goal = np.linalg.norm(np.array(self._get_coordinates(False)) - np.array(self.goal_locations[self.goal_index]))
    if self.status == EXPLORATION_STATUS and distance_to_goal <= GOAL_DISTANCE_ALLOWANCE:
      return True
    return False

  def _update_status(self):
    if self.status == EXPLORATION_STATUS and self.step_counter >= len(self.exploration_frames):
      self.status = NAVIGATION_STATUS
      self.step_counter = 0

  def _get_goal_frame(self):
    return self.goal_frames[self.goal_index]
