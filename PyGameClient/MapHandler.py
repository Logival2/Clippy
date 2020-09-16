import json
import random
import sys

from opensimplex import OpenSimplex

from utils import *
from Entities import *
from MapGenerator.MapGenerator import MapGenerator


class MapHandler(object):
    def __init__(s, seed=0):
        s.map = []
        s.simplex = OpenSimplex(seed)
        s.noise_scale = 5
        if len(sys.argv) > 1:
            s.load_map_from_json(sys.argv[1])
        else:
            s.map_generator = MapGenerator(Pos(500, 500), seed)
            s.load_map_from_string(s.map_generator.get_map())
        # Check if player exists
        s.player_pos = None
        for y, line in enumerate(s.map):
            for x, ent in enumerate(line):
                if ent and isinstance(ent.top_ent, Player):
                    s.player_pos = Pos(y, x)
                    break
            if s.player_pos: break
        if not s.player_pos:
            exit_error("Invalid map file: No player defined")
        s.map_size = s.get_raw_map_size()
        # Ensure that the map is square (padd with None)
        for line in s.map:
            line += [None] * (s.map_size.x - len(line))
        s.view_target = s.player_pos

    def get_player(s):
        return s.get_tile_from_pos(s.player_pos)

    def load_map_from_json(s, map_name):
        with open(f"./maps/{map_name}.map", 'r') as f:
            data = f.read()
        s.load_map_from_string(data)

    def load_map_from_string(s, data):
        raw_map = [l for l in data.split('\n') if l]
        map = []
        for y_idx, line in enumerate(raw_map):
            tmp_line = []
            for x_idx, c in enumerate(line):
                noise_value = s.simplex.noise2d(
                                        x=x_idx / s.noise_scale,
                                        y=y_idx / s.noise_scale)
                noise_value = (noise_value + 1) / 2  # To get a value between 0 and 1
                tmp_line.append(s.create_entity(c, noise_value))
            s.map.append(tmp_line)

    def create_entity(s, c, noise_value):
        """Entity Factory"""
        # Create null
        if c == ' ': return
        # Create wall
        if c == 'w': return Tile(noise_value, None, Entity('wall', True))
        # Create grass
        if c == 'g': return Tile(noise_value, Entity('grass', False), None)
        # Create water
        if c == 'l': return Tile(noise_value, Entity('water', True), None)
        # Create default floor
        floor = Entity('floor', False)
        # Create floor
        if c == 'f': return Tile(1 - noise_value, floor, None)
        ### Living entities ###
        # Create player
        if c == 'p': return Tile(noise_value, floor, Player('player', True))
        # Create enemy
        if c == 'e': return Tile(noise_value, floor, Enemy('enemy', True))
        exit_error("Invalid map file, unknown character: " + c)

    def get_tile_from_pos(s, y, x=None):
        if x: return s.map[y][x]
        else: return s.map[y.y][y.x]  # Yeah... no overloading in python...

    def set_top_ent_to_pos(s, entity, y, x=None):
        if x: s.map[y][x].top_ent = entity
        else: s.map[y.y][y.x].top_ent = entity

    def is_valid_pos(s, pos):
        return pos.y > 0 and (pos.y < len(s.map)) and pos.x > 0 and (pos.x < len(s.map[pos.y]))

    def move_entity_absolute(s, from_p, to):
        if not s.is_valid_pos(from_p) or not s.is_valid_pos(to): return  # Bound check
        if not s.get_tile_from_pos(from_p) or not s.get_tile_from_pos(to): return  # Void check
        from_tile = s.get_tile_from_pos(from_p)
        next_tile = s.get_tile_from_pos(to)
        if next_tile and next_tile.is_free():
            s.set_top_ent_to_pos(from_tile.top_ent, to)
            s.set_top_ent_to_pos(None, from_p)
            return True

    def move_entity_relative(s, from_p, delta):
        to = from_p + delta
        return s.move_entity_absolute(from_p, to)

    def get_raw_map_size(s):
        max = 0
        for l in s.map:
            if len(l) > max:
                max = len(l)
        return Pos(len(s.map), max)
