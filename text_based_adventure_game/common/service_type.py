"""An enum to represent the type of service used by the game."""

from enum import Enum


class ServiceType(Enum):
    """An enum to represent the type of service used by the game."""

    MOVEMENT = 0
    INVENTORY = 1
    GAME = 2
    INTERACTION = 3
