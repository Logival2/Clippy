#!/usr/bin/env python3


class Comparable:
    """Base class to compare objects by their dicts"""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
