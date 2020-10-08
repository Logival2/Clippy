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
            'water': .05,
            'sand': .4,
            'gravel': .5,
            'grass': .6,
            'sand': .8,
        },
        'mountain': {
            'water': .1,
            'sand': .2,
            'grass': .5,
            'stone': 1,
        },
        'temperate': {
            'water': .2,
            'sand': .25,
            'gravel': .3,
            'grass': .8,
            'stone': 1,
        },
        'hell': {
            'lava': .3,
            'stone': .4,
            'gravel': .5,
            'stone': 1,
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
