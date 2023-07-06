"""Represents the type of controller."""

from enum import Enum


class ControllerType(Enum):
    """Represents the type of controller."""

    MOVEMENT = 0
    INVENTORY = 1
    GAME = 2
    INTERACTION = 3
