import sys
import tty
import queue
import termios
import threading

from Map import Map
from utils import Pos


# class _Getch(object):
#     def __call__(s):
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch
#
# def getch():
#     inkey = _Getch()
#     k = inkey()
#     if k == '\033':
#         exit()
#     return k

def getch(fd, old_settings, inputs_queue):
    # inkey = _Getch()
    while 42:
        # ch = inkey()
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # ch = tmp(fd, old_settings)
        inputs_queue.put(ch)
        # sys.stdin.flush()
        if ch == '\033': return # Escape, stop input reading thread

class GameHandler(object):
    def __init__(s, input):
        # Input can either be a filename or a tuple (map dimensions)
        s.map = Map(input)
        s.fd = sys.stdin.fileno()
        s.cli_attr = termios.tcgetattr(s.fd)
        s.inputs_queue = queue.Queue()
        s.inputs_thread = threading.Thread(
                                        target=getch,
                                        args=(s.fd, s.cli_attr, s.inputs_queue))
        s.inputs_thread.start()

    def do_turn(s):
        inputs = []
        while not s.inputs_queue.empty():
            inputs.append(s.inputs_queue.get_nowait())
        if '\033' in inputs: # Escape
            print("bye :)")
            exit()
        print("->", inputs)
