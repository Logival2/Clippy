import time
import queue
import threading

from MapHandler import MapHandler
from utils import Pos, getch
from CliHandler import FramerateHandler, TermLayout, Displayer
from Entities import *


class GameHandler(object):
    def __init__(s):
        s.map_handler = MapHandler()
        # Keyboard inputs related
        s.inputs_queue = queue.Queue()
        s.inputs_thread = threading.Thread(
                                        target=getch,
                                        args=(s.inputs_queue, ),
                                        daemon = True)
        s.inputs_thread.start()
        # Display related
        s.framerate_handler = FramerateHandler.FramerateHandler(fps=20)
        s.term_layout = TermLayout.TermLayout(
                            s.map_handler.get_raw_sizes(),
                            info_column_width=35)
        # Game related
        s.score = 0
        s.start_time = time.time()

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
            s.handle_ia()
            Displayer.display_map(s.map_handler, s.term_layout)
            s.draw_hud()
            s.framerate_handler.end_frame()

    def handle_ia(s):
        return

    def draw_hud(s):
        center_space = s.term_layout.info_column_width - 2

        print(f"\033[{1};{s.term_layout.info_column_pos}H╦{'═'*center_space}╗")
        for i in range(2, s.term_layout.end_y_idx):
            print(f"\033[{i};{s.term_layout.info_column_pos}H║{' '*center_space}║")

        print(f"\033[{2};{s.term_layout.info_column_pos + 2}HScore: {s.score}")
        print(f"\033[{3};{s.term_layout.info_column_pos}H╟{'─'*center_space}╢")
        print(f"\033[{4};{s.term_layout.info_column_pos + 2}HTime: {int(time.time() - s.start_time)}")

        # Debug
        # print(f"\033[{6};{s.term_layout.info_column_pos + 2}H{isinstance(s.map_handler.map[0][0].top_ent, Entity)}")

        print(f"\033[{s.term_layout.end_y_idx};{s.term_layout.info_column_pos}H╩{'═'*center_space}╝")
        # Reset cursor
        # print(f"\033[{s.term_layout.term_size.y - 1};1H")  # Reset cursor

    def handle_inputs(s, inputs):
        for last_input in inputs[-2:]:
            if not last_input in ['z', 'q', 's', 'd']: continue
            delta = None
            if last_input == 'z':   delta = Pos(-1, 0)
            elif last_input == 's': delta = Pos(1, 0)
            if last_input == 'q':   delta = Pos(0, -1)
            elif last_input == 'd': delta = Pos(0, 1)
            if delta and s.map_handler.move_entity_relative(s.map_handler.player_pos, delta):
                s.map_handler.player_pos += delta
