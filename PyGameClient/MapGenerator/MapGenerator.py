import random
import time
import math

from opensimplex import OpenSimplex

from utils import Pos
from Entities import *


class MapGenerator(object):
    def __init__(s, config):
        s.config = config
        s.simplex = OpenSimplex(s.config['seed'])
        s.regions_nbr = 5
        # Create a bit more capitals, to give a more interesting region layout,
        # with some regions splitted into multiple parts of the map
        s.capitals_positions = []
        s.generate_capitals_positions(int(s.regions_nbr * 1.5))
        s.generated_chunks = []

    def get_map(s):
        str = [''.join(l) for l in s.map]
        str = '\n'.join(str)
        return str

    def save_chunk(s, anchor_pos, chunk):
        """ Saves the chunk (double array of tiles, defined by its anchor pos) to disk"""
        pass

    def get_chunk(s, anchor_pos):
        """ Get the chunk based on its anchor pos
        (from anchor_pos to anchor_pos + chunk size)
        if the chunk has already been generated (in s.generated_chunks) load it from disk
        otherwise generate it. Those functions return a double array of tiles
        """
        if anchor_pos in s.generated_chunks:
            return None # Load from disk
        else:
            return s.generate_chunk(anchor_pos)

    def generate_chunk(s, anchor_pos):
        chunk = []
        for y in range(s.config['chunk_size']):
            tmp_line = []
            for x in range(s.config['chunk_size']):
                tile_pos = Pos(x=anchor_pos.x + x, y=anchor_pos.y + y)
                noise_value = s.simplex.noise2d(
                                        x=tile_pos.x / s.config['noise_scale'],
                                        y=tile_pos.y / s.config['noise_scale'])
                noise_value = (noise_value + 1) / 2  # To get a value between 0 and 1
                if random.randint(0, 3):
                    tmp_line.append(Tile(
                                        1 - noise_value,
                                        Entity('floor', False, s.get_pos_region(tile_pos)),
                                        None))
                else:
                    tmp_line.append(Tile(
                                        noise_value,
                                        None,
                                        Entity('wall', True, s.get_pos_region(tile_pos))))
            chunk.append(tmp_line)

        # DEBUGGING, placing player to have something on screen
        middle_x = anchor_pos.x + s.config['chunk_size'] // 2
        middle_y = anchor_pos.y + s.config['chunk_size'] // 2
        chunk[middle_y][middle_x].top_ent = Player('player', True)

        return chunk

    def get_pos_region(s, tile_pos):
        dmin = math.hypot(s.config['map_size'] - 1, s.config['map_size'] - 1)
        closest_region_idx = 0
        for idx, capital_pos in enumerate(s.capitals_positions):
            d = math.hypot(capital_pos.x - tile_pos.x, capital_pos.y - tile_pos.y)
            if d < dmin:
                dmin = d
                closest_region_idx = idx % s.regions_nbr
        return closest_region_idx

    def generate_capitals_positions(s, capitals_nbr):
        for c in range(capitals_nbr):
            point_x = random.randint(0, s.config['map_size'])
            while point_x < 0 or point_x >= s.config['map_size']:
                point_x = random.randint(0, s.config['map_size'])
            point_y = random.randint(0, s.config['map_size'])
            while point_y < 0 or point_y >= s.config['map_size']:
                point_y = random.randint(0, s.config['map_size'])
            s.capitals_positions.append(Pos(x=point_x, y=point_y))
