import sys
import tty
import queue
import termios

from CliHandler import get_terminal_size


class Pos(object):
    def __init__(s, y, x):
        s.y = y
        s.x = x

    def __add__(s, other):
        return Pos(s.y + other.y, s.x + other.x)

    def __repr__(s):
        return f"Pos y={s.y}/x={s.x}"


class Update(object):
    def __init__(s, arg):
        s.arg = arg


class TermLayout(object):
    def __init__(s, raw_map_width, info_column_width):
        s.info_column_width = info_column_width
        s.raw_map_width = raw_map_width
        s.term_size = 0
        s.map_size_factor = 1
        s.info_column_pos = 0
        s.update_term_size()
        s.compute_layout()

    def update_term_size(s):
        s.term_size = Pos(*get_terminal_size.get_terminal_size())

    def compute_layout(s):
        map_available_space = s.term_size.x - (s.info_column_width + 3)
        s.map_size_factor = map_available_space // s.raw_map_width
        s.info_column_pos = s.raw_map_width * s.map_size_factor + 3
        # print(f"{s.term_size.x} / {map_available_space} / {s.map_size_factor} / {s.info_column_pos}")


def getch(inputs_queue):
    """This function is launched in another thread, owned by GameHandler"""
    fd = sys.stdin.fileno()
    cli_attr = termios.tcgetattr(fd)
    while 42:
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, cli_attr)
        inputs_queue.put(ch)
        if ch == '\x1b': return # Escape, stop input reading thread


def exit_error(msg):
    print(msg)
    exit()
