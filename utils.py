import time
import random


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

    def __eq__(s, other):
        return s.y == other.y and s.x == other.x


def exit_error(msg):
    print(msg)
    exit()


def log_to_file(msg):
    with open('./log.txt', 'w') as f:
        f.write(f"{time.time()}:\t{msg}\n")


def get_random_unicode_from_range(ranges_list, length=1):
    """ Receives a list of tuples (list of (range_start, range_end))
    returns {length} chars at random from this range """
    try:
        get_char = unichr
    except NameError:
        get_char = chr
    res = ""
    for i in range(length):
        selected_range = random.choice(ranges_list)
        res += get_char(random.randint(*selected_range))
    return res
