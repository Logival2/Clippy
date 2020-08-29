import time
import queue
import threading

from MapHandler import MapHandler
from utils import Pos, TermLayout, getch
from CliHandler import FramerateHandler


class GameHandler(object):
    def __init__(s, input):
        # Input can either be a filename or a tuple (map dimensions)
        s.map_handler = MapHandler(input)
        s.framerate_handler = FramerateHandler.FramerateHandler(fps=20)
        # Keyboard inputs related
        s.inputs_queue = queue.Queue()
        s.inputs_thread = threading.Thread(
                                        target=getch,
                                        args=(s.inputs_queue, ),
                                        daemon = True)
        s.inputs_thread.start()
        # Display related
        s.term_layout = TermLayout(
                            s.map_handler.get_max_width(),
                            info_column_width=70)
        # Game related
        s.score = 0
        s.start_time = time.time()
        s.player = s.map_handler.get_player()
        s.draw_hud()

    def launch(s):
        while 42:
            s.framerate_handler.start_frame()
            inputs = []
            while not s.inputs_queue.empty():
                inputs.append(s.inputs_queue.get_nowait())
            if '\x1b' in inputs: # Escape
                print("bye :)")
                exit()
            s.handle_inputs(inputs)
            s.map_handler.full_display()
            s.framerate_handler.end_frame()

    def handle_inputs(s, inputs):
        for last_input in inputs[-3:]:
            if not last_input in ['z', 'q', 's', 'd']: continue
            delta = None
            if last_input == 'z':   delta = Pos(-1, 0)
            elif last_input == 's': delta = Pos(1, 0)
            if last_input == 'q':   delta = Pos(0, -1)
            elif last_input == 'd': delta = Pos(0, 1)
            if delta and s.map_handler.move_entity_relative(s.map_handler.player_pos, delta):
                s.map_handler.player_pos += delta

    def draw_hud(s):
        pass
        # print(f"Win size = {s.term_size}")
                    # print(f"\033[K\033[{y+1};1H")
