"""A class which represents a game objective."""

from typing import Any

from common.player import Player
from common.room import Room


class GameObjective:
    """A class which represents a game objective."""

    def __init__(
        self: "GameObjective",
        name: str,
        hints: list[str],
        requirements: list[str],
        interactions: list[dict[str, Any]],
    ) -> None:
        """Initialize the game objective."""
        self.name = name
        self._hints = hints
        self.hint_count = 0
        # This property ensures that a player must have certain items nearby.
        self.requirements = requirements
        # This property requires that the
        self.interactions: list[dict[str, Any]] = interactions

    def __repr__(self: "GameObjective") -> str:
        """Return the string representation of the game objective."""
        return f"{self.name}, {self._hints}, {self.requirements}, {self.interactions}"

    def is_complete(self: "GameObjective", player: Player) -> bool:
        """Return True if the objective is complete."""
        # find out if all required items are near the player.
        for requirement in self.requirements:
            if not self.in_room_inventory(
                player.location, requirement
            ) and not self.in_player_inventory(player, requirement):
                return False
        for interaction in self.interactions:
            if interaction["complete"] is False:
                return False
        return True

    def complete_interaction_objective(
        self: "GameObjective", item: str, action: str
    ) -> None:
        """Set the interaction objective to complete."""
        for interaction in self.interactions:
            if (
                interaction["item"] == item
                and interaction["interaction_type"] == action
            ):
                interaction["complete"] = True

    def increment_hint_count(self):
        self.hint_count += 1

    @property
    def hints(self):
        return self._hints[: self.hint_count]

    @staticmethod
    def in_room_inventory(room: Room, item_name: str) -> bool:
        """Return True if the item is in the room's inventory."""
        item = next((item for item in room.inventory if item.name == item_name), None)
        if item is None or item.is_collectible:
            return False
        return True

    @staticmethod
    def in_player_inventory(player: Player, item_name: str) -> bool:
        """Return True if the item is in the player's inventory."""
        item = next((item for item in player.inventory if item.name == item_name), None)
        return item is not None
