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

def exit_error(msg):
    print(msg)
    exit()


class Update(object):
    def __init__(s, arg):
        s.arg = arg


def getch(inputs_queue):
    fd = sys.stdin.fileno()
    cli_attr = termios.tcgetattr(fd)
    while 42:
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, cli_attr)
        inputs_queue.put(ch)
        if ch == '\033': return # Escape, stop input reading thread
