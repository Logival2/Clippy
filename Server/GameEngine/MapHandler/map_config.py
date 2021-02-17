MAP_CONFIG = {
    'seed': 1,
    'regions_nbr': 5,
    'map_size': 1024,
    'chunk_size': 32,
    'noise_scale': 15,  # Bigger = Zoom in
    'regions': {
        'desert': {
            'repartition': {
                'grass': 0.3,
                'sand': 0.8,
                'stone': 1,
            },
            'random_bloc_swaps_frequency': 70,
        },
        'mountain': {
            'repartition': {
                'stone': 1,
            },
            'random_bloc_swaps_frequency': 10,
        },
        'temperate': {
            'repartition': {
                'grass': .8,
            },
            'random_bloc_swaps_frequency': 20,
        },
        'hell': {
            'repartition': {
                'lava': .3,
            },
            'random_bloc_swaps_frequency': 90,
        },
        'ocean': {
            'repartition': {
                'water': 1,
            },
            'random_bloc_swaps_frequency': 2,
        },
    }
}
