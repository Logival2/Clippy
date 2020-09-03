import copy
import math
import random
import string

from utils import Pos


WALL_CHAR = 'w'
FLOOR_CHAR = 'f'


class MapGenerator(object):
    def __init__(s, size, room_placement_attemps_nbr=50):
        s.size = size
        s.map = []
        s.rooms = []
        s.erased_poses = []
        s.done_poses = []
        s.cardinal_neighbors_deltas = [Pos(-1, 0), Pos(0, -1), Pos(0, 1), Pos(1, 0)]
        s.neighbors_delta = s.cardinal_neighbors_deltas + [Pos(-1, -1), Pos(-1, 1), Pos(1, -1), Pos(1, 1)]
        for y in range(size.y):
            s.map.append([WALL_CHAR]*size.x)
        s.room_placement_attemps_nbr = size.x // 2
        for _ in range(room_placement_attemps_nbr):
            s.erased_poses.clear()
            s.place_room()
            # break
        # s.print_map()
        # print(s.rooms)
        s.place_player()

    def place_player(s):
        for y, l in enumerate(s.map):
            for x, c in enumerate(l):
                if c == FLOOR_CHAR:
                    s.map[y][x] = 'p'
                    return

    def get_map(s):
        res = ""
        for l in s.map:
            tmp_buf = ""
            for c in l:
                tmp_buf += c
            res += tmp_buf + "\n"
        return res

    def place_room(s):
        # room_char = random.choice(string.ascii_letters)
        room_char = FLOOR_CHAR
        room_type = random.choice(["natural", "square", "square"])
        room_center = Pos(random.randint(2, s.size.y - 1), random.randint(2, s.size.x - 1))
        while not s.check_surroundings(room_center):
            room_center = Pos(random.randint(2, s.size.y - 1), random.randint(2, s.size.x - 1))
        room_size = Pos(
                        int(random.gauss(
                            (2 + (s.size.y // 5)) / 2, 4)),
                        int(random.gauss(
                            (2 + (s.size.x // 5)) / 2, 4))
                    )
        # print(room_center, room_size.x )
        if room_type == "square":
            y_min = max(1,          room_center.y - room_size.y // 2)
            y_max = min(s.size.y - 1, room_center.y + room_size.y // 2)
            x_min = max(1,          room_center.x - room_size.x // 2)
            x_max = min(s.size.x - 1, room_center.x + room_size.x // 2)
            # Check avail
            for y in range(y_min - 1, y_max + 1):
                for x in range(x_min - 1, x_max + 1):
                    if s.map[y][x] == room_char:
                        return map
            s.rooms.append(room_center)
            # Carve room
            for y in range(y_min, y_max):
                for x in range(x_min, x_max):
                    s.map[y][x] = room_char
        elif room_type == "natural":
            # print("------------\nStarting carving")
            s.map[room_center.y][room_center.x] = room_char
            s.erased_poses.append(room_center)
            s.done_poses.append(room_center)
            s.carve_surroundings(room_center, room_size.x, room_char)

    def carve_surroundings(s, start_pos, size_left, room_char):
        if size_left <= 0 or start_pos.x < 2 or start_pos.x > len(s.map[0]) - 3 or start_pos.y < 2 or start_pos.y > len(s.map) - 3:
            # print("ended")
            return
        size_left -= 1
        for neighbor_delta in s.cardinal_neighbors_deltas:
            absolute_pos = start_pos + neighbor_delta
            if absolute_pos in s.done_poses:
                continue
            s.done_poses.append(absolute_pos)
            if s.check_surroundings(absolute_pos):
                s.map[absolute_pos.y][absolute_pos.x] = room_char
                s.erased_poses.append(absolute_pos)
                s.carve_surroundings(absolute_pos, size_left, room_char)
        # print("going up!")

    def check_surroundings(s, start_pos):
        holes_count = 0
        for neighbor_delta in s.neighbors_delta:
            absolute_pos = start_pos + neighbor_delta
            if not s.is_valid_pos(absolute_pos):
                continue
            if s.map[absolute_pos.y][absolute_pos.x] != WALL_CHAR:
                if absolute_pos not in s.erased_poses:
                    holes_count += 1
                    # print(f"hole found, sp={start_pos}, hole={absolute_pos}, list={erased_poses}")
        return holes_count == 0

    def is_valid_pos(s, pos):
        return pos.x >= 0 and pos.x < len(s.map[0]) and pos.y >= 0 and pos.y < len(s.map)

    def print_map(s):
        for l in s.map:
            tmp_buf = ""
            for c in l:
                tmp_buf += (c * 2)
            print(tmp_buf)

if __name__ == '__main__':
    map_g = MapGenerator(Pos(40, 100))
