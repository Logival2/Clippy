#!/usr/bin/env python3
from Event import Event
from Utils.Seq import Seq
from Utils.Comparable import Comparable


_PROTOCOL_ID: bytes = bytes.fromhex("deadbeef")


class ProtocolIDError(ValueError):
    """When a package is not a valid Clippy package"""
    pass


class DuplicateSeqError(ConnectionError):
    """When a package has a sequence number already received before"""
    pass


class Header(Comparable):
    """Clippy package Header"""

    def __init__(self, sequence: int, ack: int, ack_bitfield: str):
        """
        sequence: package sequence number
        ack: sequence number of last received package
        ack_bitfield: 32 bytes string for the 32 sequence numbers before ack
            the first byte is for the sequence number just before ack and so on
            byte set to '1' means package was received, '0' means not received
        TODO: transform string bitfield into real bitfield of 4 bytes (4*8=32)
            and use bit flips
        """
        self.sequence = Seq(sequence)
        self.ack = Seq(ack)
        self.ack_bitfield = ack_bitfield

    def toByteArray(self) -> bytearray:
        """returns 12 bytes representing the header"""
        result = bytearray(_PROTOCOL_ID)
        result.extend(self.sequence.toSeqBytes())
        result.extend(self.ack.toSeqBytes())
        result.extend(int(self.ack_bitfield, 2).to_bytes(4, "big"))
        return result

    def destructure(self) -> tuple:
        """returns Header properties in a tuple"""
        return (self.sequence, self.ack, self.ack_bitfield)

    @classmethod
    def deconstructDatagram(cls, datagram: bytes) -> tuple:
        """returns a tuple with the header and the rest of the datagram"""
        if datagram[:4] != _PROTOCOL_ID:
            raise ProtocolIDError()
        sequence = Seq.fromSeqBytes(datagram[4:6])
        ack = Seq.fromSeqBytes(datagram[6:8])
        ack_bitfield = bin(int.from_bytes(datagram[8:12], "big"))[2:].zfill(32)
        payload = datagram[12:]
        return (cls(sequence, ack, ack_bitfield), payload)


class Package(Comparable):
    """UDP package implementing Clippy protocol"""
    __timeout: float = 1.0
    __max_size: int = 2048

    def __init__(self, header: Header, events: list = None):
        self.header = header
        self.__events = events if events is not None else []
        self.__datagram: bytes = None

    @property
    def events(self) -> list:
        return self.__events[:]

    def add_event(self, event: Event) -> None:
        """adds an event to the package"""
        if self.__datagram is not None:
            serialized = event.toBytes()
            if len(self.datagram) + len(serialized) + 2 > self.__max_size:
                raise OverflowError(f"Package exceeds max size of {self.__max_size} bytes.")
            self.__datagram += len(serialized).to_bytes(2, "big") + serialized
        self.__events.append(event)

    def getSize(self) -> int:
        """Returns the size of the underlying datagram"""
        if self.__datagram is None:
            self.toDatagram()
        return len(self.__datagram)

    def toDatagram(self) -> bytes:
        """Returns package serialized to bytes"""
        if self.__datagram is not None:
            return self.__datagram
        datagram = self.header.toByteArray()  # first 12 bytes of the package
        datagram.extend(self.__createEventsBlock())
        if len(datagram) > self.__max_size:
            raise OverflowError(f"Package exceeds max size of {self.__max_size} bytes.")
        self.__datagram = datagram
        return self.__datagram

    def __createEventsBlock(self) -> bytearray:
        block = bytearray()
        for ev in self.__events:
            serialized = ev.toBytes()
            block.extend(len(serialized).to_bytes(2, "big"))
            block.extend(serialized)
        return block

    @classmethod
    def fromBytes(cls, datagram: bytes) -> "Package":
        header, payload = Header.deconstructDatagram(datagram)
        events = cls.__readEventsBlock(payload)
        result = cls(header, events)
        result.__datagram = datagram
        return result

    @staticmethod
    def __readEventsBlock(block: bytes) -> list:
        events = []
        while block:
            size = int.from_bytes(block[:2], "big")
            events.append(Event.fromBytes(block[2: size + 2]))
            block = block[size + 2:]
        return events
