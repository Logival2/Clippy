from pprint import pprint
import random

from pygase import GameState, Backend

from utils import Pos
from GameEngine.MapGenerator.MapGenerator import MapGenerator
from GameEngine.map_config import MAP_CONFIG


class ClippyGame(object):
    def __init__(self):
        random.seed(MAP_CONFIG['seed'])
        self.entity = 0
        self.systems = []
        self.components = {}
        self.map_generator = MapGenerator(MAP_CONFIG)
        self.map = self.map_generator.generate_terrain_chunk()
        self.initial_game_state = GameState(
            players={},  # dict with `player_id: player_dict` entries
        )
        self.backend = Backend(
            self.initial_game_state,
            self.time_step,
            event_handlers={'MOVE': self.on_move, 'JOIN': self.on_join}
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
        if component.__name__ not in self.components:
            print("No component " + component.__name__ + " stored.")
            return []
        if entity is None:
            return self.components[component.__name__]
        if entity not in self.components[component.__name__]:
            print("No component " + component.__name__ + " for id " + entity + " stored.")
            return None
        return self.components[component.__name__][entity]

    def add_component(self, entity, component):
        if type(component).__name__ not in self.components:
            self.components[type(component).__name__] = {}
        self.components[type(component).__name__][entity] = component

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
        self.backend.server.dispatch_event("PLAYER_CREATED", player_id, self.map, target_client=client_address)
        return {
            # Add a new entry to the players dict
            "players": {player_id: {"name": player_name}}
        }
