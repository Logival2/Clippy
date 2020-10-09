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
            noise_value = s.get_simplex_value(tile_pos)
            region = s.get_pos_region(tile_pos)
            tmp_line.append(get_tile(s, noise_value, region))
        chunk.append(tmp_line)
    return chunk

def get_tile(s, noise_value, region):
    block_name = ''
    for tmp_block_name, value in s.config['regions'][region].items():
        block_name = tmp_block_name
        if noise_value < value: break
    low_ent = s.config['blocks'][block_name](noise_value, region)
    return Tile(noise_value, low_ent, None)
