import json
import time

from opensimplex import OpenSimplex

from utils import Pos
from MapGenerator.voronoi import generate_voronoi


class MapGenerator(object):
    def __init__(s, map_size, seed=0):
        s.map_size = map_size
        s.simplex = OpenSimplex(seed)
        s.map = generate_voronoi(
                            width=map_size.x,
                            height=map_size.y,
                            values=['f', 'w', 'g', 'l', 'e'])
        s.map[map_size.y // 2][map_size.x // 2] = 'p'

    def get_map(s):
        str = [''.join(l) for l in s.map]
        str = '\n'.join(str)
        return str
