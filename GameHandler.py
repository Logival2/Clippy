import sys
import tty
import queue
import termios
import threading

from Map import Map
from utils import Pos
from CliHandler import FramerateHandler


def getch(fd, cli_attr, inputs_queue):
    while 42:
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, cli_attr)
        inputs_queue.put(ch)
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
        # s.map.full_display()
        # print(f"\033[6;100HPlopinet")
        # print("->", inputs, "\033[K", end="\r", flush=True)

        print("->", inputs, '\r')
        # sys.stdout.flush()
