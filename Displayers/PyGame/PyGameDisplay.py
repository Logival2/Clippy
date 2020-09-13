import time
from os import listdir
from os.path import isfile, join

import pygame
# import pygame.freetype
from pygame.locals import *

from utils import Pos
from Displayers.PyGame.pygame_defines import *


class PyGameDisplay(object):
    def __init__(s, fps=20, target_resolution=None, hud_width=10):
        ### Pygame related ###
        pygame.init()
        s.square_size = 26  # Should be even
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
        pygame.display.set_caption('Name')
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
        s.draw_map(map_handler)
        s.draw_grid()
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

        final_player_pos = Pos(
                            term_y_idx + map_handler.player_pos.y - map_y_idx,
                            shift_x + (map_handler.player_pos.x - map_x_start) * 2
                        )
        while term_y_idx < s.map_squares_nbr.y:
            term_y_idx += 1
            try:
                tmp_line = map_handler.map[map_y_idx][map_x_start:map_x_end]
            except IndexError:
                break
            for x_idx, square in enumerate(tmp_line):
                if square:
                    types = square.get_types()
                    s.display_entity(types, Pos(x=shift_x + x_idx, y=term_y_idx))
            map_y_idx += 1

    def display_entity(s, ent_types, pos):
        # First, draw lower entity
        if ent_types[1]:
            if ent_types[1] not in s.images.keys():
                name = 'fallback'
            else:
                name = ent_types[1]
            s.display.blit(
                        s.images[name],
                        s.get_square_px_pos(pos).get_tuple()
                    )
        # Now draw top entity
        if ent_types[0]:
            if ent_types[0] not in s.images.keys():
                name = 'fallback'
            else:
                name = ent_types[0]
            s.display.blit(
                        s.images[name],
                        s.get_square_px_pos(pos).get_tuple()
                    )

    def draw_hud(s, info_list):
        pass

    def draw_borders(s):
        # Top border
        for y in range(0, s.square_size):
            pygame.draw.line(s.display, WHITE, (0, y), (s.screen_size.x, y))
        # Bottom border
        for y in range(s.screen_size.y - s.square_size, s.screen_size.y):
            pygame.draw.line(s.display, WHITE, (0, y), (s.screen_size.x, y))
        # Left border
        for x in range(0, s.square_size):
            pygame.draw.line(s.display, WHITE, (x, 0), (x, s.screen_size.y))
        # Right border
        for x in range(s.screen_size.x - s.square_size, s.screen_size.x):
            pygame.draw.line(s.display, WHITE, (x, 0), (x, s.screen_size.y))
        hud_x_start = (1 + s.map_squares_nbr.x) * s.square_size
        # HUD border
        for x in range(hud_x_start, hud_x_start + s.square_size):
            pygame.draw.line(s.display, WHITE, (x, 0), (x, s.screen_size.y))
        # TEXT TEST
        # text_surface = s.font.render('mega', False, RED)
        # s.display.blit(text_surface, (50, 50))

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
        images_dir_path = 'Displayers/PyGame/images/'
        images_names_list = [f[:f.find('.')] for f in listdir(images_dir_path) if isfile(join(images_dir_path, f))]
        print(f"[+] Loading textures: {', '.join(images_names_list)}")
        for image_name in images_names_list:
            tmp_img = pygame.image.load(f'Displayers/PyGame/images/{image_name}.png')
            tmp_img = pygame.transform.scale(tmp_img, (s.square_size, s.square_size))
            s.images[image_name] = tmp_img

    def handle_sleep(s):
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            pygame.time.wait(int(to_sleep * 1000))
        else:
            print(f"Lagging {-to_sleep} seconds behind")
        s.frame_start = time.time()
