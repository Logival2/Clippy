#!/usr/bin/env python3
from pprint import pprint

import pygame
import pygame_menu
from pygase import Client

from MainMenuLoop import MainMenuLoop
from GameLoop import GameLoop
from config import *


class NetworkClient(Client):
    '''Subclass pygase classes to scope event handlers and game-specific variables.'''
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.map = None
        # The backend will send a "PLAYER_CREATED" event in response to a "JOIN" event.
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)

    def on_player_created(self, player_id, map):
        '''"PLAYER_CREATED" event handler'''
        # Remember the id the backend assigned the player.
        self.player_id = player_id
        self.map = map

class App(object):
    def __init__(self):
        self.client = NetworkClient()
        self.game_loop = GameLoop(DISPLAY_CONFIG, self.client)
        # Final window size is needed as the window size
        # will shrink to adapt to the tile size specified in config.py
        self.main_menu_loop = MainMenuLoop(self.game_loop.screen_size, self.client)
        self.active_loop = self.main_menu_loop
        self.clock = pygame.time.Clock()

    def __del__(self):
        if self.client.connection is not None:
            self.client.disconnect()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    if self.client.connection is not None:
                        self.client.disconnect()
                    exit()
            if not self.active_loop.update(events, self.game_loop.display):
                self.active_loop = self.game_loop
                self.map = self.client.map
                pprint(self.map)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
