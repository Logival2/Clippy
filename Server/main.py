#!/usr/bin/env python3
import logging
from GameEngine.GameServer import ecs
from GameEngine.Components.Fox import fox_update
from GameEngine.Components.Rabbit import rabbit_update

logging.basicConfig()
logging.root.setLevel(logging.INFO)


if __name__ == '__main__':
    ecs.add_system(rabbit_update)
    ecs.add_system(fox_update)
    ecs.run()
