"""A class to manage the initial list of possible game items."""

from common.item import Item
from common.load_error import FileOperationError
from game_repository.file_manager import FileManager
from common.player import Player


class ItemManager:
    """A class to manage the list of game items."""

    def __init__(self: "ItemManager") -> None:
        """Initialize the item manager."""
        self.items: dict[str, Item] = dict()

    def load_items(self: "ItemManager", new: bool) -> None | FileOperationError:
        """Load the initial list of items."""
        items_state = FileManager.get_items_file(new)
        if isinstance(items_state, FileOperationError):
            return items_state

        items: dict[str, Item] = dict()
        for item in items_state:
            name = str(item["name"])
            alias = item.get("alias", [])
            is_collectible = bool(item["is_collectible"])
            description = item["description"]
            look_at_message = item["look_at_message"]
            discovered = bool(item["discovered"])
            interactions = item["interactions"]
            locked = item.get("locked", False)
            hidden = item.get("hidden", False)
            new_item = Item(
                name=name,
                alias=alias,
                is_collectible=is_collectible,
                description=description,
                look_at_message=look_at_message,
                discovered=discovered,
                interactions=interactions,
                locked=locked,
                hidden=hidden,
            )
            items[name] = new_item
        self.items = items

    def get_item_by_name(self: "ItemManager", name: str | None) -> Item | None:
        """Get an item by name."""
        for items in self.items.values():
            if items.name == name or name in items.alias:
                return items
        return None

    def get_item_by_name_by_room(
        self: "ItemManager", name: str | None, player: Player
    ) -> Item | None:
        """Get an item by name per room"""
        for items in player.inventory:
            if items.name == name or name in items.alias:
                return items
        for items in player.location.inventory:
            if items.name == name or name in items.alias:
                return items
        return None

    def get_list_of_items(self: "ItemManager", item_names: list[str]) -> list[Item]:
        """Get a list of items by name."""
        found_items: list[Item] = []
        for item_name in item_names:
            item = self.get_item_by_name(item_name)
            if item is not None:
                found_items.append(item)
        return found_items
