This is a gym wrapper for all Vizdoom environments used in ICLR'18 paper https://github.com/nsavinov/SPTM. Feel free to extend it to other Vizdoom tasks.

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
Brief overview below, see more details in the paper. All envs are ready for plug-n-play with RL.
## Test/Val
```
TODO: names
```
## Train
Those were used for training RL baselines.
### Exploration
The agent gets reward for collecting invisible healthkits and thus learns to explore. There are 1000 healthkits initially, they are not replenishable. 
```
TODO: names
```
### Navigation
```
TODO: names
```
# Caveats
TODO
