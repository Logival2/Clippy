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
        s.compute_layouts_values_ranges()

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
        return s.generate_random_chunk(anchor_pos)

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
                layout_name = s.get_layout_name_from_noise_value(noise_value)
                value = random.randint(0, 60)
                if value < 10:
                    tmp_line.append(Tile(
                                    noise_value,
                                    layout_name,
                                    None,
                                    Entity('wall', True, s.get_pos_region(tile_pos))))
                elif value == 11:
                    tmp_line.append(Tile(
                                        1 - noise_value,
                                        layout_name,
                                        Entity('grass', False, s.get_pos_region(tile_pos)),
                                        None))
                elif value == 12:
                    tmp_line.append(Tile(
                                        1 - noise_value,
                                        layout_name,
                                        Entity('water', True, s.get_pos_region(tile_pos)),
                                        None))
                else:
                    tmp_line.append(Tile(
                                        1 - noise_value,
                                        layout_name,
                                        Entity('floor', False, s.get_pos_region(tile_pos)),
                                        None))
            chunk.append(tmp_line)

        # DEBUGGING, placing player to have something on screen
        middle_x = anchor_pos.x + s.config['chunk_size'] // 2
        middle_y = anchor_pos.y + s.config['chunk_size'] // 2
        chunk[middle_y][middle_x] = Tile(
                                        0.7,
                                        layout_name,
                                        Entity('floor', False, s.get_pos_region(Pos(x=middle_x, y=middle_y))),
                                        Player('player', True))
        return chunk

    def get_pos_region(s, tile_pos):
        dmin = math.hypot(s.config['map_size'] - 1, s.config['map_size'] - 1)
        closest_region_idx = -1
        for idx, capital_pos in enumerate(s.capitals_positions):
            d = math.hypot(capital_pos.x - tile_pos.x, capital_pos.y - tile_pos.y)
            if d < dmin:
                dmin = d
                closest_region_idx = idx % s.regions_nbr
        return closest_region_idx

    def get_layout_name_from_noise_value(s, noise_value):
        layout_name = ''
        for l_name, l_data in s.config['layouts'].items():
            if l_data["range_lower_value"] < noise_value < l_data["range_upper_value"]:
                return l_name

    def compute_layouts_values_ranges(s):
        """ Define each range of float values in [0;2] to a specific layout,
        according to the proportions specified in s.config['layouts'][layout_type].
        Will store range values in s.config['layouts'][layout_type] """
        # Noise values range from 0 to 2, divide 2 by the total number
        # of sections to get a single gap value
        total = sum([layout_data["proportion"] for layout_data in s.config['layouts'].values()])
        single_gap = 2 / total
        range_lower_value = 0
        for l_name, l_data in s.config['layouts'].items():
            s.config['layouts'][l_name]["range_lower_value"] = range_lower_value
            range_lower_value = range_lower_value + (l_data["proportion"] * single_gap)
            s.config['layouts'][l_name]["range_upper_value"] = range_lower_value

    def generate_capitals_positions(s, capitals_nbr):
        for c in range(capitals_nbr):
            point_x = random.randint(0, s.config['map_size'])
            while point_x < 0 or point_x >= s.config['map_size']:
                point_x = random.randint(0, s.config['map_size'])
            point_y = random.randint(0, s.config['map_size'])
            while point_y < 0 or point_y >= s.config['map_size']:
                point_y = random.randint(0, s.config['map_size'])
            s.capitals_positions.append(Pos(x=point_x, y=point_y))
