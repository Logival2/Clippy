#!/usr/bin/env python3
import zlib
import time
import hashlib
from pprint import pprint

import umsgpack
import pygame
import pygame_menu
from pygase import Client

from MainMenuLoop import MainMenuLoop
from GameLoop import GameLoop
from config import *


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
            # The main menu returns false when the player is connected
            # Will need to change to accomodate pause menus etc...
            if not self.active_loop.update(events, self.game_loop.display):
                self.end_main_menu()

            pygame.display.update()
            self.clock.tick(60)

    def end_main_menu(self):
        print('Quitting menu')
        # Load map

        print('Downloading map...')
        self.client.dispatch_event('MAP_REQUEST')
        start_time = time.time()
        # Wait for map loading
        # if it never happens we let the player kill the program
        while self.client.map_dl_is_complete is not True:
            time.sleep(0.1)
        self.active_loop = self.game_loop


class NetworkClient(Client):
    '''Subclass pygase classes to scope event handlers and game-specific variables.'''
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.map = None
        self.map = []
        self.map_dl_is_complete = False
        # The backend will send a "PLAYER_CREATED" event in response to a "JOIN" event.
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)
        self.register_event_handler("MAP_RESPONSE", self.on_map_response)

    def on_player_created(self, player_id):
        '''"PLAYER_CREATED" event handler'''
        # Remember the id the backend assigned the player.
        self.player_id = player_id

    def on_map_response(self, dl_is_complete, chunk_num, map_datagram):
        self.map.append((chunk_num, map_datagram))
        if dl_is_complete:
            print('[+] - Map download complete')
            self.map.sort(key=lambda x: x[0])
            self.map = b''.join([x for _, x in self.map])
            print('Maphash:', hashlib.md5(self.map).hexdigest())
            self.map = zlib.decompress(self.map)
            self.map = umsgpack.unpackb(self.map)
            self.map_dl_is_complete = True


if __name__ == '__main__':
    app = App()
    app.run()
