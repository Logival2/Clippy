#!/usr/bin/env python3
import logging
from GameEngine.GameServer import ecs

logging.basicConfig()
logging.root.setLevel(logging.INFO)


if __name__ == '__main__':
    ecs.run()

