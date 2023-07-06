"""An enum that represents the type of request that is being made by the player."""

from enum import Enum


class RequestType(Enum):
    """An enum that represents the type of request that is being made by the player."""

    EXIT = 0
    MOVE = 1
    LOOK = 2
    TAKE = 3
    DROP = 4
    GAME_STORY = 5
    INSPECT = 6
    INVENTORY = 7
    LOAD_GAME = 8
    LOAD_GAME_DENIED = 9
    NEW_GAME = 10
    SAVE_GAME = 11
    HELP = 12
    USE = 13
    PULL = 14
    CHEW = 15
    OBJECTIVES = 16
    ALIAS = 17
    SIT = 18
    SCROLL = 19
    CLEAN = 20
    DRINK = 21
    HINT = 22
    GAME_MAP = 23
    CLIMB = 24
    TURN_ON = 25
    OPEN = 26
    PLAY = 27
    FLUSH = 28
    DRAW = 29
    UNKNOWN = 100
