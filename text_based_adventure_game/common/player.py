"""The player data for the game."""

import json

from common.item import Item
from common.room import Room


class Player:
    """The player data for the game."""

    def __init__(
        self: "Player",
        name: str,
        location: Room,
        visited_rooms: list[str],
        inventory: list[Item],
        won: bool,
        watched_end_credits: bool,
    ) -> None:
        """Initialize the player."""
        self.name = name
        self.location = location
        self.visited_rooms = visited_rooms
        self.inventory = inventory
        self.won = won
        self.watched_end_credits = watched_end_credits

    def __repr__(self) -> str:
        """Representation of the item."""
        return json.dumps(self.__dict__, indent=4, sort_keys=True)  # pragma: no cover

    @staticmethod
    def default_player() -> "Player":
        """Return the default player."""
        return Player(
            "Player",
            Room.default_room(),
            [],
            [],
            False,
            False,
        )
