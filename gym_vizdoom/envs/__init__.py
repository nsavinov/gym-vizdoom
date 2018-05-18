from gym_vizdoom.envs.vizdoom_navigation_env import VizdoomNavigationEnv

class VizdoomNavigationEnvDeepmindSmall(VizdoomNavigationEnv):
  def __init__(self):
    super(VizdoomNavigationEnvDeepmindSmall, self).__init__('deepmind_small')