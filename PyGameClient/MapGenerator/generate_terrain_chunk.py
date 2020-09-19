import random
import math

from opensimplex import OpenSimplex

from utils import Pos
from Entities import *


def generate_terrain_chunk(s, anchor_pos):
    chunk = []
    for y in range(s.config['chunk_size']):
        tmp_line = []
        for x in range(s.config['chunk_size']):
            tile_pos = Pos(x=anchor_pos.x + x, y=anchor_pos.y + y)
            region = s.get_pos_region(tile_pos)
            noise_value = s.simplex.noise2d(*(tile_pos / s.config['noise_scale']).get_xy())
            noise_value = (noise_value + 1) / 2  # To get a value between 0 and 1

            if 0 < noise_value < 0.2:
                tmp_line.append(Tile(noise_value, Entity('water', True, region), None))
            elif noise_value < .7:
                if random.randint(0, 3):
                    tmp_line.append(Tile(1 - noise_value, Entity('floor', False, region), None))
                else:
                    tmp_line.append(Tile(noise_value, Entity('grass', False, region), None))
            else:
                tmp_line.append(Tile(noise_value, None, Entity('wall', True, region)))
        chunk.append(tmp_line)
    return chunk
