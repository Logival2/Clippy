from pprint import pprint

import pygame
import pygame_menu

from config import *
from utils import is_valid_ipv4_address


class MainMenuLoop(object):
    def __init__(s, win_size):
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
        # pprint(dir(s.m._widgets[4]))

    def join(s):
        s.m._widgets[-4]._font_color = BLACK
        # Attempt connection here
        ip = s.m._widgets[4]._get_input_string()
        if not is_valid_ipv4_address(ip):
            s.m._widgets[-4]._font_color = RED
            s.m._widgets[-5]._font_color = RED
            return
        print("Connecting to", ip)
        if not 42:  # If connection is successful
            s.is_active = False
        else:
            s.m._widgets[-5]._font_color = RED

    def update(s, events, surface):
        if not s.is_active:
            return False
        if s.m.is_enabled():
            s.m.update(events)
            s.m.draw(surface)
            pygame.draw.line(surface, WHITE, (0, 70), (s.win_size.x, 70), 1)
        return True
