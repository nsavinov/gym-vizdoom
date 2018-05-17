import gym
import gym_vizdoom
env = gym.make('VizdoomNavigationDeepmindSmall-v0')
for i_episode in range(1):
  observation = env.reset()
  while True:
    # print(observation)
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print(info['step_counter'])
    print(info['status'])
    print(info['map_index'])
    print(info['goal_index'])
    if done:
      print('Episode finished!')
      break
