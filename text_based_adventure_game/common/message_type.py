"""A module that contains the MessageType class."""

from enum import Enum


class MessageType(Enum):
    """A class that represents a type of printable message."""

    PARAGRAPH = 1
    SINGLE_LINE = 2
    BLANK_LINE = 3
    ART = 4
