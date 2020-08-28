from CliHandler import FramerateHandler, get_terminal_size
from GameHandler import GameHandler


if __name__ == '__main__':
    framerate_handler = FramerateHandler.FramerateHandler(fps=60)
    gameHandler = GameHandler("test")
    while 42:
        framerate_handler.start_frame()
        gameHandler.do_turn()
        framerate_handler.end_frame()
