import sys
import time

from GameEngine.Components.Keyboard import *
from GameEngine.Components.Network import network_update
from GameEngine.Components.Position import Position


if __name__ == '__main__':
    ecs.tick = 144

    ecs.add_update(keyboard_update)
    ecs.add_update(network_update)

    _in = time.time()
    for x in range(-500, 500):
        for y in range(-500, 500):
            ecs.map.get_tile(x, y)
    print(str(time.time() - _in) + " seconds")

    entity = ecs.new_entity()
    ecs.add_component(entity, Keyboard({'KEY_Z': {'function': lambda x: move_up(x, entity), 'status': False}, 'KEY_Q': {'function': lambda x: move_left(x, entity), 'status': False}, 'KEY_S': {'function': lambda x: move_down(x, entity), 'status': False}, 'KEY_D': {'function': lambda x: move_right(x, entity), 'status': False}}))
    ecs.add_component(entity, Position(0, 0))

    ecs.add_update(lambda: print(ecs.get_component(Position, entity).x, ecs.get_component(Position, entity).y))
    while True:
        ecs.update()
