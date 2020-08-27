from utils import *


class Map(object):
    def __init__(s, input):
        s.updates = []
        if isinstance(input, Pos):
            # Map Generator
            s.map = []
            for y in range(input.y):
                line = [Entity('x')] * input.x
                s.map.append(line)
        else:
            with open(f"./maps/{input}.map", 'r') as f:
                data = f.read()
            attr, map = parse_map_file(data)
            # Build a double array containing Entity objects with
            # the colors specified in the map header
            s.map = [[Entity(c, *attr.get(c, [])) for c in l] for l in map]
        # Print the map entirely for the first time
        for l in s.map:
            for entity in l:
                print(entity, end=' \x1b[0m')
            print()

    def refresh_display(s):
        for update in s.updates:
            print(f"\033[{update.pos.y};{update.pos.y}H{update.entity.__repr__()}")


class Entity(object):
    def __init__(s, repr_char, fg_color=39, bg_color=49):
        s.repr_char = repr_char
        s.fg_color = fg_color
        s.bg_color = bg_color

    def __repr__(s):
        return f"\x1b[{s.bg_color};{s.fg_color}m{s.repr_char}"


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
