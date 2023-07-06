"""The service which handles inventory management in the game."""

from common.game_message import GameMessage
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.item import Item
from common.player import Player
from common.request_status import RequestStatus
from common.room import Room
from game_repository.game_repository import GameRepository


class InventoryService:
    """The service which handles inventory management."""

    def __init__(self: "InventoryService", repository: GameRepository) -> None:
        """Initialize the inventory service."""
        self.repository = repository

    def open_inventory(self: "InventoryService", _: GameRequest) -> GameResponse:
        """Return the contents of the inventory."""
        messages = self.get_inventory_contents(self.repository.player)
        if len(messages) == 0:
            return GameResponse.success("You have no items in your inventory.")

        return GameResponse.success_with_header_and_strings(
            "Inventory Contents:", messages
        )

    def get_inventory_contents(self: "InventoryService", player: Player) -> list[str]:
        """Return the contents of the inventory."""
        messages = []
        for item in player.inventory:
            messages.append(f"{item.name.capitalize()} - {item.description}")

        return messages

    def pick_up(self: "InventoryService", request: GameRequest) -> GameResponse:
        """Add an item to the player inventory."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        if item is None:
            return self.item_not_found_response
        current_room = self.repository.current_location
        player = self.repository.player
        validation_result = self.handle_pickup_validation(player, current_room, item)
        if validation_result is not None:
            return validation_result
        self.remove_item_from_room_and_add_to_player(player, current_room, item)
        return self.item_added_response(item)

    def drop(self: "InventoryService", request: GameRequest) -> GameResponse:
        """Remove an item from the player inventory."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        if item is None:
            return self.item_not_found_response
        current_room = self.repository.current_location
        player = self.repository.player
        validation_result = self.handle_drop_validation(player, current_room, item)
        if validation_result is not None:
            return validation_result
        self.remove_item_from_player_and_add_to_room(player, current_room, item)
        return self.item_removed_response(item, current_room)

    def look_at(self: "InventoryService", request: GameRequest) -> GameResponse:
        """Look at an item and provide its look_at_message."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        if item is None or (
            item not in self.repository.player.inventory
            and item not in self.repository.current_location.inventory
        ):
            return self.item_not_found_response
        else:
            messages = []
            for key in item.look_at_message.keys():
                message = item.look_at_message.get(key, "")
                stripped_key = key.replace("list_", "")
                if self.should_strike_message(stripped_key):
                    message = self.strike(item.look_at_message[key])
                if self.should_add_look_at_line(key):
                    if not self.is_list(key):
                        messages.append(GameMessage.blank_line())
                    messages.append(GameMessage.paragraph(message))
            return GameResponse(messages, RequestStatus.SUCCESS)

    def is_list(self: "InventoryService", key: str) -> bool:
        """Decide whether to strike the line with the corresponding key."""
        return key[:5] == "list_"

    def should_add_look_at_line(self: "InventoryService", key: str) -> bool:
        """Decide whether to add the line with the corresponding key to the message."""
        item = self.repository.items.get_item_by_name(key)
        if item is None:
            return True
        else:
            return not item.discovered and not item.hidden

    def item_added_response(self: "InventoryService", item: Item) -> GameResponse:
        """Return a response for when an item is added to the player's inventory."""
        header = "You added an item to your inventory:"
        message = f"{item.name.capitalize()} - {item.description}"
        return GameResponse.success_with_header(header, message)

    def item_removed_response(
        self: "InventoryService", item: Item, room: Room
    ) -> GameResponse:
        """Return a response for when an item is removed from the player's inventory."""
        header = f"You dropped an item in {room.name}:"
        message = f"{item.name.capitalize()} - {item.description}"
        return GameResponse.success_with_header(header, message)

    def remove_item_from_room_and_add_to_player(
        self: "InventoryService", player: Player, room: Room, item: Item
    ) -> None:
        """Remove an item from the room and add it to the player's inventory."""
        room.inventory.remove(item)
        player.inventory.append(item)
        item.discovered = True
        self.repository.state_dirty = True

    def remove_item_from_player_and_add_to_room(
        self: "InventoryService", player: Player, room: Room, item: Item
    ) -> None:
        """Remove an item from the player's inventory and add it to the room."""
        player.inventory.remove(item)
        room.inventory.append(item)
        self.repository.state_dirty = True

    def handle_pickup_validation(
        self: "InventoryService", player: Player, room: Room, item: Item
    ) -> GameResponse | None:
        """Handle validation for picking up an item."""
        if item is None or item == "":
            return self.item_not_found_response
        elif item not in room.inventory and item in player.inventory:
            return self.you_already_have_that_response
        elif not item.is_collectible or item.locked:
            return self.item_not_collectible_response
        elif item not in room.inventory:
            return self.item_not_found_response

    def handle_drop_validation(
        self: "InventoryService", player: Player, room: Room, item: Item
    ) -> GameResponse | None:
        """Handle validation for dropping an item."""
        if item is None or item == "":
            return self.item_not_found_response
        if item not in player.inventory:
            return self.item_not_in_player_inventory_response
        if item in room.inventory:
            return self.item_already_in_room_response

    def strike(self: "InventoryService", text: str):
        """Strike through the given text."""
        return text.replace("-", "x")

    def should_strike_message(self: "InventoryService", key: str) -> bool:
        """Decide whether to strike through the message."""
        possible_objective = self.repository.objectives.get_objective_by_name(key)
        if possible_objective is None:
            return False
        else:
            return possible_objective.is_complete(self.repository.player)

    @property
    def item_not_in_player_inventory_response(self: "InventoryService") -> GameResponse:
        """Return a response for when an item is not in the player's inventory."""
        return GameResponse.failure("You don't have that item in your inventory.")

    @property
    def item_not_found_response(self: "InventoryService") -> GameResponse:
        """Return a response for when an item is not found."""
        return GameResponse.failure("Hmm, you can't seem to find that.")

    @property
    def item_not_collectible_response(self: "InventoryService") -> GameResponse:
        """Return a response for when an item is not collectible."""
        return GameResponse.failure("You can't pick that up.")

    @property
    def you_already_have_that_response(self: "InventoryService") -> GameResponse:
        """Return a response for when an item is already in the player's inventory."""
        return GameResponse.failure("You already have that item in your inventory.")

    @property
    def item_already_in_room_response(self: "InventoryService") -> GameResponse:
        """Return a response for when an item is already in the room."""
        return GameResponse.failure("That item is already in this room.")
