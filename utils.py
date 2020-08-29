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
    def __init__(s, map_max_width, info_column_width):
        s.info_column_width = info_column_width
        s.map_max_width = map_max_width
        s.term_size = None
        s.update_term_size()
        s.compute_layout()

    def update_term_size(s):
        s.term_size = Pos(*get_terminal_size.get_terminal_size())
        empty = s.term_size.x - s.info_column_width
        print(f"term size = {s.term_size}")

    def get_info_column_pos(s):
        return

    def compute_layout(s):
        available_space = s.term_size.x
        min_width = s.map_max_width + 3 + s.info_column_width


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
