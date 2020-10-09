from utils import Pos
from Entities import *


DISPLAY_CONFIG = {
    'fps': 4,
    'target_resolution': Pos(x=1800, y=1000),
    'hud_width_px': 200,
    'tile_size': 32,
    'borders_width': 2,
}

MAP_CONFIG = {
    'regions_nbr': 5,
    'map_size': 32,
    'chunk_size': 32,
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
