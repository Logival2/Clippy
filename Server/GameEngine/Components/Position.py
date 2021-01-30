import umsgpack
import struct


@umsgpack.ext_serializable(0x1)
class Position(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.y + other.y, self.x + other.x)
        return Position(self.y + other, self.x + other)

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.y - other.y, self.x - other.x)
        return Position(self.y + other, self.x + other)

    def __floordiv__(self, factor):
        return Position(self.y // factor, self.x // factor)

    def __truediv__(self, factor):
        return Position(self.y / factor, self.x / factor)

    def __str__(self):
        return f"({self.y}, {self.x})"

    def __repr__(self):
        return f"Position(y={self.y}, x={self.x}"

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __gt__(self, other):
        return self.y > other.y or self.x > other.x

    def __lt__(self, other):
        return self.y < other.y or self.x < other.x

    def __mul__(self, other):
        if isinstance(other, Position):
            return Position(self.y * other.y, self.x * other.x)
        return Position(self.y * other, self.x * other)

    def get_xy(self):
        return (self.x, self.y)

    def __hash__(self):
        # WARNING, THE HASH SHOULD NEVER CHANGE DURING LIFETIME ###
        return hash(f"{self.y}|{self.x}")

    def packb(self):
        return struct.pack(">ii", self.y, self.x)

    @staticmethod
    def unpackb(data):
        return Position(*struct.unpack(">ii", data))
