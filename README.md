This is a wrapper for the Vizdoom exploration task which was used to train one of RL baselines in ICLR'18 paper https://github.com/nsavinov/SPTM. The agent gets reward for collecting invisible healthkits and thus learns to explore. There are 1000 healthkits initially, they are not replenishable. See more details in the paper.
Feel free to extend it to other Vizdoom tasks.

# Installation
```bash
git clone https://github.com/nsavinov/gym-vizdoom.git
cd gym-vizdoom
pip install -e .
```
