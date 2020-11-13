#!/usr/bin/env python3
import time

import pygame
from pygame.locals import *


class PyGameDisplay(object):
    def __init__(s):
        pygame.init()
        # Launch display, (x, y)
        s.screen_size = (256, 256)
        s.display = pygame.display.set_mode(s.screen_size)
        pygame.display.set_caption('Test network')
        ### FPS related ###
        s.delta = 1 / 2 # 2 FPS
        s.frame_start = time.time()

    def draw(s):
        s.display.fill((0, 0, 0))
        s.draw_grid()  # Useful for debugging
        pygame.display.update()
        s.handle_sleep()

    def draw_grid(s):
        for y in range(0, s.screen_size[1], 16):
            pygame.draw.line(s.display, (236, 240, 241), (0, y), (s.screen_size[0], y), 1)
        for x in range(0, s.screen_size[0], 16):
            pygame.draw.line(s.display, (236, 240, 241), (x, 0), (x, s.screen_size[1]), 1)

    def get_inputs(s):
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

    def handle_sleep(s):
        """ Maintains the framerate """
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            pygame.time.wait(int(to_sleep * 1000))
        else:
            print(f"Lagging {-to_sleep:.2f} seconds behind")
        s.frame_start = time.time()


class GameHandler(object):
    def __init__(s, input_queue, output_queue):
        s.cli_handler = PyGameDisplay()
        ### HUD ###
        s.start_time = time.time()
        s.input_queue = input_queue
        s.output_queue = output_queue
        s.counter = 0
        s.avail_inputs = [
            'UP',
            'DOWN',
            'LEFT',
            'RIGHT',
        ]

    def launch(s):
        while 42:
            print('tour')
            s.handle_inputs()
            while not s.input_queue.empty():
                print('---------')
                print(s.input_queue.get_nowait().decode('utf-8'))
            s.cli_handler.draw()

    def handle_inputs(s):
        """ Exit if needed, otherwise try to execute the first move, if not successful (collision)
        try the next one etc, otherwise return """
        player_inputs = s.cli_handler.get_inputs()
        if not player_inputs: return
        if "EXIT" in player_inputs: exit()  ## networkmanager.stop()
        if 'LEFT' in player_inputs:
            print(f"envoi {s.counter}")
            s.output_queue.put(f"envoi {s.counter}".encode('utf-8'))
            s.counter += 1
