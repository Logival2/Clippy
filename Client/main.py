#!/usr/bin/env python3
from pprint import pprint

import pygame
import pygame_menu
from pygase import Client

from MainMenuLoop import MainMenuLoop
from GameLoop import GameLoop
from config import *


class ChaseClient(Client):
    '''Subclass pygase classes to scope event handlers and game-specific variables.
    '''
    def __init__(self):
        super().__init__()
        self.player_id = None
        # The backend will send a "PLAYER_CREATED" event in response to a "JOIN" event.
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)

    def on_player_created(self, player_id):
        '''"PLAYER_CREATED" event handler'''
        # Remember the id the backend assigned the player.
        self.player_id = player_id


class App(object):
    def __init__(s):
        s.client = ChaseClient()
        s.game_loop = GameLoop(DISPLAY_CONFIG)
        # Final window size is needed as the window size
        # will shrink to adapt to the tile size specified in config.py
        s.main_menu_loop = MainMenuLoop(s.game_loop.screen_size, s.client)
        s.active_loop = s.main_menu_loop
        s.clock = pygame.time.Clock()

    def run(s):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    s.client.disconnect()
                    exit()
            if not s.active_loop.update(events, s.game_loop.display):
                s.active_loop = s.game_loop
            pygame.display.update()
            s.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
