import zlib
import random
import umsgpack
import hashlib
import time
from inspect import signature
# from pprint import pprint
from pygase import GameState, Backend
from GameEngine.Components.Position import Position
from GameEngine.MapGenerator.MapGenerator import MapGenerator
from GameEngine.Displayer.GameLoop import GameLoop
from GameEngine.Displayer.config import *


def chunk_map(bs, n):
    for i in range(0, len(bs), n):
        yield bs[i:i+n]


class ClippyGame(object):
    def __init__(self):
        self.game_loop = GameLoop(DISPLAY_CONFIG)
        self.entity = 10
        self.systems = []
        self.debug_timer = None
        self.map_generator = MapGenerator()
        self.map = self.map_generator.generate_terrain_chunk()
        self.game_state = {
            "players": {0: {
                    "name": "rock",
                    "entity": 1
                }},  # dict with `player_id: player_dict` entries
            "components": { #ugly but it works
                "Position": {},
                "Sprite": {}
            }
        }
        self.tmp_initial_game_state = GameState(
            players={},  # dict with `player_id: player_dict` entries
            components={"Position": {}}
        )
        self.backend = Backend(
            self.tmp_initial_game_state,
            self.time_step,
            event_handlers={
                'MOVE': self.on_move,
                'JOIN': self.on_join,
                'MAP_REQUEST': self.on_map_request
                }
        )
        self.add_system(self.movement_system)
        self.add_system(self.debug_system)
        self.on_join(0, self.tmp_initial_game_state, "128.1.1.2")


    def movement_system(self, game_state, dt):
        position_update = {}
        inputs_update = {}
        for id, player in game_state.players.items():
            player_entity = player["entity"]
            player_inputs = game_state.components["Inputs"][player_entity]
            if len(player_inputs) == 0:
                continue
            x = y = 0
            for input in player_inputs:
                if input == "UP":
                    y += 1
                elif input == "DOWN":
                    y -= 1
                elif input == "RIGHT":
                    x += 1
                elif input == "LEFT":
                    x -= 1
            inputs_update[player_entity] = []
            position_update[player_entity] = game_state.components["Position"][player_entity] + Position(y, x)
        return {"components": {"Position": position_update, "Inputs": inputs_update}}

    def debug_system(self, game_state, dt):
        if self.debug_timer is None:
            self.debug_timer = time.time()
            return {}
        now = time.time()
        if now - self.debug_timer > 5:
            print("Position: ", game_state.components["Position"])
            self.debug_timer = now
        return {}

    def time_step(self, game_state, dt):
        # Before a player joins, updating the game state is unnecessary.
        # if len(game_state.players) == 0:
        #     return {}
        updates = {}
        for function in self.systems:
            if str(signature(function)) != "()":
                system_updates = function(game_state, dt)
            else:
                system_updates = function()
            updates.update(system_updates)
        # tmp
        self.game_state = self.game_loop.update(self.map, self.game_state)
        print(self.game_state)
        return {"updates":"jej"}

    def new_entity(self):
        new_entity = self.entity
        self.entity += 1
        return new_entity

    def delete_id(self, id):
        """delete every component of id"""
        pass

    def get_component(self, component, entity=None):
        if component.__name__ not in self.game_state["components"]:
            print("No component " + component.__name__ + " stored.")
            return []
        if entity is None:
            return self.game_state["components"][component.__name__]
        if entity not in self.game_state["components"][component.__name__]:
            print("No component " + component.__name__ + " for id " + entity + " stored.")
            return None
        return self.game_state["components"][component.__name__][entity]

    def add_component(self, entity, component):
        if type(component).__name__ not in self.game_state["components"]:
            self.game_state["components"][type(component).__name__] = {}
        self.game_state["components"][type(component).__name__][entity] = component

    def filter(self, type0, *types):
        if type0.__name__ not in self.game_state["components"]:
            return []
        list_ids = list(self.game_state["components"][type0.__name__].keys())
        for typ in types:
            if type0.__name__ in self.game_state["components"]:
                ids = list(self.game_state["components"][typ.__name__].keys())
                for id in list_ids:
                    if id not in ids:
                        list_ids.remove(id)
        return list_ids

    def add_system(self, function):
        self.systems.append(function)

    def run(self):
        self.backend.run("0.0.0.0", 8080)

    def on_move(self, player_id, inputs, game_state, **kwargs):
        print(f"received inputs from client id n°{player_id}: {inputs!r}")
        if player_id not in game_state.players:
            return {}
        player_entity = game_state.players[player_id]["entity"]
        return {
            "components": {
                    "Inputs": {player_entity: inputs}
            }
        }

    def on_join(self, player_name, game_state, client_address, **kwargs):
        print(f"{player_name} joined.")
        player_id = len(game_state.players)
        player_entity = self.new_entity()
        # Notify client that the player successfully joined the game.
        # self.backend.server.dispatch_event("PLAYER_CREATED", player_id, player_entity, target_client=client_address)
        return {
            "components": {
                "Position": {
                    player_entity: Position(0, 0),
                },
                "Inputs": {
                    player_entity: []
                }
            },
            "players": {
                player_id: {
                    "name": player_name,
                    "entity": player_entity
                }
            }
        }

    def on_map_request(self, client_address, **kwargs):
        print(f"player at adress {client_address} asked for the map")
        packed = umsgpack.packb(self.map)
        print(f"packed map length is : {len(packed)}")
        compressed_data = zlib.compress(packed)
        print(f"bytestring hash is {hashlib.md5(compressed_data).hexdigest()}")
        splitted = list(chunk_map(compressed_data, 256))
        nchunks = len(splitted)
        for i, bs in enumerate(splitted):
            finished = True if i == nchunks - 1 else False
            self.backend.server.dispatch_event("MAP_RESPONSE", finished, i, bs, target_client=client_address)
        return {}


ecs = ClippyGame()
