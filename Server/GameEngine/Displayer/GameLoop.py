import time
from os import listdir
from os.path import isfile, join
from pprint import pprint

import pygame
from pygame.locals import *

from utils import Pos, exit_error
from GameEngine.Displayer.config import *


class GameLoop(object):
    def __init__(self, config):
        ### Pygame related ###
        pygame.init()
        self.config = config
        self.tile_size = config['tile_size']
        self.borders_width = config['borders_width']
        # Based on the tile size (px), ensure that the final resolution makes for an even
        # number of tiles
        if config['target_resolution']:
            tmp_screen_size = config['target_resolution']
        else:
            tmp_screen_size = pygame.display.Info()
            tmp_screen_size = Pos(x=tmp_screen_size.current_w, y=tmp_screen_size.current_h)
        self.tiles_nbr =  tmp_screen_size // self.tile_size
        if self.tiles_nbr.x % 2: self.tiles_nbr.x -=1
        if self.tiles_nbr.y % 2: self.tiles_nbr.y -=1
        # Set variables
        self.screen_size = self.tiles_nbr * self.tile_size
        self.hud_tiles_nbr = (config['hud_width_px'] // self.tile_size) + 1
        self.map_tiles_nbr = Pos(x=self.tiles_nbr.x - 3 - self.hud_tiles_nbr, y=self.tiles_nbr.y - 2)
        # Launch display
        self.display = pygame.display.set_mode((self.screen_size.x , self.screen_size.y))
        pygame.display.set_caption('Clippy')
        ### ASSETS ###
        self.font = pygame.font.Font('./GameEngine/Displayer/assets/fonts/Everson_Mono.ttf', 24)
        self.sprites = {}
        self.load_available_sprites(self.tile_size)
        self.last_print_time = time.time()

    def update(self, map, game_state):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        self.display.fill(BLACK)

        self.draw_borders()
        # self.draw_hud(info_list)
        self.draw_map(map, game_state)
        self.draw_entities(map, game_state)

        # SEND INPUTS
        inputs = self.get_inputs()
        # For now just put it in the gamestate
        game_state["players"]['rick']["inputs"] = inputs
        # if inputs:
        #     self.client.dispatch_event(
        #         event_type="MOVE",
        #         player_id=self.client.player_id,
        #         inputs=inputs,
        #     )

        pygame.display.update()
        return game_state

    def draw_entities(self, map, game_state):
        ''' Draw the dynamic entities, which are in the game state '''
        for entity_id, sprite in game_state["components"]["Sprite"].items():
            self.display_entity(
                sprite.sprite_type,
                sprite.region,
                sprite.noise_value,
                game_state["components"]["Position"][entity_id]
            )
        # with self.client.access_game_state() as game_state:
        #     if time.time() - self.last_print_time > 0.5:
        #         self.last_print_time = time.time()
        #     try:
        #         print('COMP', game_state.components['Position'])
        #         # print('COMP', game_state.components['Position'][self.client.entity_id])
        #     except:
        #         print('No player with id found', self.client.entity_id)
        #     # print()
        #     # print('PLAYER', game_state.players)

    def draw_map(self, map, game_state):
        ''' Display the static map, received at the start of the connection '''
        x_idx = 0
        y_idx = 0
        while y_idx < self.map_tiles_nbr.y and y_idx < len(map):
            while x_idx < self.map_tiles_nbr.x and x_idx < len(map[0]):
                pos = Pos(y=y_idx, x=x_idx)
                # print(pos)
                # tile_data = self.client.map[y_idx][x_idx]
                # Take in ECS
                tile_data = map[y_idx][x_idx]
                self.display_entity(*tile_data, pos)
                x_idx += 1
            x_idx = 0
            y_idx += 1

    # def tmp_draw_map(self, map_handler):
    #     """ Draw the map sent by the server, keeping the player at the center of the screen """
    #     needed_lines_top = self.map_tiles_nbr.y // 2 + 2
    #     to_add_top = needed_lines_top - map_handler.player_pos.y
    #     term_y_idx = 0 if to_add_top <= 0 else to_add_top
    #     map_y_idx = 0 if to_add_top >= 0 else -to_add_top
    #
    #     tiles_to_add_left = self.map_tiles_nbr.x // 2 - map_handler.player_pos.x
    #     shift_x = 0 if tiles_to_add_left <= 0 else tiles_to_add_left
    #     shift_x += 1
    #     map_x_start = 0 if tiles_to_add_left >= 0 else -tiles_to_add_left
    #     avail_tiles_right = self.map_tiles_nbr.x // 2
    #     map_x_end = map_handler.player_pos.x + avail_tiles_right
    #
    #     while term_y_idx < self.map_tiles_nbr.y and map_y_idx < len(map_handler.map):
    #         term_y_idx += 1
    #         tmp_line = map_handler.map[map_y_idx][map_x_start:map_x_end]
    #         for x_idx, tile in enumerate(tmp_line):
    #             if tile:
    #                 types = tile.get_types()
    #                 pos = Pos(x=shift_x + x_idx, y=term_y_idx)
    #                 # Lower entity
    #                 if types[1]: self.display_entity(tile.low_ent, tile.noise_value, pos)
    #                 # Top entity
    #                 if types[0]: self.display_entity(tile.top_ent, tile.noise_value, pos)
    #         map_y_idx += 1

    def display_entity(self, sprite_type, region, noise_value, pos):
        """ From the entity type, position and noise value assigned to this position
        (computed server side) draw a sprite"""
        sprite_name = f'{region}_{sprite_type}'
        if sprite_name not in self.sprites.keys():
            sprite_name = sprite_type
            if sprite_name not in self.sprites.keys():
                sprite_name = 'default'
        sprite_idx = int(noise_value * len(self.sprites[sprite_name]))
        self.display.blit(self.sprites[sprite_name][sprite_idx], ((pos + Pos(1, 1)) * self.tile_size).get_xy())

    def draw_hud(self, info_list):
        hud_text_x_start = (3 + self.map_tiles_nbr.x) * self.tile_size
        # Draw title
        text_surface = self.font.render('CLIPPY', False, WHITE)
        self.display.blit(text_surface, (hud_text_x_start, self.tile_size * 2))
        # Draw informations
        y_idx = 5
        for key, value in info_list.items():
            final_str = f"{key}: {value}" if value != None else f"{key}"
            text_surface = self.font.render(final_str, False, WHITE)
            self.display.blit(text_surface, (hud_text_x_start, self.tile_size * y_idx))
            y_idx += 2

    def draw_borders(self):
        # Top border
        for y in range(self.tile_size - self.borders_width, self.tile_size):
            pygame.draw.line(self.display, WHITE,
                                (self.tile_size - self.borders_width, y),
                                (self.screen_size.x - self.tile_size + self.borders_width - 1, y))
        # Bottom border
        for y in range(self.screen_size.y - self.tile_size, self.screen_size.y - self.tile_size + self.borders_width):
            pygame.draw.line(self.display, WHITE,
                                (self.tile_size - self.borders_width, y),
                                (self.screen_size.x - self.tile_size + self.borders_width - 1, y))
        # Left border
        for x in range(self.tile_size - self.borders_width, self.tile_size):
            pygame.draw.line(self.display, WHITE,
                                (x, self.tile_size),
                                (x, self.screen_size.y - self.tile_size))
        # Right border
        for x in range(self.screen_size.x - self.tile_size, self.screen_size.x - self.tile_size + self.borders_width):
            pygame.draw.line(self.display, WHITE,
                                (x, self.tile_size),
                                (x, self.screen_size.y - self.tile_size))
        hud_x_start = (1 + self.map_tiles_nbr.x) * self.tile_size
        # Right Map border
        for x in range(hud_x_start, hud_x_start + self.borders_width):
            pygame.draw.line(self.display, WHITE,
                                (x, self.tile_size),
                                (x, self.screen_size.y - self.tile_size))
        # Left HUD border
        for x in range(hud_x_start + self.tile_size - self.borders_width, hud_x_start + self.tile_size):
            pygame.draw.line(self.display, WHITE,
                                (x, self.tile_size),
                                (x, self.screen_size.y - self.tile_size))
        # Top HUD border
        hud_line_y_start = self.tile_size * 4 + self.tile_size // 2
        for y in range(hud_line_y_start, hud_line_y_start + self.borders_width):
            pygame.draw.line(self.display, WHITE,
                                (hud_x_start + self.tile_size, y),
                                (self.screen_size.x - self.tile_size + self.borders_width - 1, y))

    def draw_grid(self):
        """ Draws a grid on the whole screen, for debugging purposes """
        for y in range(0, self.screen_size.y, self.tile_size):
            pygame.draw.line(self.display, WHITE, (0, y), (self.screen_size.x, y), 1)
        for x in range(0, self.screen_size.x, self.tile_size):
            pygame.draw.line(self.display, WHITE, (x, 0), (x, self.screen_size.y), 1)

    def get_inputs(self):
        """ Convert PyGame inputs into the formatted ones """
        keys = pygame.key.get_pressed()
        res = []
        if keys[K_LEFT] or keys[K_q]: res.append('LEFT')
        if keys[K_RIGHT] or keys[K_d]: res.append('RIGHT')
        if keys[K_UP] or keys[K_z]: res.append('UP')
        if keys[K_DOWN] or keys[K_s]: res.append('DOWN')
        return res

    def load_available_sprites(self, sprite_size):
        no_rot_path = './GameEngine/Displayer/assets/sprites/no_rot_sprites'
        rot_path = './GameEngine/Displayer/assets/sprites'
        # Load sprites with no rotation
        no_rot_sprites = [f[:f.find('.')] for f in listdir(no_rot_path) if isfile(join(no_rot_path, f))]
        rot_sprites = [f[:f.find('.')] for f in listdir(rot_path) if isfile(join(rot_path, f))]
        for sprite_name in no_rot_sprites:
            self.sprites[sprite_name] = [self.load_sprite(no_rot_path, sprite_name)]
        for sprite_name in rot_sprites:
            final_sprite_name = sprite_name[:-2]
            if final_sprite_name in self.sprites:
                self.sprites[final_sprite_name].append(self.load_sprite(rot_path, sprite_name))
            else:
                self.sprites[final_sprite_name] = [self.load_sprite(rot_path, sprite_name)]
        print(f'[+] {len(self.sprites)} sprites loaded')
        # Now create the rotated version of the sprites which need it
        for sprite_name in rot_sprites:
            for angle in [90, 180, 270]:
                self.sprites[sprite_name[:-2]].append(pygame.transform.rotate(self.sprites[sprite_name[:-2]][0], angle))
        print(f'[+] {sum([len(a) for a in self.sprites.values()])} total sprites after rotations')

    def load_sprite(self, path, name):
            tmp_sprite = pygame.image.load(f'{path}/{name}.png')
            # Transform it to a pygame friendly format (quicker drawing)
            tmp_sprite.convert()
            # Scale it to the tile size
            return pygame.transform.scale(tmp_sprite, (self.config['tile_size'], self.config['tile_size']))
