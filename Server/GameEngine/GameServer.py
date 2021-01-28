import time
import random
from pygase import GameState, Backend
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


class ClippyGame(object):
    """docstring for Clippy_Game."""

    def __init__(self):
        super(ClippyGame, self).__init__()
        self.entity = 0
        self.systems = []
        self.components = {}
        self.initial_game_state = GameState(
            players={},  # dict with `player_id: player_dict` entries
        )
        self.map_handler = MapHandler()
        self.map = Map(self)
        self.backend = Backend(
            self.initial_game_state,
            self.time_step,
            event_handlers={"MOVE": self.on_move, "JOIN": self.on_join}
        )
        self.add_system(self.movement_system)

    def movement_system(self, gamestate, dt):
        return {}

    def time_step(self, game_state, dt):
        # Before a player joins, updating the game state is unnecessary.
        if len(game_state.players) == 0:
            return {}
        updates = {}
        for function in self.systems:
            system_updates = function(game_state, dt)
            updates.update(system_updates)
        return updates

    def new_entity(self):
        self.entity += 1
        return self.entity

    def get_component(self, component, entity=None):
        if type(component()).__name__ not in self.components:
            print("No component " + type(component()).__name__ + " stored.")
            return []
        if entity is None:
            return self.components[type(component()).__name__]
        return next(item for item in self.components[type(component()).__name__] if item["entity"] == entity)['component']

    def add_component(self, entity, component):
        if type(component).__name__ not in self.components:
            self.components[type(component).__name__] = []
        self.components[type(component).__name__].append({"entity": entity, "component": component})

    def add_system(self, function):
        self.systems.append(function)

    def run(self):
        self.backend.run("127.0.0.1", 8080)

    def on_move(self, player_id, inputs, **kwargs):
        print(f"received inputs from client id n°{player_id}: {inputs!r}")
        return {}

    def on_join(self, player_name, game_state, client_address, **kwargs):
        print(f"{player_name} joined.")
        player_id = len(game_state.players)
        # Notify client that the player successfully joined the game.
        self.backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
        return {
            # Add a new entry to the players dict
            "players": {player_id: {"name": player_name, "position": (random.random() * 640, random.random() * 420)}}
        }
