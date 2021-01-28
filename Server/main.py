#!/usr/bin/env python3
import logging
from GameEngine.GameServer import ClippyGame
logging.basicConfig()
logging.root.setLevel(logging.INFO)


def main():
    game = ClippyGame()
    game.run()


if __name__ == '__main__':
    main()
