import json

from utils import *
from Entities import *


class Map(object):
    def __init__(s, input):
        s.updates = []
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
        s.full_display()

    def load_map_from_json(s, input):
        with open(f"./maps/{input}.json", 'r') as f:
            data = f.read()
        data = json.loads(data)
        if not all(e in data["entities"].keys() for e in ["player", "enemies", "obstacles"]):
            exit_error("Invalid map file, not enough entities defined")
        map = [l for l in data["map"].split('\n') if l]
        for line in map:
            tmp_line = []
            for c in line:
                tmp_line.append(s.create_entity(c, data["entities"]))
            s.map.append(tmp_line)

    def create_entity(s, c, ent_data):
        """Entity Factory, returns none if the char is not defined as any entity"""
        # Create player
        if c in ent_data["player"].keys():
            data = ent_data["player"][c]
            return Player(c, data["fg_c"], data["bg_c"])
        # Create enemy
        if c in ent_data["enemies"].keys():
            data = ent_data["enemies"][c]
            return Enemy(c, data["fg_c"], data["bg_c"])
        # Create obstacle
        if c in ent_data["obstacles"].keys():
            data = ent_data["obstacles"][c]
            return Obstacle(c, data["fg_c"], data["bg_c"])

    def get_player_data(s):
        return

    def full_display(s):
        for l in s.map:
            for entity in l:
                if not entity:
                    print(" ", end='')
                else:
                    print(entity, end='\x1b[0m')
            print()

    def refresh_display(s):
        """Reprint only the parts which moved during last turn"""
        for update in s.updates:
            print(f"\033[{update.pos.y};{update.pos.y}H{update.entity.__repr__()}")
