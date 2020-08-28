from CliHandler import FramerateHandler, get_terminal_size
from GameHandler import GameHandler


if __name__ == '__main__':
    framerate_handler = FramerateHandler.FramerateHandler(fps=2)
    gameHandler = GameHandler("test")
    while 42:
        if not framerate_handler.do_turn(): continue
        gameHandler.do_turn()
        # map.refresh_display()
