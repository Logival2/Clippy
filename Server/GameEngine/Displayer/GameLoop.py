import time
from os import listdir
from os.path import isfile, join
from pprint import pprint

import pygame
from pygame.locals import *

from GameEngine.Displayer.utils import exit_error
from GameEngine.Displayer.config import *
from GameEngine.Components.Position import Position


class GameLoop(object):
    def __init__(self, config):
        ### Pygame related
        pygame.init()
        self.config = config
        self.tile_size = config['tile_size']
        self.borders_width = config['borders_width']
        # Based on the tile size (px), ensure that the final resolution
        # will result in an even number of tiles
        if config['target_resolution']:
            tmp_screen_size = config['target_resolution']
        else:
            tmp_screen_size = pygame.display.Info()
            tmp_screen_size = Position(
                x=tmp_screen_size.current_w,
                y=tmp_screen_size.current_h
            )
        self.tiles_nbr = tmp_screen_size // self.tile_size
        # Always get an even number of tiles ? Don't remember why I did that
        if self.tiles_nbr.x % 2: self.tiles_nbr.x -=1
        if self.tiles_nbr.y % 2: self.tiles_nbr.y -=1
        ### Now set variables:
        # Number of tiles total
        self.screen_size = self.tiles_nbr * self.tile_size
        # Number of horizontal tiles for the HUD
        self.hud_tiles_nbr = (config['hud_width_px'] // self.tile_size) + 1
        # Number of tiles for the map
        self.map_tiles_nbr = Position(
            x=self.tiles_nbr.x - 3 - self.hud_tiles_nbr,
            y=self.tiles_nbr.y - 2
        )
        self.mid_map_position = Position(
            y=self.map_tiles_nbr.y // 2,
            x=self.map_tiles_nbr.x // 2
        )
        self.player_pos = None
        ### Launch display
        self.display = pygame.display.set_mode((self.screen_size.x , self.screen_size.y))
        pygame.display.set_caption('Clippy')
        ### ASSETS ###
        self.font = pygame.font.Font('./GameEngine/Displayer/assets/fonts/Everson_Mono.ttf', 24)
        self.sprites = {}
        self.load_available_sprites(self.tile_size)
        # self.last_print_time = time.time()
        self.clock = pygame.time.Clock()

    def update(self, map, game_state):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        self.display.fill(BLACK)

        self.draw_borders()
        self.player_pos = game_state["components"]["Position"][1]
        # self.draw_hud(info_list)
        self.draw_map(map, game_state)
        self.draw_entities(map, game_state)

        # SEND INPUTS
        inputs = self.get_inputs()
        # For now just put it in the game_state, check if player exists
        if 0 in game_state["players"]:
            game_state["players"][0]["inputs"] = inputs
        # if inputs:
        #     self.client.dispatch_event(
        #         event_type="MOVE",
        #         player_id=self.client.player_id,
        #         inputs=inputs,
        #     )
        pygame.display.update()
        self.clock.tick(144)
        return game_state

    def draw_entities(self, map, game_state):
        ''' Draw the dynamic entities, which are in the game state '''
        for entity_id, sprite in game_state["components"]["Sprite"].items():
            entity_position = game_state["components"]["Position"][entity_id]
            entity_screen_position = self.map_pos_to_screen_pos(entity_position)
            if not entity_screen_position: continue  # Out of screen
            self.display_entity(
                sprite.sprite_type,
                sprite.region,
                sprite.noise_value,
                entity_screen_position
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

    def screen_pos_to_map_pos(self, screen_pos):
        return self.player_pos + screen_pos - self.mid_map_position

    def map_pos_to_screen_pos(self, map_pos):
        screen_pos = map_pos + self.mid_map_position - self.player_pos
        if screen_pos >> Position(0, 0) and screen_pos << self.map_tiles_nbr - Position(1, 1):
            return screen_pos
        # Off screen position, return None

    def draw_map(self, map, game_state):
        ''' Display the static map, received at the start of the connection
        and keep the player at the center of the screen '''
        for y_idx in range(self.map_tiles_nbr.y):
            for x_idx in range(self.map_tiles_nbr.x):
                screen_pos = Position(y=y_idx, x=x_idx)
                map_pos = self.screen_pos_to_map_pos(screen_pos)
                line = map.get(map_pos.y, None)
                if not line: continue
                tile = line.get(map_pos.x, None)
                if not tile: continue
                self.display_entity(*tile, screen_pos)

    def display_entity(self, sprite_type, region, noise_value, screen_pos):
        """ From the entity type, position and noise value assigned to this position
        (computed server side) draw a sprite"""
        sprite_name = f'{region}_{sprite_type}'
        if sprite_name not in self.sprites.keys():
            sprite_name = sprite_type
            if sprite_name not in self.sprites.keys():
                sprite_name = 'default'
        sprite_idx = int(noise_value * len(self.sprites[sprite_name]))
        self.display.blit(
            self.sprites[sprite_name][sprite_idx],
            ((screen_pos + Position(1, 1)) * self.tile_size).get_xy()
        )

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
        self.load_sprite_folder(
            "./GameEngine/Displayer/assets/sprites",
            sprite_size
        )
        self.load_sprite_folder(
            "./GameEngine/Displayer/assets/sprites/no_rot_sprites",
            sprite_size, rotate=False
        )
        self.load_sprite_folder(
            "./GameEngine/Displayer/assets/sprites/no_rot_sprites/no_flip_sprites",
            sprite_size, rotate=False, flip=False
        )
        print(f'[+] {len(self.sprites)} sprites loaded:')
        # pprint(self.sprites)

    def load_sprite_folder(self, folder_path, sprite_size, rotate=True, flip=True):
        sprites_names = [f[:f.find('.')] for f in listdir(folder_path) if isfile(join(folder_path, f))]
        for sprite_name in sprites_names:
            final_sprite_name = sprite_name[:-2]
            final_sprite_list = []

            final_sprite_list.append(self.load_sprite(folder_path, sprite_name))

            if rotate:
                for angle in [90, 180, 270]:
                    final_sprite_list.append(pygame.transform.rotate(final_sprite_list[0], angle))
            # Now create the flipped version of all the sprites (also those created by the rotation)
            if flip:
                new_images = []
                for sprite in final_sprite_list:
                    new_images.append(pygame.transform.flip(sprite, True, False))
                final_sprite_list += new_images
            self.sprites[final_sprite_name] = final_sprite_list

    def load_sprite(self, path, name):
            tmp_sprite = pygame.image.load(f'{path}/{name}.png')
            # Transform it to a pygame friendly format (quicker drawing)
            tmp_sprite.convert()
            # Scale it to the tile size
            return pygame.transform.scale(tmp_sprite, (self.config['tile_size'], self.config['tile_size']))
