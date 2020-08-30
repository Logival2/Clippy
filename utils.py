import sys
import tty
import queue
import termios


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
