from pprint import pprint
import time

import pygame
import pygame_menu

from config import *
from utils import is_valid_ipv4_address


class MainMenuLoop(object):
    def __init__(s, win_size, client):
        s.client = client
        s.is_active = True
        s.win_size = win_size
        s.custom_theme = pygame_menu.themes.Theme(
            background_color=BLACK,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,

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
            'Clippy',
            theme=s.custom_theme
        )
        s.m.add_label("Player name:")
        s.m._widgets[-1]._font_color = GREEN
        s.m.add_text_input('', default='Player 1')
        s.m.add_vertical_margin(40)
        s.m.add_label("Server:")
        s.m._widgets[-1]._font_color = GREEN
        s.m.add_text_input('', default='127.0.0.1:1337', maxchar=16)
        s.m.add_label("Connection Failed!")
        s.m._widgets[-1]._font_color = BLACK
        s.m.add_label("Invalid IPv4 adress")
        s.m._widgets[-1]._font_color = BLACK
        s.m.add_vertical_margin(10)
        s.m.add_button('JOIN', s.join)
        s.m.add_button('QUIT', pygame_menu.events.EXIT)

    def join(s):
        s.m._widgets[-4]._font_color = BLACK
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

    def update(s, events, surface):
        if not s.is_active:
            return False
        if s.m.is_enabled():
            s.m.update(events)
            s.m.draw(surface)
            pygame.draw.line(surface, WHITE, (0, 70), (s.win_size.x, 70), 1)
        return True
