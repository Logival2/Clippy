from pprint import pprint
import time

import pygame
import pygame_menu

from config import *
from utils import is_valid_ipv4_address, get_random_words


class MainMenuLoop(object):
    def __init__(self, win_size, client):
        self.client = client
        self.is_active = True
        self.win_size = win_size
        self.custom_theme = pygame_menu.themes.Theme(
            background_color=TRANSPARENT,

            widget_background_color=BLACK,

            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            title_offset=(12, 6),

            title_font_size=60,
            widget_font_size=40,

            title_font_color= WHITE,
            widget_font_color= WHITE,
            cursor_color= WHITE,
            selection_color= WHITE,
            widget_font=pygame_menu.font.FONT_MUNRO,
            title_font=pygame_menu.font.FONT_MUNRO,
        )
        self.m = pygame_menu.Menu(
            *win_size.get_xy()[::-1],
            'Clippy -',
            theme=self.custom_theme,
        )
        self.m.add_label("Player name:", font_color=GREEN)
        self.m.add_text_input('', default=get_random_words(2))
        self.m.add_vertical_margin(40)
        self.m.add_label("Server:", font_color=GREEN)
        self.m.add_text_input('', default='127.0.0.1:8080', maxchar=21)
        self.m.add_label("Connection Failed!", font_color=TRANSPARENT)
        self.m.add_label("Invalid IPv4 adress", font_color=TRANSPARENT)
        self.m.add_vertical_margin(10)
        self.m.add_button('JOIN', self.join)
        self.m.add_button('QUIT', pygame_menu.events.EXIT)

        self.BGPos = 0
        self.BGStarsPos = 0
        self.sprites = {
            'space': self.load_sprite('./assets/menu/space.png'),
            'stars': self.load_sprite('./assets/menu/stars.png'),
        }
        self.font = pygame.font.Font('./assets/fonts/Everson_Mono.ttf', 110)
        self.rand_text = self.font.render(get_random_words(1), False, BLACK)

    def join(self):
        self.m._widgets[-4]._font_color = TRANSPARENT
        # Attempt connection here
        host = is_valid_ipv4_address(self.m._widgets[4]._get_input_string())
        if not host:
            self.m._widgets[-4]._font_color = RED
            self.m._widgets[-5]._font_color = RED
            return
        if self.connect(*host, self.m._widgets[1]._get_input_string()):
            self.is_active = False
        else:  # Connection failed
            self.m._widgets[-5]._font_color = RED

    def connect(self, ip, port, player_name):
        print(f'Connecting to {ip}:{port}...')
        self.client.connect_in_thread(hostname=ip, port=port)
        self.client.dispatch_event("JOIN", player_name)
        start_time = time.time()
        while time.time() - start_time < 5 and self.client.player_id is None:
            time.sleep(0.1)
        if self.client.player_id is None:
            self.client.disconnect()
        return self.client.player_id is not None

    def update(self, events, display):
        if not self.is_active:
            return False
        display.fill(BLACK)
        self.handleBG(display)
        if self.m.is_enabled():
            self.m.update(events)
            self.m.draw(display)
            pygame.draw.line(display, WHITE, (0, 70), (self.win_size.x, 70), 1)
        return True

    def load_sprite(self, path):
            sprite = pygame.image.load(path)
            # Transform it to a pygame friendly format for quicker drawing
            sprite.convert()
            return sprite

    def handleBG(self, display):
        display.blit(self.sprites['space'], (self.BGPos, 0))
        self.BGPos -= 2
        if (self.BGPos <= -self.win_size.x):
            self.BGPos = 0

        display.blit(self.sprites['stars'], (self.BGStarsPos, 0))
        self.BGStarsPos -= 1
        if (self.BGStarsPos <= -800):
            self.BGStarsPos = 0

        # Now draw random text at random positions to get a blinking star effect
        display.blit(self.rand_text, (20, self.win_size.y // 5))
        display.blit(self.rand_text, (40, self.win_size.y // 2))
        display.blit(self.rand_text, (self.win_size.x // 1.5 + 40, self.win_size.y // 5.3))
        display.blit(self.rand_text, (self.win_size.x // 1.5 + 60, self.win_size.y // 1.9))
