import time
from os import listdir
from os.path import isfile, join
# from ctypes import *

import pygame
from pygame.locals import *

from utils import Pos
from Displayers.PyGame.pygame_defines import *


class PyGameDisplay(object):
    def __init__(s, fps=20, target_resolution=None, hud_width=10, seed=0):
        ### Pygame related ###
        pygame.init()
        # Square size should be even
        s.square_size = 24
        # Ensure that the final resolution makes for an even square_nbr, based on
        # the square size (in px)
        if target_resolution:
            tmp_screen_size = target_resolution
        else:
            tmp_screen_size = pygame.display.Info()
            tmp_screen_size = Pos(x=tmp_screen_size.current_w, y=tmp_screen_size.current_h)
        s.squares_nbr =  tmp_screen_size // s.square_size
        if s.squares_nbr.x % 2:
            s.squares_nbr.x -=1
        if s.squares_nbr.y % 2:
            s.squares_nbr.y -=1
        s.screen_size = s.squares_nbr * s.square_size
        s.hud_squares_nbr = hud_width
        s.map_squares_nbr = Pos(x=s.squares_nbr.x - 3 - s.hud_squares_nbr, y=s.squares_nbr.y - 2)
        s.display = pygame.display.set_mode((s.screen_size.x , s.screen_size.y))
        pygame.display.set_caption('Clippy')
        ### FPS related ###
        s.delta = 1 / fps
        s.frame_start = time.time()
        ### FONTS ###
        s.main_font = pygame.font.Font('Displayers/PyGame/fonts/CozetteVector.ttf', 32)
        ### IMAGES ###
        s.images = {}
        s.load_available_images()

    def __del__(s):
        pygame.quit()

    def draw(s, map_handler, info_list):
        s.display.fill(BLACK)
        s.draw_borders()
        # s.draw_hud(info_list)
        s.draw_map(map_handler)
        # s.draw_grid()  # Useful for debugging
        pygame.display.update()
        s.handle_sleep()

    def draw_map(s, map_handler):
        # Nbr of lines available from the player (-1) to the top of the map screen
        needed_lines_top = s.map_squares_nbr.y // 2 + 2
        to_add_top = needed_lines_top - map_handler.player_pos.y
        term_y_idx = 0 if to_add_top <= 0 else to_add_top
        map_y_idx = 0 if to_add_top >= 0 else -to_add_top

        needed_squares_left = s.map_squares_nbr.x // 2
        squares_to_add_left = needed_squares_left - map_handler.player_pos.x
        shift_x = 0 if squares_to_add_left <= 0 else squares_to_add_left
        map_x_start = 0 if squares_to_add_left >= 0 else -squares_to_add_left
        shift_x += 1
        avail_squares_right = s.map_squares_nbr.x // 2 + 1
        map_x_end = map_handler.player_pos.x + avail_squares_right

        while term_y_idx < s.map_squares_nbr.y and map_y_idx < len(map_handler.map):
            term_y_idx += 1
            tmp_line = map_handler.map[map_y_idx][map_x_start:map_x_end]
            for x_idx, square in enumerate(tmp_line):
                if square:
                    types = square.get_types()
                    noise_value = square.noise_value
                    s.display_entities(types, Pos(x=shift_x + x_idx, y=term_y_idx), noise_value)
            map_y_idx += 1

    def display_entities(s, ent_types, pos, noise_value):
        # Draw low entity first
        if ent_types[1]:
            s.display_entity(ent_types[1], pos, noise_value)
        if ent_types[0]:
            s.display_entity(ent_types[0], pos, noise_value)

    def display_entity(s, ent_type, pos, noise_value):
        if ent_type not in s.images.keys():
            name = 'fallback'
            img_idx = 0
        else:
            name = ent_type
            img_idx = int(noise_value * IMAGES[name])
        s.display.blit(
                    s.images[name][img_idx],
                    s.get_square_px_pos(pos).get_tuple())

    def draw_hud(s, info_list):
        text_surface = s.main_font.render('mega', False, RED)
        s.display.blit(text_surface, (s.square_size * 2, s.square_size * 2))

    def draw_borders(s):
        border_width = 4
        # Top border
        for y in range(s.square_size - border_width, s.square_size):
            pygame.draw.line(s.display, WHITE,
                                (s.square_size - border_width, y),
                                (s.screen_size.x - s.square_size + border_width, y))
        # Bottom border
        for y in range(s.screen_size.y - s.square_size, s.screen_size.y - s.square_size + border_width):
            pygame.draw.line(s.display, WHITE,
                                (s.square_size - border_width, y),
                                (s.screen_size.x - s.square_size + border_width, y))
        # Left border
        for x in range(s.square_size - border_width, s.square_size):
            pygame.draw.line(s.display, WHITE,
                                (x, s.square_size),
                                (x, s.screen_size.y - s.square_size))
        # Right border
        for x in range(s.screen_size.x - s.square_size, s.screen_size.x - s.square_size + border_width + 1):
            pygame.draw.line(s.display, WHITE,
                                (x, s.square_size),
                                (x, s.screen_size.y - s.square_size))
        hud_x_start = (1 + s.map_squares_nbr.x) * s.square_size
        # Right Map border
        for x in range(hud_x_start, hud_x_start + border_width + 1):
            pygame.draw.line(s.display, WHITE,
                                (x, s.square_size),
                                (x, s.screen_size.y - s.square_size))
        # Left HUD border
        for x in range(hud_x_start + s.square_size - border_width, hud_x_start + s.square_size + 1):
            pygame.draw.line(s.display, WHITE,
                                (x, s.square_size),
                                (x, s.screen_size.y - s.square_size))

    def draw_grid(s):
        for y in range(0, s.screen_size.y, s.square_size):
            pygame.draw.line(s.display, WHITE, (0, y), (s.screen_size.x, y), 1)
        for x in range(0, s.screen_size.x, s.square_size):
            pygame.draw.line(s.display, WHITE, (x, 0), (x, s.screen_size.y), 1)

    def draw_square(s, pos):
        # Check square filling
        pos = s.get_square_px_pos(Pos(x=pos.x, y=pos.y))
        for y in range(pos.y, pos.y + s.square_size):
            for x in range(pos.x, pos.x + s.square_size):
                s.display.set_at((x, y), RED)

    def get_square_px_pos(s, pos):
        return pos * s.square_size

    def get_inputs(s):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'EXIT'
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            return 'EXIT'
        # Actual inputs
        if keys[K_LEFT] or keys[K_q]:
            return 'LEFT'
        if keys[K_RIGHT] or keys[K_d]:
            return 'RIGHT'
        if keys[K_UP] or keys[K_z]:
            return 'UP'
        if keys[K_DOWN] or keys[K_s]:
            return 'DOWN'

    def load_available_images(s):
        name = '8'
        delta = int(name)
        master_img = pygame.image.load(f'Displayers/PyGame/images/{name}px.png')
        for y_idx, image_item in enumerate(IMAGES.items()):
            tmp_type_images = []
            for x_idx in range(image_item[1]):
                subsurface = master_img.subsurface((x_idx * delta, y_idx * delta, delta, delta))
                subsurface = pygame.transform.scale(subsurface, (s.square_size, s.square_size))
                subsurface.convert()
                tmp_type_images.append(subsurface)
            s.images[image_item[0]] = tmp_type_images

    def handle_sleep(s):
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            pygame.time.wait(int(to_sleep * 1000))
        else:
            print(f"Lagging {-to_sleep} seconds behind")
        s.frame_start = time.time()
