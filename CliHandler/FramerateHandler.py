import time


class FramerateHandler(object):
    def __init__(s, fps):
        s.delta = 1 / fps
        s.frame_start = None

    def start_frame(s):
        s.frame_start = time.time()

    def end_frame(s):
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            time.sleep(to_sleep)
        else:
            print(f"Lagging {-to_sleep} seconds behind")
