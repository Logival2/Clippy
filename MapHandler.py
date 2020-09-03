import random

from utils import *
from Entities import *
from map_gen import MapGenerator


class MapHandler(object):
    def __init__(s):
        s.map = []
        s.config = load_theme_file()
        if len(sys.argv) > 1:
            s.load_map_from_json(sys.argv[1])
        else:
            s.map_generator = MapGenerator(Pos(200, 200))
            s.load_map_from_string(s.map_generator.get_map())
            # s.map = generate_room()
        # Check if player exists
        s.player_pos = None
        found_flag = False
        for y, line in enumerate(s.map):
            for x, ent in enumerate(line):
                if ent and isinstance(ent.top_ent, Player):
                    s.player_pos = Pos(y, x)
                    found_flag = True
                    break
            if found_flag: break
        if not found_flag:
            exit_error("Invalid map file: No player defined")
        s.map_size = s.get_raw_map_size()

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
            char = random.choice(list(s.config["wall"].keys()))
            data = s.config["wall"][char]
            return Square(None, Wall(char, True, data["fg_c"], data["bg_c"]))
        # Create default floor
        char = random.choice(list(s.config["floor"].keys()))
        data = s.config["floor"][char]
        floor = Entity(char, False, data["fg_c"], data["bg_c"])
        # Create floor
        if c == 'f': return Square(floor)
        ### Living entities ###
        # Create player
        if c == 'p':
            char = random.choice(list(s.config["player"].keys()))
            data = s.config["player"][char]
            return Square(floor, Player(char, True, data["fg_c"], data["bg_c"]))
        # Create enemy
        if c == 'e':
            char = random.choice(list(s.config["enemy"].keys()))
            data = s.config["enemy"][char]
            return Square(floor, Enemy(char, True, data["fg_c"], data["bg_c"]))
        exit_error("Invalid map file, unknown character: " + c)

    def get_square_from_pos(s, y, x=None):
        if x: return s.map[y][x]
        else: return s.map[y.y][y.x]  # Yeah... no overloading in python...

    def set_top_ent_to_pos(s, entity, y, x=None):
        if x: s.map[y][x].top_ent = entity
        else: s.map[y.y][y.x].top_ent = entity

    def is_valid_pos(s, pos):
        return pos.y > 0 and (pos.y < len(s.map)) and pos.x > 0 and (pos.x < len(s.map[pos.y]))

    def move_entity_absolute(s, from_p, to):
        if not s.is_valid_pos(from_p) or not s.is_valid_pos(to): return
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
