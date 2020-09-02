import os
import sys
import tty
import json
import queue
import termios


class Pos(object):
    def __init__(s, y, x):
        s.y = y
        s.x = x

    def __add__(s, other):
        if isinstance(other, Pos):
            return Pos(s.y + other.y, s.x + other.x)
        return Pos(s.y + other, s.x + other)

    def __sub__(s, other):
        return Pos(s.y - other.y, s.x - other.x)

    def __floordiv__(s, factor):
        return Pos(s.y // factor, s.x // factor)

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


def load_theme_file():
    theme_file_path = sys.argv[1] if len(sys.argv) > 1 else "default_theme"
    try:
        with open(f"./maps/{theme_file_path}.json", 'r') as f:
            data = f.read()
    except FileNotFoundError:
        with open(f"./maps/default_theme.json", 'r') as f:
            data = f.read()
    data = json.loads(data)
    if not all(e in data.keys() for e in ['floor', 'enemy', 'player']):
        exit_error("Invalid map file, not enough entities defined")
    return data


def generate_room():
    return
