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
