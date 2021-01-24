#!/usr/bin/env python3
from threading import Lock
from Logger import logger


class LockedRessource:
    """
    Access a ressource thread-safely.
    This class makes an object available via a context manager that essentialy attaches a
    `threading.Lock` to it, that threads writing to this object should abide.
    """

    def __init__(self, ressource):
        self.lock: Lock = Lock()
        self.ressource = ressource

    def __enter__(self):
        """Lock `ressource` and return it."""
        self.lock.acquire()
        logger.debug(f"Acquired lock for {self.ressource}.")
        return self.ressource

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        """Release the lock."""
        self.lock.release()
        logger.debug(f"Released lock for {self.ressource}.")
