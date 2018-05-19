import gym
from gym_vizdoom import (LIST_OF_ENVS, EXPLORATION_GOAL_FRAME)
from gym_vizdoom.logging.navigation_video_writer import NavigationVideoWriter

def test(env, video_writer, number_of_episodes):
  for _ in range(number_of_episodes):
    observation = env.reset()
    c = observation.shape[2] // 2
    current = observation[..., :c]
    goal = observation[..., c:]
    video_writer.write(current, goal)
    step = 0
    while True:
      step += 1
      action = env.action_space.sample()
      observation, reward, done, info = env.step(action)
      c = observation.shape[2] // 2
      current = observation[..., :c]
      goal = observation[..., c:]
      video_writer.write(current, goal)
      print('step:', step)
      print('reward:', reward)
      print('status:', 'exploration' if goal == EXPLORATION_GOAL_FRAME else 'navigation')
      if done:
        print('Episode finished!')
        break

def main():
  print('All possible env names:', LIST_OF_ENVS)
  just_started = True
  for env_name in LIST_OF_ENVS:
    print('Testing env: {}'.format(env_name))
    env = gym.make(env_name)
    if just_started:
      video_writer = NavigationVideoWriter('output.mov',
                                           env.observation_space.shape)
      just_started = False
    test(env, video_writer, 1)

if __name__ == '__main__':
  main()
