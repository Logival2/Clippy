import time
import copy
import queue
import threading

from CliHandler.get_terminal_size import get_terminal_size
from utils import Pos, getch, exit_error


class CliHandler(object):
    def __init__(s, fps=20, info_column_width=35):
        # FPS related
        s.delta = 1 / fps
        s.frame_start = time.time()
        # Display related
        s.term_size = Pos(*get_terminal_size())
        if s.term_size.y < 15 or s.term_size.x < 70:
            exit_error("Display error: Terminal is too small (min 15H x 70W)")
        s.info_column_width = info_column_width
        s.info_column_x_pos = s.term_size.x - s.info_column_width
        s.empty_term_repr = []
        s.term_repr = []
        s.end_y_idx = s.term_size.y - 3
        
        s.t_map_available_space = Pos(s.end_y_idx - 2, s.info_column_x_pos - 3)
        s.t_map_center = s.t_map_available_space // 2
        s.t_map_center += Pos(1, 2)
        s.init_map_repr()
        # Keyboard inputs related
        s.inputs_queue = queue.Queue()
        s.inputs_thread = threading.Thread(
                                        target=getch,
                                        args=(s.inputs_queue, ),
                                        daemon = True)
        s.inputs_thread.start()

    def draw(s, map_handler, info_list):
        s.term_repr = copy.copy(s.empty_term_repr)
        s.copy_hud_to_buffer(info_list)
        s.copy_map_to_buffer(map_handler)
        print(f"\033[1;0H{''.join(s.term_repr)}", end= '', flush=True)
        s.handle_sleep()

    def copy_map_to_buffer(s, map_handler):
        needed_lines_top = (s.t_map_available_space.y - 1) // 2  # nbr lignes dispo
        to_add_top = needed_lines_top - (map_handler.player_pos.y + 1) + 1
        shift_y = 0 if to_add_top < 0 else to_add_top
        map_y_idx = 0 if to_add_top >= 0 else -to_add_top

        needed_squares_left = ((s.t_map_available_space.x - 2) // 2) // 2  # nbr lignes dispo
        avail_square_left = (map_handler.player_pos.x + 1)
        squares_to_add_left = needed_squares_left - avail_square_left
        shift_x = 0 if squares_to_add_left < 0 else squares_to_add_left
        shift_x *= 2  # Square to char
        shift_x += 3  # Borders
        map_x_start = 0 if squares_to_add_left >= 0 else -squares_to_add_left

        avail_squares_right = ((s.t_map_available_space.x + 2) // 2) // 2
        map_x_end = map_handler.player_pos.x + avail_squares_right + 1


        for y_idx in range(shift_y + 1, s.end_y_idx):
            try:
                line = map_handler.map[map_y_idx][map_x_start:map_x_end]
            except IndexError:
                break
            buf = ""
            for entity in line:
                if entity:
                    repr = entity.__repr__()
                    buf += repr
                else:
                    buf += "  "
            s.n_fill_line(y_idx, shift_x, buf, len(line) * 2 + shift_x) # En attendant pour pas que ca depasse a droite
            map_y_idx += 1

    def copy_hud_to_buffer(s, info_list):
        y_idx = 0
        center_space = s.info_column_width - 2
        for key, value in info_list.items():
            y_idx += 1
            if key == "separator":
                s.fill_line(y_idx, s.info_column_x_pos - 1, f"╟{'─'*center_space}╢")
            elif key == "empty":
                continue
            else:
                final_str = f" {key}: {value}" if value != None else f" {key}"
                padding = center_space - len(final_str)
                s.fill_line(y_idx, s.info_column_x_pos, final_str)

    def fill_line(s, y_idx, x_start_idx, new_data):
        if len(new_data) + x_start_idx > len(s.term_repr[0]):
            exit_error("T'a CHIEEE 1")
        final_line = s.term_repr[y_idx][:x_start_idx]
        final_line += new_data
        final_line += s.term_repr[y_idx][len(final_line):]
        s.term_repr[y_idx] = final_line

    def n_fill_line(s, y_idx, x_start_idx, new_data, new_data_len):
        final_line = s.term_repr[y_idx][:x_start_idx]
        final_line += new_data
        final_line += s.term_repr[y_idx][new_data_len:]
        s.term_repr[y_idx] = final_line

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

    def init_map_repr(s):
        center_space = s.info_column_width - 2
        # Top border
        s.empty_term_repr.append(f" ╔{'═' * s.t_map_available_space.x}╦{'═' * center_space}╗ ")
        for i in range(1, s.end_y_idx):
            s.empty_term_repr.append(f" ║{' ' * s.t_map_available_space.x}║{' ' * center_space}║ ")
        # Bottom border
        s.empty_term_repr.append(f" ╚{'═' * s.t_map_available_space.x}╩{'═' * center_space}╝ ")
