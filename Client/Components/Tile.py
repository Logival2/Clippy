from enum import Enum


class Types(Enum):
    GRASS = 0
    GRAVEL = 1
    LAVA = 2
    SAND = 3
    STONE = 4
    WATER = 5


class Tile(object):
    def __init__(s, tile=0):
        s.type = Types(tile)
        pass
