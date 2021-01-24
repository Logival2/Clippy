#!/usr/bin/env python3
"""Defines base class for serializable objects"""
import umsgpack
from Comparable import Comparable


class Serializable(Comparable):
    """Base class to make objects serializable with the msgpack protocol"""

    def toBytes(self) -> bytes:
        return umsgpack.packb(self.__dict__, force_float_precision="single")

    @classmethod
    def fromBytes(cls, packed_bytes: bytes):
        try:
            received = object.__new__(cls)
            received.__dict__ = umsgpack.unpackb(packed_bytes)
            return received
        except (umsgpack.InsufficientDataException, KeyError, TypeError):
            raise TypeError("Received bytes couldn't be parsed into " + cls.__name__ + ".")
