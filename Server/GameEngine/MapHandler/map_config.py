from collections import OrderedDict


MAP_CONFIG = {
    'seed': 3,
    'regions_nbr': 8,
    'map_size': 128,
    'chunk_size': 24,
    'noise_scale': 15,  # Bigger = Zoom in
    'small_noise_scale': 8,  # Bigger = Zoom in
    'random_bloc_swaps_frequency': 0.01,
    'regions': {
        'swamp': {
            'repartition': [
                ('water', 0.6),
                ('sand', 0.7),
                ('gravel', 0.8),
                ('grass', 0.9),
                ('stone', 1),
            ],
            'lichen_probability': 0.2,
            'trees_probability': 0.3,
            'rocks_probability': 0.2,
        },
        'desert': {
            'repartition': [
                ('grass', 0.32),
                ('sand', 0.75),
                ('gravel', 0.78),
                ('sand', 0.85),
                ('stone', 1),
            ],
            'lichen_probability': 0.3,
            'trees_probability': 0.1,
            'rocks_probability': 0.15,
        },
        'mountain': {
            'repartition': [
                ('sand', 0.15),
                ('gravel', 0.3),
                ('stone', 1),
            ],
            'lichen_probability': 0.1,
            'trees_probability': 0.1,
            'rocks_probability': 1.3,
        },
        'temperate': {
            'repartition': [
                ('water', .1),
                ('gravel', .2),
                ('grass', .7),
                ('stone', .8),
            ],
            'lichen_probability': 0.1,
            'trees_probability': 1.3,
            'rocks_probability': 0.2,
        },
        'hell': {
            'repartition': [
                ('lava', 1),
            ],
            'lichen_probability': 0,
            'trees_probability': 0,
            'rocks_probability': 0.7,
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
