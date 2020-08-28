import sys
import termios
import tty

class Pos(object):
    def __init__(s, y, x):
        s.y = y
        s.x = x

    def __add__(s, other):
        return Pos(s.y + other.y, s.x + other.x)

    def __sub__(s, other):
        return Pos(s.y - other.y, s.x - other.x)


def exit_error(msg):
    print(msg)
    exit()


class Update(object):
    def __init__(s, arg):
        s.arg = arg


class Printer(object):
    def __init__(s, fd, cli_attr):
        s.fd = fd
        s.cli_attr = cli_attr

    def safe_print(s, msg):
        termios.tcsetattr(s.fd, termios.TCSADRAIN, s.cli_attr)
        print(msg)
        tty.setraw(s.fd)
