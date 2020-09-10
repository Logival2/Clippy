import curses

from GameHandler import GameHandler


def main(stdscr=None):
    gameHandler = GameHandler(stdscr)  # Map name
    gameHandler.launch()


# if __name__ == '__main__':
    # main()
curses.wrapper(main)
