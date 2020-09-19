import random
import math

from opensimplex import OpenSimplex

from utils import Pos
from Entities import *


def generate_random_chunk(s, anchor_pos):
    chunk = []
    for y in range(s.config['chunk_size']):
        tmp_line = []
        for x in range(s.config['chunk_size']):
            tile_pos = Pos(x=anchor_pos.x + x, y=anchor_pos.y + y)
            noise_value = s.simplex.noise2d(
                                    x=tile_pos.x / s.config['noise_scale'],
                                    y=tile_pos.y / s.config['noise_scale'])
            noise_value = (noise_value + 1) / 2  # To get a value between 0 and 1
            value = random.randint(0, 60)
            if value < 10:
                tmp_line.append(Tile(
                                noise_value,
                                None,
                                Entity('wall', True, s.get_pos_region(tile_pos))))
            elif value == 11:
                tmp_line.append(Tile(
                                    1 - noise_value,
                                    Entity('grass', False, s.get_pos_region(tile_pos)),
                                    None))
            elif value == 12:
                tmp_line.append(Tile(
                                    1 - noise_value,
                                    Entity('water', True, s.get_pos_region(tile_pos)),
                                    None))
            else:
                tmp_line.append(Tile(
                                    1 - noise_value,
                                    Entity('floor', False, s.get_pos_region(tile_pos)),
                                    None))
        chunk.append(tmp_line)
    return chunk
