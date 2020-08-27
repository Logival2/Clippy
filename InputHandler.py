import sys

import tty
import termios


class _Getch(object):
    def __call__(s):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def getch():
    valid_inputs = ['\r', 'z', 'd', 's', 'q', '\033']
    inkey = _Getch()
    while (1):
        k = inkey()
        if k in valid_inputs: break
        else: print("Invalid Input")
    if k == '\033':
        print("Bye! :)")
        exit()
    return k
