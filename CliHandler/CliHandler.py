import time
import queue
import threading

from CliHandler import get_terminal_size
from utils import Pos, getch


class CliHandler(object):
    def __init__(s, fps=20, info_column_width=35):
        # Keyboard inputs related
        s.inputs_queue = queue.Queue()
        s.inputs_thread = threading.Thread(
                                        target=getch,
                                        args=(s.inputs_queue, ),
                                        daemon = True)
        s.inputs_thread.start()
        # FPS related
        s.delta = 1 / fps
        s.frame_start = time.time()
        # Display related
        s.term_size = Pos(*get_terminal_size.get_terminal_size())
        s.info_column_width = info_column_width
        s.info_column_x_pos = s.term_size.x - (s.info_column_width)
        s.end_y_idx = s.term_size.y - 3

    def draw(s, map_handler, info_list):
        s.draw_map(map_handler)
        s.draw_hud(info_list)
        s.handle_sleep()

    def draw_map(s, map_handler):
        # cropped_map = crop_map(map_handler)
        print(f"\033[K\033[1;2H╔{'═'*(s.info_column_x_pos - 2)}", end='')
        map_end = 0
        for y, l in enumerate(map_handler.map):
                # \033[K erase line, then print
                print(f"\033[K\033[{y + 2};2H║ ", end='')
                for entity in l:
                    if entity:
                        repr = entity.__repr__()
                        print(repr * 2, end='')
                    else:
                        print("  ", end='')
                map_end = y
        for i in range(map_end, s.end_y_idx):
            print(f"\033[K\033[{i};2H║", end='')
        print(f"\033[K\033[{s.end_y_idx};2H╚{'═'*(s.info_column_x_pos - 2)}", end='')

    def draw_hud(s, info_list):
        center_space = s.info_column_width - 2
        # Top line
        print(f"\033[{1};{s.info_column_x_pos}H╦{'═'*center_space}╗")
        line_drawn_count = 2
        for key, value in info_list.items():
            if key == "separator":
                print(f"\033[{line_drawn_count};{s.info_column_x_pos}H╟{'─'*center_space}╢")
            elif key == "empty":
                print(f"\033[{line_drawn_count};{s.info_column_x_pos}H║{' '*center_space}║")
            else:
                final_str = f" {key}: {value}"
                padding = center_space - len(final_str)
                print(f"\033[{line_drawn_count};{s.info_column_x_pos}H║{final_str}{' '*padding}║")
            line_drawn_count += 1
        # Fill empty lines
        for i in range(line_drawn_count, s.end_y_idx):
            print(f"\033[{i};{s.info_column_x_pos}H║{' '*center_space}║")
        # Last line
        print(f"\033[{s.end_y_idx};{s.info_column_x_pos}H╩{'═'*center_space}╝")

    def get_inputs(s):
        inputs = []
        while not s.inputs_queue.empty():
            inputs.append(s.inputs_queue.get_nowait())
        if '\x1b' in inputs: # Escape
            print("See you soon!")
            exit()
        return inputs

    def handle_sleep(s):
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            time.sleep(to_sleep)
        else:
            print(f"Lagging {-to_sleep} seconds behind")
        s.frame_start = time.time()
