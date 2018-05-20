This is a gym wrapper for all Vizdoom environments used in ICLR'18 paper https://github.com/nsavinov/SPTM. Feel free to extend it to other Vizdoom tasks. Use with python3.

# Installation
```bash
git clone https://github.com/nsavinov/gym-vizdoom.git
cd gym-vizdoom
pip install -e .
```
# Test all available envs
```
python test.py
```
# Types of envs
Brief overview below, see more details in the paper. All envs are ready for plug-n-play with RL. At each step, the env returns a concatenation of (observation, goal). Repeat of 4 is used for all envs.
## Train exploration
Those were used for training RL exploration baselines. The agent gets reward for collecting invisible healthkits (+1 each) and thus learns to explore. There are 1000 healthkits initially, they are not replenishable. Episode lasts for 2500 steps. Goal frame is provided as a special value EXPLORATION_GOAL_FRAME and concatenated with observation. Here is the gym env name:
```bash
VizdoomExplorationTrain-v0
```
## Train navigation
First 2500 steps the same as exploration. After that, 1250 steps for navigation. In addition to reward +1 for invisible healthkits, the agent gets a large reward +800 for reaching the goal. During navigation, goal frame is not masked (as during exploration). Here is the gym env name:
```bash
VizdoomNavigationTrain-v0
```
## Test/Val navigation
Same as train, but during first 2500 steps (a bit less for some envs) the agent cannot move, it only observes the exploration sequence provided to it. Afterwards, navigation as usual. Also, the rewards all always 0 besides when it reaches the goal (during navigation), in which case +800. Here is how environment names in the paper map into the names in the code:
```bash
# format:
# NAME_PAPER NAME_CODE
Test-1 VizdoomNavigationTestDeepmindSmall-v0
Test-2 VizdoomNavigationTestOpenSpaceFive-v0
Test-3 VizdoomNavigationTestStarMaze-v0
Test-4 VizdoomNavigationTestOffice1-v0
Test-5 VizdoomNavigationTestColumns-v0
Test-6 VizdoomNavigationTestOffice2-v0
Test-7 VizdoomNavigationTestTopologicalStarEasier-v0
Val-1 VizdoomNavigationValOpenSpaceTwo-v0
Val-2 VizdoomNavigationValBranching-v0
Val-3 VizdoomNavigationValDeepmindLarge-v0
```
For some of those envs, there are additional versions (used in the supplementary of the paper). Those containing "Dm" in the name use homogenious textures with sparse landmarks, "Autoexplore" -- use automatic algorithm for providing exploration sequence (for the default envs exploration sequences were provided by humans). 
# Caveats
Long file paths cause Vizdoom to hang (in particular, replay_episode method in this code). Try to install this repo as close as possible to the root.
