import time

import pygame
# import pygame.freetype
from pygame.locals import *

from utils import Pos
from Displayers.PyGame.pygame_defines import *


class PyGameDisplay(object):
    def __init__(s, fps=20, hud_width=20):
        ### Pygame related ###
        pygame.init()
        s.screen_size = pygame.display.Info()
        s.screen_size = Pos(x=1920, y=1080)
        # s.screen_size = Pos(s.screen_size.current_h, s.screen_size.current_w)
        s.square_size = 16  # Must be even
        s.squares_nbr = s.screen_size // s.square_size
        # print(s.squares_nbr)
        s.hud_squares_nbr = hud_width
        s.map_squares_nbr = Pos(x=s.squares_nbr.x - 3 - s.hud_squares_nbr, y=s.squares_nbr.y - 2)
        # ((0,0),pygame.FULLSCREEN)
        s.display = pygame.display.set_mode((s.screen_size.x , s.screen_size.y))
        pygame.display.set_caption('Name')
        ### FPS related ###
        s.delta = 1 / fps
        s.frame_start = time.time()
        ### Assets ###
        # Main font
        s.main_font = pygame.font.Font('Displayers/PyGame/fonts/CozetteVector.ttf', 32)
        # Resize unicode font till it fits into a single square
        font_start_size = 22
        s.font = pygame.font.Font('Displayers/PyGame/fonts/Everson_Mono.ttf', font_start_size)
        # x, y = s.font.size('x')
        # while x > s.square_size or y > s.square_size:
        #     s.font = pygame.font.Font('Displayers/PyGame/fonts/Everson_Mono.ttf', font_start_size)
        #     x, y = s.font.size('x')
        #     font_start_size -= 1
        print(font_start_size)

        s.images = {}
        s.load_sprite('player')
        s.load_sprite('floor')
        s.load_sprite('grass')

    def __del__(s):
        pygame.quit()

    def draw(s, map_handler, info_list):
        s.display.fill(BLACK)
        s.draw_borders()
        s.draw_map(map_handler)
        # s.draw_grid()
        pygame.display.update()
        s.handle_sleep()

    def draw_map(s, map_handler):
        # Nbr of lines available from the player (-1) to the top of the map screen
        needed_lines_top = s.map_squares_nbr.y // 2
        to_add_top = needed_lines_top - map_handler.player_pos.y
        term_y_idx = 0 if to_add_top <= 0 else to_add_top
        map_y_idx = 0 if to_add_top >= 0 else -to_add_top

        needed_squares_left = s.map_squares_nbr.x // 2
        squares_to_add_left = needed_squares_left - map_handler.player_pos.x
        shift_x = 0 if squares_to_add_left <= 0 else squares_to_add_left
        map_x_start = 0 if squares_to_add_left >= 0 else -squares_to_add_left

        avail_squares_right = s.map_squares_nbr.x // 2 + 2
        map_x_end = map_handler.player_pos.x + avail_squares_right

        final_player_pos = Pos(
                            term_y_idx + map_handler.player_pos.y - map_y_idx,
                            shift_x + (map_handler.player_pos.x - map_x_start) * 2
                        )

        while term_y_idx < s.map_squares_nbr.y + 1:
            try:
                tmp_line = map_handler.map[map_y_idx][map_x_start:map_x_end]
            except IndexError:
                break
            for x_idx, square in enumerate(tmp_line):
                if square:
                    char = square.get_char()
                    name = 'floor'
                    color = WHITE
                    if char == '⧱ ':
                        color = GREEN
                        name = 'player'
                    elif char == 'w':
                        name = 'wall'
                    text_surface = s.font.render(char[1], False, color)
                    s.display.blit(text_surface, s.get_square_px_pos(Pos(x=shift_x + x_idx, y=term_y_idx)).get_tuple())
                    # s.display.blit(
                    #             s.images[name],
                    #             s.get_square_px_pos(Pos(x=shift_x + x_idx, y=term_y_idx)).get_tuple()
                    #         )
            term_y_idx += 1
            map_y_idx += 1

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

    def load_sprite(s, name):
        s.images[name] = pygame.image.load(f'Displayers/PyGame/images/{name}.png')

    def handle_sleep(s):
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            pygame.time.wait(int(to_sleep * 1000))
        else:
            print(f"Lagging {-to_sleep} seconds behind")
        s.frame_start = time.time()
