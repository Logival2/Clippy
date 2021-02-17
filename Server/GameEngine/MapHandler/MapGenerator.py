import math
import random

from opensimplex import OpenSimplex

from GameEngine.Components import *
# WTF is this? Fox is not imported by * ????
from GameEngine.Components import Fox
from GameEngine.Components import Vegetable
from GameEngine.MapHandler.map_config import MAP_CONFIG


class MapGenerator(object):
    def __init__(self, ecs):
        self.ecs = ecs
        self.config = MAP_CONFIG
        random.seed(self.config['seed'])
        self.simplex = OpenSimplex(self.config['seed'])
        # Create a bit more capitals, to give a more interesting region layout
        # as some regions will be splitted into multiple parts of the map
        self.capitals_positions = []
        self.generate_capitals_positions(int(self.config['regions_nbr'] * 1.5))

    def generate_chunk(self, anchor_pos):
        # Only create the ground blocs
        chunk, regions_blocs_positions = self.layout_basic_ground(anchor_pos)
        # Now randomly swap some of them
        # self.randomly_swap_blocs(chunk, anchor_pos)
        # Add Trees, rocks etc
        self.decorate_chunk(chunk, regions_blocs_positions, anchor_pos)
        # Create some AIs in this chunk
        self.populate_chunk(chunk, anchor_pos)
        return chunk

    def get_random_position(self, anchor_pos):
        return anchor_pos + Position.Position(
            random.randint(0, self.config['chunk_size']),
            random.randint(0, self.config['chunk_size']),
        )

    def populate_chunk(self, chunk, anchor_pos):
        entity = self.ecs.new_entity()
        ent_pos = self.get_random_position(anchor_pos)
        self.ecs.add_component(entity, ent_pos)
        self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy()))
        self.ecs.add_component(entity, Rabbit.Rabbit())
        self.ecs.add_component(entity, Sprite.Sprite('rabbit', 'desert', 0.5))

        entity = self.ecs.new_entity()
        ent_pos = self.get_random_position(anchor_pos)
        self.ecs.add_component(entity, ent_pos)
        self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy()))
        self.ecs.add_component(entity, Fox.Fox())
        self.ecs.add_component(entity, Sprite.Sprite('fox', 'desert', 0.5))

    def decorate_chunk(self, terrain, regions_blocs_positions, anchor_pos):
        # Add lichen
        for i in range(20):
            ent_pos = self.get_random_position(anchor_pos)
            entity = self.ecs.new_entity()
            self.ecs.add_component(entity, ent_pos)
            self.ecs.add_component(
                entity,
                Sprite.Sprite(
                    'lichen',
                    self.get_pos_region(ent_pos),
                    self.get_simplex_value(ent_pos),
                )
            )
            self.ecs.add_component(entity, Vegetable.Vegetable())
        # Add trees
        for i in range(20):
            ent_pos = self.get_random_position(anchor_pos)
            entity = self.ecs.new_entity()
            self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy()))
            self.ecs.add_component(entity, ent_pos)
            self.ecs.add_component(
                entity,
                Sprite.Sprite(
                    'tree',
                    self.get_pos_region(ent_pos),
                    self.get_simplex_value(ent_pos),
                )
            )
        # Add rocks
        for i in range(20):
            ent_pos = self.get_random_position(anchor_pos)
            entity = self.ecs.new_entity()
            self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy()))
            self.ecs.add_component(entity, ent_pos)
            self.ecs.add_component(
                entity,
                Sprite.Sprite(
                    'rock',
                    self.get_pos_region(ent_pos),
                    self.get_simplex_value(ent_pos),
                )
            )
        # Add pebbles
        for i in range(self.config['chunk_size']):
            ent_pos = self.get_random_position(anchor_pos)
            entity = self.ecs.new_entity()
            self.ecs.add_component(entity, ent_pos)
            self.ecs.add_component(
                entity,
                Sprite.Sprite(
                    'pebble',
                    self.get_pos_region(ent_pos),
                    self.get_simplex_value(ent_pos),
                )
            )

    def layout_basic_ground(self, anchor_pos):
        chunk = {}
        regions_blocs_positions = {region:[] for region in self.config['regions']}
        for y in range(self.config['chunk_size']):
            tmp_line = {}
            for x in range(self.config['chunk_size']):
                tile_pos = Position.Position(x=anchor_pos.x + x, y=anchor_pos.y + y)
                region = self.get_pos_region(tile_pos)
                ### Define the bloc type now, based on two noises of different scales
                # along with some random
                noise_value = self.get_simplex_value(tile_pos)
                # Also use a bit of another noise, a smaller one (more details)
                bloc_type_noise_value = (
                    + 6 * noise_value
                    + 1 *random.uniform(0, 1)
                ) / 7
                if bloc_type_noise_value < 0 or bloc_type_noise_value > 1:
                    print("1111")
                bloc_type = self.get_bloc_type(bloc_type_noise_value, region)
                ### Now create the noise which will be used for sprite drawing
                # Use the "normal scale" noise value and normalize it
                # so all type of sprites for a specific bloc type can be drawn
                OldMin, OldMax = self.get_bloc_type_noise_bounds(region, bloc_type)
                stretched_noise_value = (noise_value - OldMin) / (OldMax - OldMin)
                # TODO: Check why this returns some values <0 or > 1,
                # For now, clamp it
                stretched_noise_value = max(min(stretched_noise_value, 1), 0)
                # Finally merge those with some bit of random
                sent_noise_value = (
                    # + 3 * small_noise_value
                    + 2 * stretched_noise_value
                    + 1 *random.uniform(0, 1)
                ) / 3

                tmp_line[x + anchor_pos.x] = (
                    bloc_type, region,
                    sent_noise_value
                )
                regions_blocs_positions[region].append((y, x))
            chunk[y + anchor_pos.y] = tmp_line
        return chunk, regions_blocs_positions

    def get_bloc_type_noise_bounds(self, region, bloc_type):
        low_noise_value = 0
        max_noise_value = 1
        for tmp_bloc_type, bloc_type_max_noise_value in self.config['regions'][region]['repartition']:
            if tmp_bloc_type == bloc_type:
                max_noise_value = bloc_type_max_noise_value
                break
            low_noise_value = bloc_type_max_noise_value
        return low_noise_value, max_noise_value

    def randomly_swap_blocs(self, chunk, anchor_pos):
        # Now randomly swap blocs
        swaps_nbr = 0
        # for region in self.config['regions']:
        bloc_nbr_to_swap = self.config['chunk_size'] * self.config['chunk_size'] * self.config['random_bloc_swaps_frequency']
            # print(f"Swapping {bloc_nbr_to_swap} blocs in {region}")
        while swaps_nbr < bloc_nbr_to_swap:
            # choose two blocs
            bloc_1_pos = Position.Position(
                x=random.randint(anchor_pos.x, anchor_pos.x + self.config['chunk_size'] - 1),
                y=random.randint(anchor_pos.y, anchor_pos.y + self.config['chunk_size'] - 1),
            )
            bloc_2_pos = Position.Position(
                x=random.randint(anchor_pos.x, anchor_pos.x + self.config['chunk_size'] - 1),
                y=random.randint(anchor_pos.y, anchor_pos.y + self.config['chunk_size'] - 1),
            )
            if bloc_1_pos == bloc_2_pos:
                continue
            swaps_nbr += 2
            tmp = chunk[bloc_1_pos.y][bloc_1_pos.x]
            chunk[bloc_1_pos.y][bloc_1_pos.x] = chunk[bloc_2_pos.y][bloc_2_pos.x]
            chunk[bloc_2_pos.y][bloc_2_pos.x] = tmp

    def get_bloc_type(self, noise_value, region):
        ''' Use the region, noise value and config values (config.py) to
        determine which terrain block will be chosen'''
        block_name = ''
        for tmp_block_name, value in self.config['regions'][region]['repartition']:
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
            self.capitals_positions.append(Position.Position(x=point_x, y=point_y))

    def get_simplex_value(self, tile_pos):
        ''' Returns the noise value of a Position.Position
        '''
        noise_value = self.simplex.noise2d(
            *(tile_pos / self.config['noise_scale']).get_xy()
        )
        return (noise_value + 1) / 2  # To get a value between 0 and 1

    def get_map(self):
        ''' Useless for now, as we don't use chunks
        '''
        str = [''.join(l) for l in self.map]
        str = '\n'.join(str)
        return str
