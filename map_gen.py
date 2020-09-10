import copy
import math
import random
import string

from utils import Pos


WALL_CHAR = 'w'
FLOOR_CHAR = 'f'


class MapGenerator(object):
    def __init__(s, size, seed=0, room_placement_attemps_nbr=3):
        random.seed(seed)
        s.size = size
        s.map = []
        s.rooms = []
        s.erased_poses = []
        s.done_poses = []
        s.cardinal_neighbors_deltas = [Pos(-1, 0), Pos(0, -1), Pos(0, 1), Pos(1, 0)]
        s.neighbors_delta = s.cardinal_neighbors_deltas + [Pos(-1, -1), Pos(-1, 1), Pos(1, -1), Pos(1, 1)]
        for y in range(size.y):
            s.map.append([WALL_CHAR]*size.x)
        s.room_placement_attemps_nbr = size.x // 3
        for _ in range(s.room_placement_attemps_nbr):
            s.erased_poses.clear()
            s.place_room()
            # break
        # s.print_map()
        print(f"{len(s.rooms)} rooms")
        for room_idx, room in enumerate(s.rooms):
            # print("doing room", room_idx)
            rooms_left = copy.copy(s.rooms)
            rooms_left.remove(room)

            corr_nbr = abs(int(random.gauss(0, 3)))
            while corr_nbr == 0:
                corr_nbr = abs(int(random.gauss(0, 3)))
            corr_nbr = min(corr_nbr, len(rooms_left))

            # print("corr_nbr=", corr_nbr)

            for _ in range(0, corr_nbr):
                # print("tour de dig")
                target = random.choice(rooms_left)
                s.dig_tunnel(room, target)
        s.place_player()
        # s.dig_tunnel(Pos(3, 3), Pos(13, 20))
        # s.map[3][3] = 'p'
        # exit()

    def place_player(s):
        for y, l in enumerate(s.map):
            for x, c in enumerate(l):
                if c == FLOOR_CHAR:
                    s.map[y][x] = 'p'
                    return

    def dig_tunnel(s, start, end):
        # print(f"digging from {start} to {end}")
        lower_x = end
        upper_x = start
        if start.x < end.x:
            lower_x = start
            upper_x = end
        lower_y = end
        upper_y = start
        if start.y < end.y:
            lower_y = start
            upper_y = end

        x_idx = lower_x.x
        while x_idx < upper_x.x + 1:
            s.map[start.y][x_idx] = FLOOR_CHAR
            x_idx += 1
            # print("tour x")
        y_idx = lower_y.y
        while y_idx < upper_y.y:
            s.map[y_idx][x_idx] = FLOOR_CHAR
            y_idx += 1
            # print("tour y")

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
            for y in [y_min - 1, y_max + 1]:
                for x in range(x_min - 1, x_max + 1):
                    if random.randint(1, 4) > 3:
                        hole = Pos(y, x)
                        if s.is_valid_pos(hole, 1):
                            s.map[hole.y][hole.x] = room_char
                            s.erased_poses.append(hole)
                            s.done_poses.append(hole)
                            s.carve_surroundings(hole, random.randint(0, 3), room_char)


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
        s.rooms.append(room_center)

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

    def is_valid_pos(s, pos, delta=0):
        return pos.x >= delta and pos.x < len(s.map[0]) - delta and pos.y >= delta and pos.y < len(s.map) - delta

    def print_map(s):
        for l in s.map:
            tmp_buf = ""
            for c in l:
                tmp_buf += (c * 2)
            print(tmp_buf)


if __name__ == '__main__':
    map_g = MapGenerator(Pos(40, 100))
