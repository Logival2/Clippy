import os
import shlex
import struct
import platform
import subprocess

from utils import Pos


class TermLayout(object):
    def __init__(s, raw_map_size, info_column_width):
        s.info_column_width = info_column_width
        s.raw_map_size = raw_map_size
        s.term_size = None
        s.info_column_pos = 0
        s.end_y_idx = 0
        s.update_term_size()
        s.compute_layout()

    def update_term_size(s):
        s.term_size = Pos(*get_terminal_size())

    def compute_layout(s):
        x_available_space = s.term_size.x - (s.raw_map_size.x * 2)
        s.info_column_pos = s.term_size.x - (s.info_column_width)
        s.end_y_idx = s.term_size.y - 3


def get_terminal_size():
    tmp_term_size = get_terminal_size_raw()
    return tmp_term_size[1], tmp_term_size[0]


def get_terminal_size_raw():
    """ get width and height of console, works on linux,os x, windows, cygwin"""
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # Needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print("Fallback on default terminal size")
        tuple_xy = (80, 25)  # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10, stdout handle is -11, stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])
