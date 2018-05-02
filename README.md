This is a wrapper for the Vizdoom exploration task which we used to train one of our RL baselines in https://github.com/nsavinov/SPTM. The agent gets reward for collecting invisible healthkits and thus learns to explore. There are 1000 healthkits initially, they are not replenishable.
Feel free to extend it to other Vizdoom tasks.

# Installation
```bash
git clone https://github.com/nsavinov/gym-vizdoom.git
cd gym-vizdoom
pip install -e .
```
