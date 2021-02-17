#!/usr/bin/env python3
import logging

from GameEngine.Components.Hitbox import Hitbox
from GameEngine.GameServer import ecs
from GameEngine.Components.Keyboard import Keyboard, keyboard_update, move_up, move_left, move_down, move_right
from GameEngine.Components.Position import Position
from GameEngine.Components.Sprite import Sprite
from GameEngine.Systems.Ecosystem import rabbit_update, fox_update
from GameEngine.Systems.Physics import hitbox_update

logging.basicConfig()
logging.root.setLevel(logging.INFO)


if __name__ == '__main__':
    entity = 1
    ecs.add_component(entity, Position(10, 10))
    ecs.add_component(entity, Sprite("player", "desert", 0.5))
    ecs.add_component(entity, Keyboard({'UP': {"status": False, "function": move_up}, 'LEFT': {"status": False, "function": move_left}, 'DOWN': {"status": False, "function": move_down}, 'RIGHT': {"status": False, "function": move_right}}))
    ecs.add_component(entity, Hitbox(10, 10))
    ecs.add_system(rabbit_update)
    ecs.add_system(fox_update)
    ecs.add_system(keyboard_update)
    ecs.add_system(hitbox_update)
    ecs.run()
