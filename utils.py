import time

class Pos(object):
    def __init__(s, y, x):
        s.y = y
        s.x = x

    def __add__(s, other):
        return Pos(s.y + other.y, s.x + other.x)

    def __sub__(s, other):
        return Pos(s.y - other.y, s.x - other.x)

def exit_error(msg):
    print(msg)
    exit()

class Update(object):
    def __init__(s, arg):
        s.arg = arg

class Framerate_handler(object):
    def __init__(s, fps):
        s.last_update = time.time()
        s.delta = 1 / fps

    def do_turn(s):
        if (time.time() - s.last_update) > s.delta:
            s.last_update = time.time()
            return True
