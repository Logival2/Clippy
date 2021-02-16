import sys

from Server.GameEngine.Components.Position import Position
from Server.GameEngine.GameServer import ecs


class Keyboard(object):
    def __init__(s, keys=None):
        if keys is None:
            keys = {}
        s.keys = keys


up = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
down = "abcdefghijklmnopqrstuvwxyz"
def keyboard_update():
    keyboards = ecs.get_component(Keyboard)
    # jej = ecs.game_state["players"][0]["inputs"]
    # if len(ecs.game_state["players"][0]["inputs"]) == 0:
    #     return
    # for keyboard in keyboards:
    #     for k, v in keyboard['component'].keys.items():
    #         v["status"] = k == ecs.game_state["players"][0]["inputs"][0]
    #         if v["function"]:
    #             v["function"](v["status"])


def move_up(status, entity):
    if status:
        ecs.get_component(Position, entity).y -= 1


def move_left(status, entity):
    if status:
        ecs.get_component(Position, entity).x -= 1


def move_down(status, entity):
    if status:
        ecs.get_component(Position, entity).y += 1


def move_right(status, entity):
    if status:
        ecs.get_component(Position, entity).x += 1
