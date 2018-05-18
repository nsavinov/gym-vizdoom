from gym_vizdoom.envs.navigation_train_game import NavigationTrainGame
from gym_vizdoom.envs.constants import MAX_STEP_EXPLORATION

class ExplorationTrainGame(NavigationTrainGame):
  def is_done(self):
    return (self.game.is_episode_finished() or
            self.step_counter >= MAX_STEP_EXPLORATION)
