from gym_vizdoom.envs.navigation_test_game import NavigationTestGame
from gym_vizdoom.envs.navigation_train_game import NavigationTrainGame
from gym_vizdoom.envs.exploration_train_game import ExplorationTrainGame

GAMES = {}
GAMES['VizdoomNavigationTestDeepmindSmall'] = \
    NavigationTestGame(
        dir='Test/deepmind_small/',
        wad='deepmind_small.wad_manymaps_test.wad',
        exploration_lmp='deepmind_small.lmp',
        goal_lmps=['deepmind_small_tall_red_pillar.lmp',
                   'deepmind_small_candelabra.lmp',
                   'deepmind_small_tall_blue_torch.lmp',
                   'deepmind_small_short_green_pillar.lmp'],
        goal_locations=[(-64.0, -192.0),
                        (64.0, 64.0),
                        (320.0, -64.0),
                        (192.0, 64.0)],
        box=[-512.0, -384.0, 768.0, 256.0])
GAMES['VizdoomNavigationTestDeepmindSmallDm'] = \
    NavigationTestGame(
        dir='Test/deepmind_small_dm/',
        wad='deepmind_small.wad_manymaps_test.wad',
        exploration_lmp='deepmind_small.lmp',
        goal_lmps=['deepmind_small_tall_red_pillar.lmp',
                   'deepmind_small_candelabra.lmp',
                   'deepmind_small_tall_blue_torch.lmp',
                   'deepmind_small_short_green_pillar.lmp'],
        goal_locations=[(-64.0, -192.0),
                        (64.0, 64.0),
                        (320.0, -64.0),
                        (192.0, 64.0)],
        box=[-512.0, -384.0, 768.0, 256.0])
GAMES['VizdoomNavigationTestDeepmindSmallAutoexplore'] = \
    NavigationTestGame(
        dir='Test/deepmind_small_ae/',
        wad='deepmind_small.wad_manymaps_test.wad',
        exploration_lmp='deepmind_small.lmp',
        goal_lmps=['deepmind_small_tall_red_pillar.lmp',
                   'deepmind_small_candelabra.lmp',
                   'deepmind_small_tall_blue_torch.lmp',
                   'deepmind_small_short_green_pillar.lmp'],
        goal_locations=[(-64.0, -192.0),
                        (64.0, 64.0),
                        (320.0, -64.0),
                        (192.0, 64.0)],
        box=[-512.0, -384.0, 768.0, 256.0])
GAMES['VizdoomNavigationTestOpenSpaceFive'] = \
    NavigationTestGame(
        dir='Test/open_space_five/',
        wad='open_space_five.wad_manymaps_test.wad',
        exploration_lmp='open_space_five.lmp',
        goal_lmps=['open_space_five_tall_red_pillar.lmp',
                   'open_space_five_candelabra.lmp',
                   'open_space_five_tall_blue_torch.lmp',
                   'open_space_five_short_green_pillar.lmp'],
        goal_locations=[(1728.0, 896.0),
                        (832.0, 1728.0),
                        (832.0, 128.0),
                        (1728.0, 1152.0)],
        box=[0.0, 0.0, 1856.0, 1856.0])
GAMES['VizdoomNavigationTestStarMaze'] = \
    NavigationTestGame(
        dir='Test/star_maze/',
        wad='star_maze.wad_manymaps_test.wad',
        exploration_lmp='star_maze.lmp',
        goal_lmps=['star_maze_tall_red_pillar.lmp',
                   'star_maze_candelabra.lmp',
                   'star_maze_tall_blue_torch.lmp',
                   'star_maze_short_green_pillar.lmp'],
        goal_locations=[(-448.0, -992.0),
                        (-704.0, -320.0),
                        (736.0, -320.0),
                        (544.0, 768.0)],
        box=[-928.0, -1088.0, 1472.0, 864.0])
GAMES['VizdoomNavigationTestOffice1'] = \
    NavigationTestGame(
        dir='Test/office1/',
        wad='office1.wad_manymaps_test.wad',
        exploration_lmp='office1.lmp',
        goal_lmps=['office1_tall_red_pillar.lmp',
                   'office1_candelabra.lmp',
                   'office1_tall_blue_torch.lmp',
                   'office1_short_green_pillar.lmp'],
        goal_locations=[(320.0, 192.0),
                        (192.0, 192.0),
                        (960.0, -64.0),
                        (832.0, -576.0)],
        box=[-384.0, -640.0, 1280.0, 256.0])
GAMES['VizdoomNavigationTestOffice1Dm'] = \
    NavigationTestGame(
        dir='Test/office1_dm/',
        wad='office1.wad_manymaps_test.wad',
        exploration_lmp='office1.lmp',
        goal_lmps=['office1_tall_red_pillar.lmp',
                   'office1_candelabra.lmp',
                   'office1_tall_blue_torch.lmp',
                   'office1_short_green_pillar.lmp'],
        goal_locations=[(320.0, 192.0),
                        (192.0, 192.0),
                        (960.0, -64.0),
                        (832.0, -576.0)],
        box=[-384.0, -640.0, 1280.0, 256.0])
GAMES['VizdoomNavigationTestOffice1Autoexplore'] = \
    NavigationTestGame(
        dir='Test/office1_ae/',
        wad='office1.wad_manymaps_test.wad',
        exploration_lmp='office1.lmp',
        goal_lmps=['office1_tall_red_pillar.lmp',
                   'office1_candelabra.lmp',
                   'office1_tall_blue_torch.lmp',
                   'office1_short_green_pillar.lmp'],
        goal_locations=[(320.0, 192.0),
                        (192.0, 192.0),
                        (960.0, -64.0),
                        (832.0, -576.0)],
        box=[-384.0, -640.0, 1280.0, 256.0])
GAMES['VizdoomNavigationTestColumns'] = \
    NavigationTestGame(
        dir='Test/columns/',
        wad='columns.wad_manymaps_test.wad',
        exploration_lmp='columns.lmp',
        goal_lmps=['columns_tall_red_pillar.lmp',
                   'columns_candelabra.lmp',
                   'columns_tall_blue_torch.lmp',
                   'columns_short_green_pillar.lmp'],
        goal_locations=[(-672.0, -480.0),
                        (-224.0, 352.0),
                        (256.0, 320.0),
                        (768.0, -448.0)],
        box=[-704.0, -512.0, 832.0, 384.0])
GAMES['VizdoomNavigationTestColumnsDm'] = \
    NavigationTestGame(
        dir='Test/columns_dm/',
        wad='columns.wad_manymaps_test.wad',
        exploration_lmp='columns.lmp',
        goal_lmps=['columns_tall_red_pillar.lmp',
                   'columns_candelabra.lmp',
                   'columns_tall_blue_torch.lmp',
                   'columns_short_green_pillar.lmp'],
        goal_locations=[(-672.0, -480.0),
                        (-224.0, 352.0),
                        (256.0, 320.0),
                        (768.0, -448.0)],
        box=[-704.0, -512.0, 832.0, 384.0])
GAMES['VizdoomNavigationTestColumnsAutoexplore'] = \
    NavigationTestGame(
        dir='Test/columns_ae/',
        wad='columns.wad_manymaps_test.wad',
        exploration_lmp='columns.lmp',
        goal_lmps=['columns_tall_red_pillar.lmp',
                   'columns_candelabra.lmp',
                   'columns_tall_blue_torch.lmp',
                   'columns_short_green_pillar.lmp'],
        goal_locations=[(-672.0, -480.0),
                        (-224.0, 352.0),
                        (256.0, 320.0),
                        (768.0, -448.0)],
        box=[-704.0, -512.0, 832.0, 384.0])
GAMES['VizdoomNavigationTestOffice2'] = \
    NavigationTestGame(
        dir='Test/office2/',
        wad='office2.wad_manymaps_test.wad',
        exploration_lmp='office2.lmp',
        goal_lmps=['office2_tall_red_pillar.lmp',
                   'office2_candelabra.lmp',
                   'office2_tall_blue_torch.lmp',
                   'office2_short_green_pillar.lmp'],
        goal_locations=[(-384.0, -256.0),
                        (0.0, 0.0),
                        (352.0, -480.0),
                        (768.0, 32.0)],
        box=[-576.0, -640.0, 832.0, 320.0])
GAMES['VizdoomNavigationTestTopologicalStarEasier'] = \
    NavigationTestGame(
        dir='Test/top_star_easier/',
        wad='top_star_easier.wad_manymaps_test.wad',
        exploration_lmp='top_star_easier.lmp',
        goal_lmps=['top_star_easier_tall_red_pillar.lmp',
                   'top_star_easier_candelabra.lmp',
                   'top_star_easier_tall_blue_torch.lmp',
                   'top_star_easier_short_green_pillar.lmp'],
        goal_locations=[(-832.0, -384.0),
                        (-704.0, -128.0),
                        (960.0, -384.0),
                        (960.0, 128.0)],
        box=[-896.0, -448.0, 1024.0, 576.0])
GAMES['VizdoomNavigationValOpenSpaceTwo'] = \
    NavigationTestGame(
        dir='Val/open_space_two/',
        wad='open_space_two.wad_manymaps_test.wad',
        exploration_lmp='open_space_two.lmp',
        goal_lmps=['open_space_two_tall_red_pillar.lmp',
                   'open_space_two_candelabra.lmp',
                   'open_space_two_tall_blue_torch.lmp',
                   'open_space_two_short_green_pillar.lmp'],
        goal_locations=[(1728.0, 1600.0),
                        (1728.0, 128.0),
                        (128.0, 1728.0),
                        (128.0, 128.0)],
        box=[0.0, 0.0, 1856.0, 1856.0])
GAMES['VizdoomNavigationValBranching'] = \
    NavigationTestGame(
        dir='Val/branching/',
        wad='branching.wad_manymaps_test.wad',
        exploration_lmp='branching.lmp',
        goal_lmps=['branching_tall_red_pillar.lmp',
                   'branching_candelabra.lmp',
                   'branching_tall_blue_torch.lmp',
                   'branching_short_green_pillar.lmp'],
        goal_locations=[(192.0, -448.0),
                        (64.0, 320.0),
                        (320.0, -64.0),
                        (448.0, -320.0)],
        box=[-256.0, -768.0, 1024.0, 512.0])
GAMES['VizdoomNavigationValDeepmindLarge'] = \
    NavigationTestGame(
        dir='Val/deepmind_large/',
        wad='deepmind_large.wad_manymaps_test.wad',
        exploration_lmp='deepmind_large.lmp',
        goal_lmps=['deepmind_large_tall_red_pillar.lmp',
                   'deepmind_large_candelabra.lmp',
                   'deepmind_large_tall_blue_torch.lmp',
                   'deepmind_large_short_green_pillar.lmp'],
        goal_locations=[(576.0, -320.0),
                        (1088.0, -576.0),
                        (320.0, -192.0),
                        (704.0, -832.0)],
        box=[-640.0, -1024.0, 1280.0, 128.0])
GAMES['VizdoomNavigationValDeepmindLargeDm'] = \
    NavigationTestGame(
        dir='Val/deepmind_large_dm/',
        wad='deepmind_large.wad_manymaps_test.wad',
        exploration_lmp='deepmind_large.lmp',
        goal_lmps=['deepmind_large_tall_red_pillar.lmp',
                   'deepmind_large_candelabra.lmp',
                   'deepmind_large_tall_blue_torch.lmp',
                   'deepmind_large_short_green_pillar.lmp'],
        goal_locations=[(576.0, -320.0),
                        (1088.0, -576.0),
                        (320.0, -192.0),
                        (704.0, -832.0)],
        box=[-640.0, -1024.0, 1280.0, 128.0])
GAMES['VizdoomNavigationTrain'] = \
  NavigationTrainGame(
    dir='Train/',
    wad='D3_exploration_train.wad_manymaps.wad_navigation.wad',
    goal_wad='D3_exploration_train.wad_manymaps.wad_snapshot.wad',
    initial_skip=16)
# goal_wad is excessive, given for historical reasons
GAMES['VizdoomExplorationTrain'] = \
  ExplorationTrainGame(
    dir='Train/',
    wad='D3_exploration_train.wad_manymaps.wad_exploration.wad',
    goal_wad='D3_exploration_train.wad_manymaps.wad_snapshot.wad',
    initial_skip=16)
