import sys

from GameEngine.Components.Position import Position
from GameEngine.GameServer import ecs


class Keyboard(object):
    def __init__(s, keys={}):
        s.keys = keys


def keyboard_update():
    keyboards = ecs.get_component(Keyboard)
    for k, v in ecs.game_state["players"].items():
        if "inputs" in v and "entity" in v:
            for key in v["inputs"]:
                for kb, vb in keyboards[v["entity"]].keys.items():
                    print(kb, vb)
                    vb["status"] = kb == key
                    if vb["function"]:
                        vb["function"](vb["status"], v["entity"])
    return {}


def move_up(status, entity):
    if status:
        pos = ecs.get_component(Position, entity)
        if ecs.map[pos.y - 1][pos.x][0] not in ["water", "lava"]:
            pos.y -= 1


def move_left(status, entity):
    if status:
        pos = ecs.get_component(Position, entity)
        if ecs.map[pos.y][pos.x - 1][0] not in ["water", "lava"]:
            pos.x -= 1


def move_down(status, entity):
    if status:
        pos = ecs.get_component(Position, entity)
        if ecs.map[pos.y + 1][pos.x][0] not in ["water", "lava"]:
            pos.y += 1


def move_right(status, entity):
    if status:
        pos = ecs.get_component(Position, entity)
        if ecs.map[pos.y][pos.x + 1][0] not in ["water", "lava"]:
            pos.x += 1
