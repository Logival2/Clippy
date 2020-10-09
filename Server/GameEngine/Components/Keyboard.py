from GameEngine.Ecs import ecs


class Keyboard(object):
    def __init__(s):
        s.keys = []


def keyboard_update():
    keyboards = ecs.get_component(Keyboard)
    for keyboard in keyboards:
        for key in keyboard.keys:
            if key["function"]:
                key["function"](key["status"])
