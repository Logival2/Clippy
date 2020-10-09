import json
import random
import sys

from opensimplex import OpenSimplex

from utils import *
from Entities import *
from MapGenerator.MapGenerator import MapGenerator
from map_config import MAP_CONFIG


class MapHandler(object):
    def __init__(s):
        s.map = []
        s.config = MAP_CONFIG
        if s.config['chunk_size'] > s.config['map_size']: s.config['chunk_size'] = s.config['map_size']
        s.map_generator = MapGenerator(s.config)
        # Debug, get a chunk
        s.map = s.map_generator.get_chunk(Pos(0, 0))
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
        s.generated_chunks = {}

    def get_chunk(s, anchor_pos):
        """ Get the chunk based on its anchor pos
        (from anchor_pos to anchor_pos + chunk size)
        if the chunk has already been generated (in s.generated_chunks) load it from disk
        otherwise generate it. Those functions return a double array of tiles
        """
        if anchor_pos in s.generated_chunks:
            return None # Load from disk
        else:
            chunk = s.map_generator.generate_chunk(anchor_pos)
            s.generated_chunks[anchor_pos] = chunk
            return chunk

    def get_player(s):
        return s.get_tile_from_pos(s.player_pos)

    def get_tile_from_pos(s, y, x=None):
        if x: return s.map[y][x]
        else: return s.map[y.y][y.x]  # Yeah... no overloading in python...

    def set_top_ent_to_pos(s, entity, y, x=None):
        if x: s.map[y][x].top_ent = entity
        else: s.map[y.y][y.x].top_ent = entity

    def is_valid_pos(s, pos):
        return pos.y >= 0 and (pos.y < len(s.map)) and pos.x >= 0 and (pos.x < len(s.map[pos.y]))

    def move_entity_absolute(s, from_p, to):
        if not s.is_valid_pos(from_p) or not s.is_valid_pos(to): return  # Bound check
        if not s.get_tile_from_pos(from_p) or not s.get_tile_from_pos(to): return  # Void check
        from_tile = s.get_tile_from_pos(from_p)
        next_tile = s.get_tile_from_pos(to)
        if next_tile and next_tile.is_free():
            next_tile.top_ent = from_tile.top_ent
            from_tile.top_ent = None
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
