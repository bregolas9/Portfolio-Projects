"""The controller which handles inventory actions."""

from typing import Any
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_type import RequestType
from common.service_type import ServiceType
from services.inventory_service import InventoryService


class InventoryController:
    """The controller which handles player inventory."""

    def __init__(self: "InventoryController", services: dict[ServiceType, Any]) -> None:
        """Initialize the inventory controller."""
        self.inventory_service: InventoryService = services[ServiceType.INVENTORY]
        self.request_types: list[RequestType] = [
            RequestType.TAKE,
            RequestType.DROP,
            RequestType.INVENTORY,
            RequestType.INSPECT,
        ]

    def route(self: "InventoryController", request: GameRequest) -> GameResponse:
        """Handle routing for this controller internally."""
        match request.action:
            case RequestType.TAKE:
                return self.pick_up(request)
            case RequestType.DROP:
                return self.drop(request)
            case RequestType.INVENTORY:
                return self.open_inventory(request)
            case RequestType.INSPECT:
                return self.look_at(request)
            case _:
                return self.dont_know_how_to_do_that_message

    def look_at(self: "InventoryController", request: GameRequest) -> GameResponse:
        """Look at an item in the player's inventory."""
        return self.inventory_service.look_at(request)

    def pick_up(self: "InventoryController", request: GameRequest) -> GameResponse:
        """Add items to player inventory."""
        return self.inventory_service.pick_up(request)

    def drop(self: "InventoryController", request: GameRequest) -> GameResponse:
        """Remove an item from the player's inventory."""
        return self.inventory_service.drop(request)

    def open_inventory(
        self: "InventoryController", request: GameRequest
    ) -> GameResponse:
        """Display current contents of the player's inventory."""
        return self.inventory_service.open_inventory(request)

    @property
    def dont_know_how_to_do_that_message(self: "InventoryController") -> GameResponse:
        """Return the message for when the game doesn't know how to do something."""
        return GameResponse.failure("You are unsure how to do that.")
