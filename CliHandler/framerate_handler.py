import time


class Framerate_handler(object):
    def __init__(s, fps):
        s.last_update = time.time()
        s.delta = 1 / fps

    def do_turn(s):
        if (time.time() - s.last_update) > s.delta:
            s.last_update = time.time()
            return True
