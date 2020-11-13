from GameEngine.Ecs import ecs


class Keyboard(object):
    def __init__(s, keys=None):
        if keys is None:
            keys = {}
        s.keys = keys


def keyboard_update():
    keyboards = ecs.get_component(Keyboard)
    for keyboard in keyboards:
        for k, v in keyboard['component'].keys.items():
            if v["function"]:
                v["function"](v["status"])
