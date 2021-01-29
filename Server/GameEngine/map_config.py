from Entities import *

MAP_CONFIG = {
    'regions_nbr': 5,
    'map_size': 64,
    'chunk_size': 64,
    'seed': 0,
    'noise_scale': 15,  # Bigger = Zoom in
    'regions': {
        'desert': {
            'sand': 1,
        },
        'mountain': {
            'stone': 1,
        },
        'temperate': {
            'grass': .8,
        },
        'hell': {
            'lava': .3,
        },
        'ocean': {
            'water': 1,
        },
    },
    'blocks': {
        'grass': Grass,
        'gravel': Gravel,
        'lava': Lava,
        'sand': Sand,
        'stone': Stone,
        'water': Water,
    }
}
