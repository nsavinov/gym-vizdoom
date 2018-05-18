from gym_vizdoom.envs.navigation_game import NavigationGame

class NavigationTrainGame(NavigationGame):
  pass

class VizdoomEnv(gym.Env):
  metadata = {'render.modes': ['human', 'rgb_array']}

  def __init__(self):
    self._vizdoom_setup(TRAIN_WAD)
    self.action_space = spaces.Discrete(ACTION_CLASSES)
    self.observation_space = spaces.Box(0, 255, [NET_HEIGHT, NET_WIDTH, NET_CHANNELS], dtype=np.float32)
    self.episode_reward = 0.0
    self.seed()
    self.reset()

  def seed(self, seed=None):
    if seed is not None:
      self._vizdoom_seed(seed)
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def step(self, action):
    reward = self._make_action(action)
    self.episode_reward += reward
    current_state, done = self._safe_get_set_state()
    self.step_counter += 1
    if self.step_counter >= MAX_STEP:
      done = True
    return current_state, reward, done, {}

  def reset(self):
    # print('Episode reward: {}'.format(self.episode_reward))
    self.episode_reward = 0.0
    self.game.set_doom_map(MAP_NAME_TEMPLATE % self.np_random.randint(MIN_RANDOM_TEXTURE_MAP_INDEX,
                                                                      MAX_RANDOM_TEXTURE_MAP_INDEX + 1))
    self.game.new_episode()
    current_state, _ = self._safe_get_set_state()
    self.step_counter = 0
    return current_state

  def render(self, mode='rgb_array'):
    # self.show_human()
    if mode in ['rgb_array', 'human']:
      return self.current_state
    else:
      super(VizdoomEnv, self).render(mode=mode)

  def show_human(self):
    plt.figure(1)
    plt.clf()
    plt.imshow(self.render(mode='rgb_array'))
    plt.pause(0.001)

  def _vizdoom_setup(self, wad):
    game = DoomGame()
    game.load_config(DEFAULT_CONFIG)
    game.set_doom_scenario_path(wad)
    game.init()
    self.game = game

  def _vizdoom_seed(self, seed):
    self.game.set_seed(seed)

  def _safe_get_set_state(self):
    done = self._is_done()
    current_state = self._get_state() if not done else STATE_AFTER_GAME_END
    self.current_state = current_state
    # self.render(mode='human')
    return current_state, done

  def _get_state(self):
    return self.game.get_state().screen_buffer.transpose(VIZDOOM_TO_TF)

  def _make_action(self, action_index):
    return self.game.make_action(ACTIONS_LIST[action_index], TRAIN_REPEAT)

  def _is_done(self):
    return self.game.is_episode_finished()