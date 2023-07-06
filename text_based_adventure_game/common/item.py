"""Represents a game object that a user would interact with."""


import json
from typing import Any


class Item:
    """Represents a game object that a user would interact with."""

    def __init__(
        self: "Item",
        name: str,
        alias: list[str],
        description: list[str],
        look_at_message: dict[str, str],
        is_collectible: bool,
        discovered: bool,
        interactions: dict[str, Any],
        locked: bool = False,
        hidden: bool = False,
    ) -> None:
        """Initialize the item."""
        self.name: str = name
        self.alias: list[str] = alias
        self._description: list[str] = description
        self.look_at_message: dict[str, str] = look_at_message
        self.is_collectible: bool = is_collectible
        self.discovered: bool = discovered
        self.interactions: dict[str, Any] = interactions
        self.locked = locked
        self.hidden = hidden

    def __repr__(self) -> str:
        """Representation of the item."""
        return json.dumps(self.__dict__, indent=4, sort_keys=True)  # pragma: no cover

    @property
    def description(self: "Item") -> str:
        """Return the description of the item."""
        return " ".join(self._description)

    @description.setter
    def description(self: "Item", description: list[str]) -> None:
        """Set the description of the item."""
        self._description = description
