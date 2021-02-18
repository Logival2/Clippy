from collections import OrderedDict


MAP_CONFIG = {
    'seed': 21879,
    'regions_nbr': 8,
    'map_size': 128,
    'chunk_size': 24,
    'noise_scale': 15,  # Bigger = Zoom in
    'random_bloc_swaps_frequency': 0.01,
    'regions': {
        'desert': {
            'repartition': [
                ('grass', 0.32),
                ('sand', 0.75),
                ('gravel', 0.78),
                ('sand', 0.85),
                ('stone', 1),
            ],
            'lichen_probability': 0.4,
            'trees_probability': 0.2,
            'rocks_probability': 0.5,
        },
        'mountain': {
            'repartition': [
                ('sand', 0.15),
                ('gravel', 0.3),
                ('stone', 1),
            ],
            'lichen_probability': 0.1,
            'trees_probability': 0.1,
            'rocks_probability': 1,
        },
        'temperate': {
            'repartition': [
                ('water', .1),
                ('gravel', .2),
                ('grass', .7),
                ('stone', .8),
            ],
            'lichen_probability': 0.1,
            'trees_probability': 1.2,
            'rocks_probability': 0.2,
        },
        'hell': {
            'repartition': [
                ('lava', .3),
            ],
            'lichen_probability': 0,
            'trees_probability': 0,
            'rocks_probability': 0.5,
        },
        'ocean': {
            'repartition': [
                ('water', 0.8),
                ('sand', 0.9),
                ('grass', 1),
            ],
            'lichen_probability': 0,
            'trees_probability': 0,
            'rocks_probability': 0.1,
        },
    }
}
