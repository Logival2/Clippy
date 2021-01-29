import time

from GameEngine.Components.Tile import Tile
from GameEngine.MapHandler import MapHandler
from config import MAP_PARAMETERS


class Chunk(object):
    def __init__(s):
        s.tiles = [[]]
        for x in range(MAP_PARAMETERS["size"]):
            s.tiles.append([])
            for y in range(MAP_PARAMETERS["size"]):
                s.tiles[x].append({})


class Map(object):
    def __init__(s, _ecs):
        s._ecs = _ecs
        s.chunks = {}
        pass

    def get_tile(s, x, y):
        if x not in s.chunks:
            s.chunks[x] = {}
        if y not in s.chunks[x]:
            s.chunks[x][y] = Tile(0)
        return s.chunks[x][y]

# TODO add filter
class Ecs(object):
    def __init__(s):
        s.components = {}
        s.updates = []
        s.entity = 0
        s.tick = 60
        s.last_timestamp = int(round(time.time() * 1000))
        s.map_handler = MapHandler()
        s.map = Map(s)

    def new_entity(s):
        s.entity += 1
        return s.entity

    def get_component(s, component, entity=None):
        if type(component()).__name__ not in s.components:
            print("No component " + type(component()).__name__ + " stored.")
            return []
        if entity is None:
            return s.components[type(component()).__name__]
        return s.components[type(component()).__name__][entity]

    def add_component(s, entity, component):
        if type(component).__name__ not in s.components:
            s.components[type(component).__name__] = {}
        s.components[type(component).__name__][entity] = component

    def add_update(s, function):
        s.updates.append(function)

    def update(s):
        for function in s.updates:
            function()
        time.sleep(max((1000/s.tick - (int(round(time.time() * 1000)) - s.last_timestamp))/1000, 0))
        s.last_timestamp = int(round(time.time() * 1000))


ecs = Ecs()
