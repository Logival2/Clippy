import math
import random
from pprint import pprint

from opensimplex import OpenSimplex
import sys
from GameEngine.Components import *
# pprint(sys.modules)
# WTF is this? Why isn't Fox imported by * ????
from GameEngine.Components import Fox
from GameEngine.Components import Pig
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
        # Add Trees, rocks etc
        self.decorate_chunk(chunk, regions_blocs_positions, anchor_pos)
        # Create some AIs in this chunk
        self.populate_chunk(chunk, anchor_pos)
        return chunk

    def populate_chunk(self, chunk, anchor_pos):
        entity = self.ecs.new_entity()
        ent_pos = self.get_random_position(anchor_pos)
        self.ecs.add_component(entity, ent_pos)
        self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy(), False))
        self.ecs.add_component(entity, Pig.Pig())
        self.ecs.add_component(entity, Sprite.Sprite('pig', 'desert', 0.5))

        entity = self.ecs.new_entity()
        ent_pos = self.get_random_position(anchor_pos)
        self.ecs.add_component(entity, ent_pos)
        self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy(), False))
        self.ecs.add_component(entity, Fox.Fox())
        self.ecs.add_component(entity, Sprite.Sprite('fox', 'desert', 0.5))

    def create_entity(self, ent_pos, sprite_name, is_collider=False):
        entity = self.ecs.new_entity()
        self.ecs.add_component(entity, ent_pos)
        self.ecs.add_component(
            entity,
            Sprite.Sprite(
                sprite_name,
                self.get_pos_region(ent_pos),
                self.get_simplex_value(ent_pos),
            )
        )
        if is_collider:
            self.ecs.add_component(entity, Hitbox.Hitbox(*ent_pos.get_xy()))
        return entity

    def decorate_chunk(self, terrain, regions_blocs_positions, anchor_pos):
        entities_density = 20  # Bigger = less entities
        for region, region_bloc_positions in regions_blocs_positions.items():
            lichen_probability = self.config["regions"][region]["lichen_probability"]
            # Add lichen
            for i in range(int(len(region_bloc_positions) * lichen_probability / entities_density)):
                ent_pos = random.choice(regions_blocs_positions[region])
                regions_blocs_positions[region].remove(ent_pos)
                entity = self.create_entity(ent_pos + anchor_pos, "lichen", False)
                self.ecs.add_component(entity, Vegetable.Vegetable())
            # Add trees
            trees_probability = self.config["regions"][region]["trees_probability"]
            for i in range(int(len(region_bloc_positions) * trees_probability / entities_density)):
                ent_pos = random.choice(regions_blocs_positions[region])
                regions_blocs_positions[region].remove(ent_pos)
                entity = self.create_entity(ent_pos + anchor_pos, "tree", True)
            # Add rocks
            rocks_probability = self.config["regions"][region]["rocks_probability"]
            for i in range(int(len(region_bloc_positions) * rocks_probability / entities_density)):
                ent_pos = random.choice(regions_blocs_positions[region])
                regions_blocs_positions[region].remove(ent_pos)
                entity = self.create_entity(ent_pos + anchor_pos, "rock", True)
                # Add pebbles
                ent_pos = random.choice(regions_blocs_positions[region])
                regions_blocs_positions[region].remove(ent_pos)
                entity = self.create_entity(ent_pos + anchor_pos, "pebble", False)

    def layout_basic_ground(self, anchor_pos):
        chunk = {}
        regions_blocs_positions = {region:[] for region in self.config['regions']}
        for y in range(self.config['chunk_size']):
            tmp_line = {}
            for x in range(self.config['chunk_size']):
                tile_pos = Position.Position(x=anchor_pos.x + x, y=anchor_pos.y + y)
                ### Define the bloc type now, based on two noises of different scales
                # along with some random
                noise_value = self.get_simplex_value(tile_pos)
                region = self.get_pos_region(tile_pos, noise_value)
                # Also use a bit of another noise, a smaller one (more details)
                bloc_type_noise_value = (
                    + 6 * noise_value
                    + 1 *random.uniform(0, 1)
                ) / 7
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
                tmp_line[x + anchor_pos.x] = (bloc_type, region,  sent_noise_value)
                regions_blocs_positions[region].append(Position.Position(y=y, x=x))
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

    def get_bloc_type(self, noise_value, region):
        ''' Use the region, noise value and config values (config.py) to
        determine which terrain block will be chosen'''
        block_name = ''
        for tmp_block_name, value in self.config['regions'][region]['repartition']:
            block_name = tmp_block_name
            if noise_value < value:
                break
        return block_name

    def get_pos_region(self, tile_pos, noise_value=0):
        ''' Returns the region string based on a position '''
        dmin = math.hypot(self.config['map_size'] - 1, self.config['map_size'] - 1)
        closest_region = (-1, 10000)
        second_closest_region = (-1, 10000)
        for idx, capital_pos in enumerate(self.capitals_positions):
            d = math.hypot(capital_pos.x - tile_pos.x, capital_pos.y - tile_pos.y)
            if d < dmin:
                dmin = d
                second_closest_region = closest_region
                closest_region = (idx % self.config['regions_nbr'], d)
        regions_key_list = list(self.config['regions'].keys())
        choice_list = [regions_key_list[closest_region[0] % len(regions_key_list)]]
        if abs(second_closest_region[1] - closest_region[1]) < 5:
            choice_list += [
                regions_key_list[second_closest_region[0] % len(regions_key_list)],
            ]
        return choice_list[int(
            ((5 * noise_value + random.uniform(0, 1)) / 6)
             * len(choice_list)
         )]

    def generate_capitals_positions(self, capitals_nbr):
        ''' Choose {capitals_nbr} coordinates to place the capitals
        Regions will be determined based on those coordinates '''
        for c in range(capitals_nbr):
            point_x = random.randint(0, self.config['map_size'])
            while point_x < 0 or point_x >= self.config['map_size']:
                point_x = random.randint(0, self.config['map_size'])
            point_y = random.randint(0, self.config['map_size'])
            while point_y < 0 or point_y >= self.config['map_size']:
                point_y = random.randint(0, self.config['map_size'])
            self.capitals_positions.append(Position.Position(x=point_x, y=point_y))

    def get_simplex_value(self, tile_pos):
        ''' Returns the noise value of a Position.Position '''
        noise_value = self.simplex.noise2d(
            *(tile_pos / self.config['noise_scale']).get_xy()
        )
        return (noise_value + 1) / 2  # To get a value between 0 and 1

    def get_random_position(self, anchor_pos):
        return anchor_pos + Position.Position(
            random.randint(0, self.config['chunk_size']),
            random.randint(0, self.config['chunk_size']),
        )
