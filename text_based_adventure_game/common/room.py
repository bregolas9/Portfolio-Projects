"""Represents a room in the game."""

import json

from common.item import Item


class Room:
    """A room in the game."""

    def __init__(
        self: "Room",
        name: str,
        description: dict[str, str],
        exits: list[str],
        directional_exits: dict[str, str],
        aliases: list[str],
        inventory: list[Item],
        starting_inventory: list[Item],
        blockers: list[dict[str, str]],
        short_description: str = "This is a default short description.",
    ) -> None:
        """Initialize the room."""
        self.name = name
        self._description = description
        self.short_description = short_description
        self.exits = exits
        self.directional_exits = directional_exits
        self.aliases = aliases
        self.blockers = blockers
        self.inventory = inventory
        self.starting_inventory = starting_inventory

    def directional_exit(self: "Room", direction: str) -> str | None:
        """Get the room name for the given direction.

        Args:
            direction (str): The direction to get the room name for. This expects
            "north" "south" "east" or "west".

        Returns:
            str | None: The room name for the given direction or None if the direction
            is not valid.
        """
        return self.directional_exits[direction]

    def __repr__(self) -> str:
        """Representation of the item."""
        return json.dumps(self.__dict__, indent=4, sort_keys=True)  # pragma: no cover

    @property
    def description(self: "Room") -> str:
        """Provide a room description.

        Returns:
            str: Use the description of the room and optional item descriptions
            for undiscovered collectible items.
        """
        description = ""
        for key in self._description.keys():
            possible_item = self.get_starting_inventory_item_by_name(key)
            if possible_item is not None:
                if (
                    possible_item.is_collectible
                    and not possible_item.discovered
                    and not possible_item.hidden
                ):
                    description += f"{self._description[key]} "
            else:
                description += f"{self._description[key]} "
        return description

    def get_starting_inventory_item_by_name(self: "Room", name: str) -> Item | None:
        """Return a starting inventory item by name if found or None."""
        for item in self.starting_inventory:
            if item.name == name:
                return item
        return None

    @property
    def inventory_item_names(self: "Room") -> list[str]:
        """Return the names of all inventory items."""
        return [item.name for item in self.inventory]

    @staticmethod
    def default_room() -> "Room":
        """Return the default room."""
        return Room(
            name="default",
            description={"default": "This is a default room."},
            exits=[],
            directional_exits={},
            aliases=[],
            inventory=[],
            blockers=[],
            starting_inventory=[],
        )
