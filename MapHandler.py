import json
import random

from utils import *
from Entities import *


class MapHandler(object):
    def __init__(s, input):
        s.updates = []
        # TODO add an update registering system, in order to draw only the
        # screen areas which changed
        s.map = []
        s.player_pos = None
        if isinstance(input, Pos):
            # Map Generator
            for y in range(input.y):
                line = [Entity('x')] * input.x
                s.map.append(line)
        else:
            s.load_map_from_json(input)
        found_flag = False
        for y, line in enumerate(s.map):
            for x, ent in enumerate(line):
                if isinstance(ent, Player):
                    s.player_pos = Pos(y, x)
                    found_flag = True
                    break
            if found_flag: break
        if not found_flag:
            exit_error("Invalid map file: No player defined")
        # Print the map entirely for the first time
        print("\033[2J")
        s.full_display()

    def get_player(s):
        return s.get_entity_from_pos(s.player_pos)

    def load_map_from_json(s, input):
        with open(f"./maps/{input}.json", 'r') as f:
            data = f.read()
        data = json.loads(data)
        if not all(e in data["entities"].keys() for e in ['floor', 'enemies', 'player']):
            exit_error("Invalid map file, not enough entities defined")

        map = [l for l in data["map"].split('\n') if l]
        for line in map:
            tmp_line = []
            for c in line:
                tmp_line.append(s.create_entity(c, data["entities"]))
            s.map.append(tmp_line)

    def create_entity(s, c, ent_data):
        """Entity Factory, returns none if the char is not defined as any entity"""
        # Create null
        if c == ' ':
            return
        # Create player
        if c == 'p':
            char = random.choice(list(ent_data["player"].keys()))
            data = ent_data["player"][char]
            return Player(char, data["fg_c"], data["bg_c"])
        # Create enemy
        if c == 'e':
            char = random.choice(list(ent_data["enemies"].keys()))
            data = ent_data["enemies"][char]
            return Enemy(char, data["fg_c"], data["bg_c"])
        # Create obstacle
        if c == 'o':
            char = random.choice(list(ent_data["obstacles"].keys()))
            data = ent_data["obstacles"][char]
            return Obstacle(char, data["fg_c"], data["bg_c"])
        # Create floor
        if c == 'f':
            char = random.choice(list(ent_data["floor"].keys()))
            data = ent_data["floor"][char]
            return Floor(char, False, data["fg_c"], data["bg_c"])
        exit_error("Invalid map file, unknown character: " + c)

    def full_display(s):
        for y, l in enumerate(s.map):
            print(f"\033[K\033[{y+1};1H")
            for entity in l:
                if not entity:
                    print(" ", end='')
                else:
                    print(entity, end='\x1b[0m')
        print(f"\033[{len(s.map)+1};1H")
        # for l in s.map:
        #     for e in l:
        #         if e:
        #             print(e, end='')
        #         else:
        #             print(" ", end='')
        #     print()

    def get_entity_from_pos(s, y, x=None):
        if x: return s.map[y][x]
        else: return s.map[y.y][y.x]  # Yeah... no overloading in python...

    def set_entity_to_pos(s, entity, y, x=None):
        if x: s.map[y][x] = entity
        else: s.map[y.y][y.x] = entity # Yeah... no overloading in python...

    def is_valid_pos(s, pos):
        return pos.y > 0 and (pos.y < len(s.map)) and pos.x > 0 and (pos.x < len(s.map[pos.y]))

    def move_entity_absolute(s, from_p, to):
        if not s.is_valid_pos(from_p) or not s.is_valid_pos(to): return
        entity = s.get_entity_from_pos(from_p)
        next_case = s.get_entity_from_pos(to)
        if next_case and not next_case.is_collider:
            s.set_entity_to_pos(entity, to)
            s.set_entity_to_pos(None, from_p)
            return True

    def move_entity_relative(s, from_p, delta):
        to = from_p + delta
        if not s.is_valid_pos(from_p) or not s.is_valid_pos(to): return
        entity = s.get_entity_from_pos(from_p)
        next_case = s.get_entity_from_pos(to)
        if next_case and not next_case.is_collider:
            # print(f"MOVING {type(entity)} FROM {from_p} TO:{to} ({type(next_case)})")
            s.set_entity_to_pos(entity, to)
            s.set_entity_to_pos(None, from_p)
            return True

    def get_max_width(s):
        max = 0
        for l in s.map:
            if len(l) > max:
                max = len(l)
        return max
