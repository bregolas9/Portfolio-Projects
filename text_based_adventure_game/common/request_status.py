"""An enum that represents the status of a GameRequest."""

from enum import Enum


class RequestStatus(Enum):
    """An enum that represents the status of a GameRequest."""

    SUCCESS = 0
    FAILURE = 1
    ERROR = 2
