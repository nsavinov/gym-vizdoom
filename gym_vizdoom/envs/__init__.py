from gym_vizdoom.envs.vizdoom_env import VizdoomEnv

from gym_vizdoom.envs.constants import EXPLORATION_GOAL_FRAME
from gym_vizdoom.envs.register_games import GAMES

template = """
class {}(VizdoomEnv):
  def __init__(self):
    super({}, self).__init__('{}')
"""
GAME_NAMES = GAMES.keys()
for game_name in GAME_NAMES:
  exec(template.format(game_name, game_name, game_name))
