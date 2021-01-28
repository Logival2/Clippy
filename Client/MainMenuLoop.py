import pygame
import pygame_menu

from config import *


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
        s.main_m = pygame_menu.menu.Menu(
                                    *win_size.get_xy()[::-1],
                                    'Clippy',
                                    theme=s.custom_theme
                                )
        s.main_m.add_text_input('Player name: ', default='Player 1')
        s.main_m.add_vertical_margin(40)
        # s.main_m.add_label("Enter server info")
        s.main_m.add_text_input('Server IP: ', default='0.0.0.0', maxchar=16)
        s.main_m.add_text_input(
            'Server Port: ', default='1337',
            maxchar=4, input_type=pygame_menu.locals.INPUT_INT
        )
        s.main_m.add_vertical_margin(50)
        s.main_m.add_button('JOIN', s.join)
        s.main_m.add_button('QUIT', pygame_menu.events.EXIT)

    def join(s):
        # Attempt connection here
        print("Connecting...")
        # If connection is successful
        if 42:
            s.is_active = False
        else:
            s.main_m.add_label("Connection Failed!", label_id='err_con')


    def update(s, events, surface):
        if not s.is_active:
            return False
        if s.main_m.is_enabled():
            s.main_m.update(events)
            s.main_m.draw(surface)
            for x in range(0, s.win_size.x, 30):
                pygame.draw.line(surface, WHITE, (x, 70), (x + 20, 70), 6)
        return True
