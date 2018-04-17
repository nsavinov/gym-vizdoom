from gym.envs.registration import register

register(
  id='vizdoom-v0',
  entry_point='gym_vizdoom.envs:VizdoomEnv',
)
