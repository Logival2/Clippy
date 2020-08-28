from Map import Map
from CliHandler import get_terminal_size, inputs_handler, framerate_handler


if __name__ == '__main__':
    map = Map("test")
    framerate_handler = framerate_handler.Framerate_handler(fps=60)
    while 42:
        if not framerate_handler.do_turn(): continue
        input = inputs_handler.getch()
        map.refresh_display()
