import gym
import gym_vizdoom

env = gym.make('vizdoom-v0')

for i_episode in range(2):
  observation = env.reset()
  for t in range(17000):
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    env.render(mode='human')
    print(reward)
    if done:
      print("Episode finished after {} timesteps".format(t+1))
      break
