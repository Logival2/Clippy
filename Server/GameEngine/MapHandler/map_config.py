from collections import OrderedDict


MAP_CONFIG = {
    'seed': 1,
    'regions_nbr': 5,
    'map_size': 64,
    'chunk_size': 64,
    'noise_scale': 15,  # Bigger = Zoom in
    'random_bloc_swaps_frequency': 0.1,
    'regions': {
        'desert': {
            'repartition': [
                ('grass', 0.32),
                ('sand', 0.75),
                ('gravel', 0.78),
                ('sand', 0.85),
                ('stone', 1),
            ],
            'random_bloc_swaps_frequency': 70,
        },
        'mountain': {
            'repartition': [
                ('sand', 0.15),
                ('gravel', 0.3),
                ('stone', 1),
            ],
            'random_bloc_swaps_frequency': 10,
        },
        'temperate': {
            'repartition': [
                ('water', .1),
                ('gravel', .2),
                ('grass', .7),
                ('stone', .8),
            ],
            'random_bloc_swaps_frequency': 20,
        },
        'hell': {
            'repartition': [
                ('lava', .3),
            ],
            'random_bloc_swaps_frequency': 90,
        },
        'ocean': {
            'repartition': [
                ('water', 0.8),
                ('sand', 0.9),
                ('grass', 1),
            ],
            'random_bloc_swaps_frequency': 2,
        },
    }
}
