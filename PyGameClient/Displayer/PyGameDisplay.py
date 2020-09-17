import time
from os import listdir
from os.path import isfile, join

import pygame
from pygame.locals import *

from utils import Pos
from Displayer.config import *


class PyGameDisplay(object):
    def __init__(s, config):
        ### Pygame related ###
        pygame.init()
        s.tile_size = config['tile_size']
        s.borders_width = config['borders_width']
        # Based on the tile size (px), ensure that the final resolution makes for an even
        # number of tiles
        if config['target_resolution']:
            tmp_screen_size = config['target_resolution']
        else:
            tmp_screen_size = pygame.display.Info()
            tmp_screen_size = Pos(x=tmp_screen_size.current_w, y=tmp_screen_size.current_h)
        s.tiles_nbr =  tmp_screen_size // s.tile_size
        if s.tiles_nbr.x % 2: s.tiles_nbr.x -=1
        if s.tiles_nbr.y % 2: s.tiles_nbr.y -=1
        # Set variables
        s.screen_size = s.tiles_nbr * s.tile_size
        s.hud_tiles_nbr = (config['hud_width_px'] // s.tile_size) + 1
        s.map_tiles_nbr = Pos(x=s.tiles_nbr.x - 3 - s.hud_tiles_nbr, y=s.tiles_nbr.y - 2)
        # Launch display
        s.display = pygame.display.set_mode((s.screen_size.x , s.screen_size.y))
        pygame.display.set_caption('Clippy')
        ### FPS related ###
        s.delta = 1 / config['fps']
        s.frame_start = time.time()
        ### ASSETS ###
        # s.font = pygame.font.Font('Displayer/fonts/CozetteVector.ttf', 24)
        s.font = pygame.font.Font('Displayer/fonts/Everson_Mono.ttf', 24)
        s.images = {}
        s.load_available_images(16)

    def __del__(s):
        pygame.quit()

    def draw(s, map_handler, info_list):
        s.display.fill(BLACK)
        s.draw_borders()
        s.draw_hud(info_list)
        s.draw_map(map_handler)
        # s.draw_grid()  # Useful for debugging
        pygame.display.update()
        s.handle_sleep()

    def draw_map(s, map_handler):
        """ Draw the map sent by the server, keeping the player at the center of the screen """
        needed_lines_top = s.map_tiles_nbr.y // 2 + 2
        to_add_top = needed_lines_top - map_handler.player_pos.y
        term_y_idx = 0 if to_add_top <= 0 else to_add_top
        map_y_idx = 0 if to_add_top >= 0 else -to_add_top

        tiles_to_add_left = s.map_tiles_nbr.x // 2 - map_handler.player_pos.x
        shift_x = 0 if tiles_to_add_left <= 0 else tiles_to_add_left
        shift_x += 1
        map_x_start = 0 if tiles_to_add_left >= 0 else -tiles_to_add_left
        avail_tiles_right = s.map_tiles_nbr.x // 2
        map_x_end = map_handler.player_pos.x + avail_tiles_right

        while term_y_idx < s.map_tiles_nbr.y and map_y_idx < len(map_handler.map):
            term_y_idx += 1
            tmp_line = map_handler.map[map_y_idx][map_x_start:map_x_end]
            for x_idx, tile in enumerate(tmp_line):
                if tile:
                    types = tile.get_types()
                    pos = Pos(x=shift_x + x_idx, y=term_y_idx)
                    # Lower entity
                    if types[1]: s.display_entity(tile.low_ent, tile.noise_value, pos)
                    # Top entity
                    if types[0]: s.display_entity(tile.top_ent, tile.noise_value, pos)
            map_y_idx += 1

    def display_entity(s, ent, noise_value, pos):
        """ Get an entity type, position and the noise value assigned to this position
        (computed server side) and draws it"""
        name = 'fallback'
        img_idx = 0
        if not ent: return
        if ent.type != 'player' and ent.type != 'fallback':
            name = f'{ent.region}_{ent.type}'
        else:
            name = ent.type
        if name in s.images.keys():
            img_idx = int(noise_value * IMAGES[name][0])
        s.display.blit(s.images[name][img_idx], (pos * s.tile_size).get_tuple())

    def draw_hud(s, info_list):
        hud_text_x_start = (3 + s.map_tiles_nbr.x) * s.tile_size
        # Draw title
        text_surface = s.font.render('CLIPPY', False, WHITE)
        s.display.blit(text_surface, (hud_text_x_start, s.tile_size * 2))
        # Draw informations
        y_idx = 4
        for key, value in info_list.items():
            final_str = f"{key}: {value}" if value != None else f"{key}"
            text_surface = s.font.render(final_str, False, WHITE)
            s.display.blit(text_surface, (hud_text_x_start, s.tile_size * y_idx))
            y_idx += 1

    def draw_borders(s):
        # Top border
        for y in range(s.tile_size - s.borders_width, s.tile_size):
            pygame.draw.line(s.display, WHITE,
                                (s.tile_size - s.borders_width, y),
                                (s.screen_size.x - s.tile_size + s.borders_width - 1, y))
        # Bottom border
        for y in range(s.screen_size.y - s.tile_size, s.screen_size.y - s.tile_size + s.borders_width):
            pygame.draw.line(s.display, WHITE,
                                (s.tile_size - s.borders_width, y),
                                (s.screen_size.x - s.tile_size + s.borders_width - 1, y))
        # Left border
        for x in range(s.tile_size - s.borders_width, s.tile_size):
            pygame.draw.line(s.display, WHITE,
                                (x, s.tile_size),
                                (x, s.screen_size.y - s.tile_size))
        # Right border
        for x in range(s.screen_size.x - s.tile_size, s.screen_size.x - s.tile_size + s.borders_width):
            pygame.draw.line(s.display, WHITE,
                                (x, s.tile_size),
                                (x, s.screen_size.y - s.tile_size))
        hud_x_start = (1 + s.map_tiles_nbr.x) * s.tile_size
        # Right Map border
        for x in range(hud_x_start, hud_x_start + s.borders_width):
            pygame.draw.line(s.display, WHITE,
                                (x, s.tile_size),
                                (x, s.screen_size.y - s.tile_size))
        # Left HUD border
        for x in range(hud_x_start + s.tile_size - s.borders_width, hud_x_start + s.tile_size):
            pygame.draw.line(s.display, WHITE,
                                (x, s.tile_size),
                                (x, s.screen_size.y - s.tile_size))
        # Top HUD border
        hud_line_y_start = s.tile_size * 3 + s.tile_size // 2
        for y in range(hud_line_y_start, hud_line_y_start + s.borders_width):
            pygame.draw.line(s.display, WHITE,
                                (hud_x_start + s.tile_size, y),
                                (s.screen_size.x - s.tile_size + s.borders_width - 1, y))

    def draw_grid(s):
        """ Draws a grid on the whole screen, for debugging purposes """
        for y in range(0, s.screen_size.y, s.tile_size):
            pygame.draw.line(s.display, WHITE, (0, y), (s.screen_size.x, y), 1)
        for x in range(0, s.screen_size.x, s.tile_size):
            pygame.draw.line(s.display, WHITE, (x, 0), (x, s.screen_size.y), 1)

    def get_inputs(s):
        """ Convert PyGame inputs into the formatted ones """
        for event in pygame.event.get():
            if event.type == QUIT:
                return ['EXIT']
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            return ['EXIT']
        # Actual inputs
        res = []
        if keys[K_LEFT] or keys[K_q]: res.append('LEFT')
        if keys[K_RIGHT] or keys[K_d]: res.append('RIGHT')
        if keys[K_UP] or keys[K_z]: res.append('UP')
        if keys[K_DOWN] or keys[K_s]: res.append('DOWN')
        return res

    def load_available_images(s, delta):
        """ Load the master image with all the sprites, and extract each small one,
        create its rotated versions if specified """
        master_img = pygame.image.load(f'Displayer/images/{delta}px.png')
        # For each image family (type) defined in config
        for y_idx, image_item in enumerate(IMAGES.items()):
            tmp_type_images = []
            # For each item of a specific family
            for x_idx in range(image_item[1][0]):
                # Load the item from the master image (which contains all the sprites)
                subsurface = master_img.subsurface((x_idx * delta, y_idx * delta, delta, delta))
                # Scale it to the tile size
                subsurface = pygame.transform.scale(subsurface, (s.tile_size, s.tile_size))
                # Transform it to a pygame friendly format (quicker drawing)
                subsurface.convert()
                tmp_type_images.append(subsurface)
            # If rotation is activated for this family of sprites, create and load
            # all rotated versions
            if image_item[1][1]:
                rotations = []
                for image in tmp_type_images:
                    for angle in [90, 180, 270]:
                        rotations.append(pygame.transform.rotate(image, angle))
                tmp_type_images += rotations
                image_item[1][0] *= 4
            s.images[image_item[0]] = tmp_type_images

    def handle_sleep(s):
        """ Maintains the framerate """
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            pygame.time.wait(int(to_sleep * 1000))
        else:
            print(f"Lagging {-to_sleep} seconds behind")
        s.frame_start = time.time()
