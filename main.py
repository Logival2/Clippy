import curses

from GameHandler import GameHandler


def main(stdscr=None):
    gameHandler = GameHandler(stdscr)
    gameHandler.launch()


curses.wrapper(main)
