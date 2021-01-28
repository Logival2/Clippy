import pygame
import pygame_menu

from MainMenuLoop import MainMenuLoop
from GameLoop import GameLoop
from config import *


class App(object):
    def __init__(s, win_size, max_fps):
        # pygame.init()
        s.max_fps = max_fps

        # s.displayer = Displayer(DISPLAY_CONFIG)
        # s.surface = pygame.display.set_mode(win_size)

        s.game_loop = GameLoop(DISPLAY_CONFIG)
        # Final win size is needed as the window size is changed based on the tile size
        s.main_menu_loop = MainMenuLoop(s.game_loop.screen_size)
        s.active_loop = s.main_menu_loop
        s.clock = pygame.time.Clock()

    def run(s):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if not s.active_loop.update(events, s.game_loop.display):
                s.active_loop = s.game_loop
            pygame.display.update()
            s.clock.tick(s.max_fps)


if __name__ == '__main__':
    app = App((1200, 900), 60)
    app.run()
