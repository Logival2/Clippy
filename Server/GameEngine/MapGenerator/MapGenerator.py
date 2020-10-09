import random
import math

from opensimplex import OpenSimplex

from utils import Pos
from Entities import *
from . import generate_random_chunk
from . import generate_terrain_chunk


class MapGenerator(object):
    def __init__(s, config):
        s.config = config
        s.simplex = OpenSimplex(s.config['seed'])
        # Create a bit more capitals, to give a more interesting region layout,
        # with some regions splitted into multiple parts of the map
        s.capitals_positions = []
        s.generate_capitals_positions(int(s.config['regions_nbr'] * 1.5))
        # s.compute_layouts_values_ranges()

    def get_map(s):
        str = [''.join(l) for l in s.map]
        str = '\n'.join(str)
        return str

    def save_chunk(s, anchor_pos, chunk):
        """ Saves the chunk (double array of tiles, defined by its anchor pos) to disk"""
        pass

    def generate_chunk(s, anchor_pos):
        chunk = generate_terrain_chunk.generate_terrain_chunk(s, anchor_pos)
        # chunk = generate_random_chunk(s, anchor_pos)
        # DEBUGGING, placing player to have something on screen
        middle_x = anchor_pos.x + s.config['chunk_size'] // 2
        middle_y = anchor_pos.y + s.config['chunk_size'] // 2
        chunk[middle_y][middle_x].top_ent = Player('player', True)
        return chunk

    def get_pos_region(s, tile_pos):
        dmin = math.hypot(s.config['map_size'] - 1, s.config['map_size'] - 1)
        closest_region_idx = -1
        for idx, capital_pos in enumerate(s.capitals_positions):
            d = math.hypot(capital_pos.x - tile_pos.x, capital_pos.y - tile_pos.y)
            if d < dmin:
                dmin = d
                closest_region_idx = idx % s.config['regions_nbr']
        return list(s.config['regions'].keys())[closest_region_idx]

    def generate_capitals_positions(s, capitals_nbr):
        for c in range(capitals_nbr):
            point_x = random.randint(0, s.config['map_size'])
            while point_x < 0 or point_x >= s.config['map_size']:
                point_x = random.randint(0, s.config['map_size'])
            point_y = random.randint(0, s.config['map_size'])
            while point_y < 0 or point_y >= s.config['map_size']:
                point_y = random.randint(0, s.config['map_size'])
            s.capitals_positions.append(Pos(x=point_x, y=point_y))

    def get_simplex_value(s, tile_pos):
        noise_value = s.simplex.noise2d(*(tile_pos / s.config['noise_scale']).get_xy())
        return (noise_value + 1) / 2  # To get a value between 0 and 1
