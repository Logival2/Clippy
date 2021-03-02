import umsgpack
import struct


# @umsgpack.ext_serializable(0x1)
from GameEngine.Components.Hitbox import Hitbox


class Position(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __add__(self, other):
        if isinstance(other, Position) or isinstance(other, Hitbox):
            return Position(self.y + other.y, self.x + other.x)
        return Position(self.y + other, self.x + other)

    def __sub__(self, other):
        if isinstance(other, Position) or isinstance(other, Hitbox):
            return Position(self.y - other.y, self.x - other.x)
        return Position(self.y + other, self.x + other)

    def __floordiv__(self, factor):
        return Position(self.y // factor, self.x // factor)

    def __truediv__(self, factor):
        return Position(self.y / factor, self.x / factor)

    def __str__(self):
        return f"({self.y}, {self.x})"

    def __repr__(self):
        return f"Position(y={self.y}, x={self.x})"

    def __eq__(self, other):
        if isinstance(other, Position) or isinstance(other, Hitbox):
            return self.y == other.y and self.x == other.x
        return (self.y, self.x) == other

## Normal comparison operators (>, <) are used to check if AT LEAST one value is (>, <)
# to the other instance
    def __gt__(self, other):
        return self.y > other.y or self.x > other.x

    def __lt__(self, other):
        return self.y < other.y or self.x < other.x

## BITWISE operators (>>, <<) are used to check if ALL values are (>=, <=)
# to the other instance
    def __rshift__(self, other):
        return self.y >= other.y and self.x >= other.x

    def __lshift__(self, other):
        return self.y <= other.y and self.x <= other.x

    def __mul__(self, other):
        if isinstance(other, Position) or isinstance(other, Hitbox):
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
