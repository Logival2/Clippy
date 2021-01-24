#!/usr/bin/env python3
from Logger import logger


class Seq(int):
    """A sequence number that loops around when reaching max value or below 1"""

    __bytesize: int = 2
    __max_sequence: int = int("1" * (__bytesize * 8), 2)

    @classmethod
    def setByteSize(cls, bytesize: int) -> None:
        """Redefines the bitesize of all Seq instances and the max_sequence accordingly"""
        if bytesize <= 0:
            raise ValueError(f"Seq: bytesize must be >= 1, got {bytesize}")
        cls.__bytesize = bytesize
        cls.__max_sequence = int("1" * (bytesize * 8), 2)

    @classmethod
    def getMaxSequence(cls) -> int:
        """Get max number after which the Seq wraps around"""
        return cls.__max_sequence

    def __new__(cls, value) -> "Seq":
        """Creates a Seq instance"""
        if not value:
            value = 0
        elif value > cls.__max_sequence:
            raise ValueError("Seq: value exceeds max sequence value")
        elif value < 0:
            raise ValueError("Seq: value cannot be negative")
        return super(Seq, cls).__new__(cls, value)

    def __add__(self, other) -> "Seq":
        """Add sequence numbers"""
        result = super().__add__(other)
        if result > self.__max_sequence:
            result -= self.__max_sequence
            logger.debug(f"Sequence number wrap-over reached at maximum of {self.__max_sequence}.")
        return self.__class__(result)

    def __sub__(self, other) -> int:
        """Calculate the difference between sequence numbers"""
        result = super().__sub__(other)
        threshold = (self.__max_sequence - 1) / 2
        if result > threshold:
            result -= self.__max_sequence
        elif result < -threshold:
            result += self.__max_sequence
        return int(result)

    def __lt__(self, other) -> bool:
        """Check if sequence number is lower than `other`"""
        return super().__lt__(super().__add__((other - self)))

    def __gt__(self, other) -> bool:
        """Check if sequence number is greater than `other`"""
        return super().__gt__(super().__add__((other - self)))

    def toSeqBytes(self) -> bytes:
        """Return representation of the number in the currenly set bytesize."""
        return super().to_bytes(self.__bytesize, "big")

    @classmethod
    def fromSeqBytes(cls, bytestring: bytes) -> "Seq":
        """Return `Seq` object that was encoded in given bytestring."""
        return cls(super().from_bytes(bytestring, "big"))


if __name__ == '__main__':
    print("***Testing sequence numbers***\n...")
    # addition
    assert Seq(2) + Seq(3) == 5
    assert Seq(2) + 3 == 5
    assert Seq.getMaxSequence() == 65535
    assert Seq(2) + 65535 == 2

    # subtraction : subtraction is strange but implemented for
    # > and < to < work for networking
    assert Seq(5) - Seq(3) == 2
    assert Seq.getMaxSequence() == 65535
    assert Seq(5) - Seq(65530) == 10

    # lesser than
    assert not Seq(5) < Seq(3)
    assert Seq.getMaxSequence() == 65535
    assert not Seq(5) < Seq(65500)  # weird but normal
    assert Seq(5) < Seq(100)

    # greater than
    assert Seq(5) > Seq(3)
    assert Seq.getMaxSequence() == 65535
    assert Seq(5) > Seq(65500)  # weird but normal
    assert not Seq(5) > Seq(100)

    print("***OK***")
