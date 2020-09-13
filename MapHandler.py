import json
import random
import sys

from utils import *
from Entities import *
from MapGenerator.MapGenerator import MapGenerator


class MapHandler(object):
    def __init__(s, seed=0):
        random.seed(seed)
        s.map = []
        ### Load unicode ranges dict
        s.unicode_ranges = {
            "chasse":   [( 0x02B0, 0x02FF )],
            "braille":  [( 0x2800, 0x28FF )],
            "kangxi":   [( 0x2F00, 0x2FD5 )],
            "hangul":   [( 0xC000, 0xCFFF )],
            "walls":    [( 0x2596, 0x259F )],
            "enemies":  [( 0x29D1, 0x29D7 ), ( 0x29E8, 0x29E9 )],
            "grass":    [( 0x0F20, 0x0F2F )],
        }
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
        return s.get_square_from_pos(s.player_pos)

    def load_map_from_json(s, map_name):
        with open(f"./maps/{map_name}.map", 'r') as f:
            data = f.read()
        s.load_map_from_string(data)

    def load_map_from_string(s, data):
        raw_map = [l for l in data.split('\n') if l]
        map = []
        for line in raw_map:
            tmp_line = []
            for c in line:
                tmp_line.append(s.create_entity(c))
            s.map.append(tmp_line)

    def create_entity(s, c):
        """Entity Factory"""
        # Create null
        if c == ' ':
            return
        # Create wall
        if c == 'w':
            range_list = s.unicode_ranges["walls"]
            # repr = f" {get_random_unicode_from_range(range_list, 1)}"
            # fg_color = random.randint(246, 250)
            # bg_color = 15
            return Square(None, Entity('wall'))
        # Create default floor
        # repr = get_random_unicode_from_range(s.unicode_ranges["braille"], 2)
        # fg_color = random.randint(233, 237)
        # bg_color = random.randint(233, 237)
        floor = Entity('floor', False)
        # Create floor
        if c == 'f': return Square(floor)
        if c == 'g':
            # repr = f"{get_random_unicode_from_range(s.unicode_ranges['grass'])} "
            # fg_color = 46
            # bg_color = 28
            return Square(Entity('grass', False))
        ### Living entities ###
        # Create player
        if c == 'p':
            # repr = "⧱ "
            # fg_color = 82
            # bg_color = -1
            return Square(floor, Player('player'))
        # Create enemy
        if c == 'e':
            # repr = f"{get_random_unicode_from_range(s.unicode_ranges['enemies'])} "
            # fg_color = 9
            # bg_color = -1
            return Square(floor, Enemy('enemy'))
        exit_error("Invalid map file, unknown repracter: " + c)

    def get_square_from_pos(s, y, x=None):
        if x: return s.map[y][x]
        else: return s.map[y.y][y.x]  # Yeah... no overloading in python...

    def set_top_ent_to_pos(s, entity, y, x=None):
        if x: s.map[y][x].top_ent = entity
        else: s.map[y.y][y.x].top_ent = entity

    def is_valid_pos(s, pos):
        return pos.y > 0 and (pos.y < len(s.map)) and pos.x > 0 and (pos.x < len(s.map[pos.y]))

    def move_entity_absolute(s, from_p, to):
        if not s.is_valid_pos(from_p) or not s.is_valid_pos(to): return  # Bound check
        if not s.get_square_from_pos(from_p) or not s.get_square_from_pos(to): return  # Void check
        from_square = s.get_square_from_pos(from_p)
        next_square = s.get_square_from_pos(to)
        if next_square and next_square.is_free():
            s.set_top_ent_to_pos(from_square.top_ent, to)
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
