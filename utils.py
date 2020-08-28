import time
import json


class Pos(object):
    def __init__(s, y, x):
        s.y = y
        s.x = x

    def __add__(s, other):
        return Pos(s.y + other.y, s.x + other.x)

    def __sub__(s, other):
        return Pos(s.y - other.y, s.x - other.x)


def exit_error(msg):
    print(msg)
    exit()


class Update(object):
    def __init__(s, arg):
        s.arg = arg


class Framerate_handler(object):
    def __init__(s, fps):
        s.last_update = time.time()
        s.delta = 1 / fps

    def do_turn(s):
        if (time.time() - s.last_update) > s.delta:
            s.last_update = time.time()
            return True

# For the old map format, unused.
# It was then loaded this way:
# s.map = [[Entity(c, *attr.get(c, [])) for c in l] for l in map]
def parse_map_file(raw_data):
    splitted_data = [l for l in raw_data.split('\n') if l]
    if splitted_data[0][:10] != "__header__":
        exit_error("Invalid map file, no __header__ tag")
    # Get the header data
    try:
        map_segment_idx = splitted_data.index("__map__")
    except ValueError:
        exit_error("Invalid map file, no __map__ tag")
    else:
        raw_header_infos = splitted_data[1:map_segment_idx]
    # Handle the header data
    attr = {}
    for char_data in raw_header_infos:
        tmp = char_data.split(';')
        if len(tmp) != 3:
            exit_error("Invalid map file, wrong character info parameters")
        attr[tmp[0]] = tmp[1:]
    # Get the map data
    map_data = splitted_data[map_segment_idx + 1:]
    return attr, map_data
