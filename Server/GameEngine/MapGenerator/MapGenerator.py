import math
import random

from opensimplex import OpenSimplex

from utils import Pos
from Entities import *
from GameEngine.MapGenerator.map_config import MAP_CONFIG


class MapGenerator(object):
    def __init__(self):
        self.config = MAP_CONFIG
        random.seed(self.config['seed'])
        self.simplex = OpenSimplex(self.config['seed'])
        # Create a bit more capitals, to give a more interesting region layout
        # as some regions will be splitted into multiple parts of the map
        self.capitals_positions = []
        self.generate_capitals_positions(int(self.config['regions_nbr'] * 1.5))

    # def generate_entities_chunk(self, anchor_pos=Pos(0, 0)):
    #     ''' returns a double array of tuples: (entity_type, region)
    #     noise value is needed by clients to vary the display of similar bloc types'''
    #     chunk = []
    #     for y in range(self.config['chunk_size']):
    #         tmp_line = []
    #         for x in range(self.config['chunk_size']):
    #             tile_pos = Pos(x=anchor_pos.x + x, y=anchor_pos.y + y)
    #             noise_value = self.get_simplex_value(tile_pos)
    #             region = self.get_pos_region(tile_pos)
    #             bloc_type = self.get_bloc_type(noise_value, region)
    #             tmp_line.append((bloc_type, region))
    #         chunk.append(tmp_line)
    #     return chunk

    def generate_terrain_chunk(self, anchor_pos=Pos(0, 0)):
        ''' returns a double array of tuples: (bloc_type, region, noise_value)
        noise value is needed by clients to vary the display of similar bloc types'''
        chunk = {}
        regions_blocs_positions = {}
        for region in self.config['regions']:
            regions_blocs_positions[region] = []
        for y in range(self.config['chunk_size']):
            tmp_line = {}
            for x in range(self.config['chunk_size']):
                tile_pos = Pos(x=anchor_pos.x + x, y=anchor_pos.y + y)
                noise_value = self.get_simplex_value(tile_pos)
                region = self.get_pos_region(tile_pos)
                bloc_type = self.get_bloc_type(noise_value, region)
                tmp_line[x + anchor_pos.x] = (bloc_type, region, noise_value)
                regions_blocs_positions[region].append((y, x))
            chunk[y + anchor_pos.y] = tmp_line
        # Now randomly swap blocs
        swaps_nbr = 0
        for region in self.config['regions']:
            bloc_nbr_to_swap = len(regions_blocs_positions[region]) * self.config['regions'][region]['random_bloc_swaps_frequency'] // 100
            print(f"Swapping {bloc_nbr_to_swap} blocs in {region}")
            while swaps_nbr < bloc_nbr_to_swap:
                # choose two blocs
                bloc_1_pos = random.choice(regions_blocs_positions[region])
                bloc_2_pos = random.choice(regions_blocs_positions[region])
                if bloc_1_pos == bloc_2_pos:
                    continue
                swaps_nbr += 2
                tmp = chunk[bloc_1_pos[0]][bloc_1_pos[1]]
                chunk[bloc_1_pos[0]][bloc_1_pos[1]] = chunk[bloc_2_pos[0]][bloc_2_pos[1]]
                chunk[bloc_2_pos[0]][bloc_2_pos[1]] = tmp
        return chunk

    def get_bloc_type(self, noise_value, region):
        ''' Use the region, noise value and config values (config.py) to
        determine which terrain block will be chosen'''
        block_name = ''
        for tmp_block_name, value in self.config['regions'][region]['repartition'].items():
            block_name = tmp_block_name
            if noise_value < value:
                break
        return block_name

    def get_pos_region(self, tile_pos):
        ''' Returns the region string based on a position
        '''
        dmin = math.hypot(self.config['map_size'] - 1, self.config['map_size'] - 1)
        closest_region_idx = -1
        for idx, capital_pos in enumerate(self.capitals_positions):
            d = math.hypot(capital_pos.x - tile_pos.x, capital_pos.y - tile_pos.y)
            if d < dmin:
                dmin = d
                closest_region_idx = idx % self.config['regions_nbr']
        return list(self.config['regions'].keys())[closest_region_idx]

    def generate_capitals_positions(self, capitals_nbr):
        ''' Choose {capitals_nbr} coordinates to place the capitals
        Regions will be determined based on those coordinates'''
        for c in range(capitals_nbr):
            point_x = random.randint(0, self.config['map_size'])
            while point_x < 0 or point_x >= self.config['map_size']:
                point_x = random.randint(0, self.config['map_size'])
            point_y = random.randint(0, self.config['map_size'])
            while point_y < 0 or point_y >= self.config['map_size']:
                point_y = random.randint(0, self.config['map_size'])
            self.capitals_positions.append(Pos(x=point_x, y=point_y))

    def get_simplex_value(self, tile_pos):
        ''' Returns the noise value of a Pos
        '''
        noise_value = self.simplex.noise2d(*(tile_pos / self.config['noise_scale']).get_xy())
        return (noise_value + 1) / 2  # To get a value between 0 and 1

    def get_map(self):
        ''' Useless for now, as we don't use chunks
        '''
        str = [''.join(l) for l in self.map]
        str = '\n'.join(str)
        return str
