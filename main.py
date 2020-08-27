from Map import Map
from InputHandler import getch
from utils import Framerate_handler


if __name__ == '__main__':
    map = Map("test")
    framerate_handler = Framerate_handler(fps=60)
    while 1:
        if not framerate_handler.do_turn(): continue
        input = getch()
        map.refresh_display()
