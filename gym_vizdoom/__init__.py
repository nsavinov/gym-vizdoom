from gym.envs.registration import register
from gym_vizdoom.envs.vizdoom_env import MAX_STEP

register(
  id='vizdoom-v0',
  entry_point='gym_vizdoom.envs:VizdoomEnv',
)
