#!/usr/bin/env python3
import logging
from GameEngine.GameServer import ecs
from GameEngine.Components.Keyboard import Keyboard, keyboard_update, move_up
from GameEngine.Components.Position import Position
from GameEngine.Components.Sprite import Sprite
from GameEngine.Systems.Ecosystem import rabbit_update, fox_update

logging.basicConfig()
logging.root.setLevel(logging.INFO)


if __name__ == '__main__':
    entity = 1
    ecs.add_component(entity, Position(10, 10))
    ecs.add_component(entity, Sprite("player", "desert", 0.5))
    ecs.add_component(entity, Keyboard({'Z': move_up}))
    # ecs.add_system(keyboard_update)
    ecs.add_system(rabbit_update)
    ecs.add_system(fox_update)
    ecs.run()
