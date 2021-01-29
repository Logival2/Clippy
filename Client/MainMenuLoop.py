from pprint import pprint
import time

import pygame
import pygame_menu

from config import *
from utils import is_valid_ipv4_address, get_random_words


class MainMenuLoop(object):
    def __init__(s, win_size, client):
        s.client = client
        s.is_active = True
        s.win_size = win_size
        s.custom_theme = pygame_menu.themes.Theme(
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
        s.m = pygame_menu.Menu(
            *win_size.get_xy()[::-1],
            'Clippy -',
            theme=s.custom_theme,
        )
        s.m.add_label("Player name:", font_color=GREEN)
        s.m.add_text_input('', default=get_random_words(2))
        s.m.add_vertical_margin(40)
        s.m.add_label("Server:", font_color=GREEN)
        s.m.add_text_input('', default='127.0.0.1:8080', maxchar=21)
        s.m.add_label("Connection Failed!", font_color=TRANSPARENT)
        s.m.add_label("Invalid IPv4 adress", font_color=TRANSPARENT)
        s.m.add_vertical_margin(10)
        s.m.add_button('JOIN', s.join)
        s.m.add_button('QUIT', pygame_menu.events.EXIT)

        s.BGPos = 0
        s.BGStarsPos = 0
        s.sprites = {
            'space': s.load_sprite('./assets/menu/space.png'),
            'stars': s.load_sprite('./assets/menu/stars.png'),
        }
        s.font = pygame.font.Font('./assets/fonts/Everson_Mono.ttf', 110)
        s.rand_text = s.font.render(get_random_words(1), False, BLACK)

    def join(s):
        s.m._widgets[-4]._font_color = TRANSPARENT
        # Attempt connection here
        host = is_valid_ipv4_address(s.m._widgets[4]._get_input_string())
        if not host:
            s.m._widgets[-4]._font_color = RED
            s.m._widgets[-5]._font_color = RED
            return
        if s.connect(*host, s.m._widgets[1]._get_input_string()):
            s.is_active = False
        else:  # Connection failed
            s.m._widgets[-5]._font_color = RED

    def connect(s, ip, port, player_name):
        print(f'Connecting to {ip}:{port}...')
        s.client.connect_in_thread(hostname=ip, port=port)
        s.client.dispatch_event("JOIN", player_name)
        start_time = time.time()
        while time.time() - start_time < 5 and s.client.player_id is None:
            time.sleep(0.1)
        if s.client.player_id is None:
            s.client.disconnect()
        print("playerid:", s.client.player_id)
        return s.client.player_id is not None

    def update(s, events, display):
        if not s.is_active:
            return False
        display.fill(BLACK)
        s.handleBG(display)
        if s.m.is_enabled():
            s.m.update(events)
            s.m.draw(display)
            pygame.draw.line(display, WHITE, (0, 70), (s.win_size.x, 70), 1)
        return True

    def load_sprite(s, path):
            sprite = pygame.image.load(path)
            # Transform it to a pygame friendly format for quicker drawing
            sprite.convert()
            return sprite

    def handleBG(s, display):
        display.blit(s.sprites['space'], (s.BGPos, 0))
        s.BGPos -= 2
        if (s.BGPos <= -s.win_size.x):
            s.BGPos = 0

        display.blit(s.sprites['stars'], (s.BGStarsPos, 0))
        s.BGStarsPos -= 1
        if (s.BGStarsPos <= -800):
            s.BGStarsPos = 0

        # Now draw random text at random positions to get a blinking star effect
        display.blit(s.rand_text, (20, s.win_size.y // 5))
        display.blit(s.rand_text, (30, s.win_size.y // 2))
        display.blit(s.rand_text, (s.win_size.x // 1.5 + 60, s.win_size.y // 5))
        display.blit(s.rand_text, (s.win_size.x // 1.5 + 60, s.win_size.y // 2))
