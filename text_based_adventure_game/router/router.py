"""The router handles the GameRequest objects after creation by the text parser."""

from typing import Any

from common.controller_type import ControllerType
from common.game_request import GameRequest
from common.game_response import GameResponse
from controllers.game_controller import GameController
from controllers.interaction_controller import InteractionController
from controllers.inventory_controller import InventoryController
from controllers.movement_controller import MovementController


class Router:
    """A class that represents the router."""

    def __init__(self: "Router", controllers: dict[ControllerType, Any]) -> None:
        """Initialize the router."""
        self.controllers = controllers

    def route(self: "Router", request: GameRequest) -> GameResponse:
        """Route the given game request and return the game response."""
        if request.action in self.movement_controller.request_types:
            return self.movement_controller.route(request)
        elif request.action in self.game_controller.request_types:
            return self.game_controller.route(request)
        elif request.action in self.inventory_controller.request_types:
            return self.inventory_controller.route(request)
        elif request.action in self.interaction_controller.request_types:
            return self.interaction_controller.route(request)
        else:
            return self.dont_know_how_to_do_that_message

    @property
    def game_controller(self: "Router") -> GameController:
        """Returns the game controller."""
        return self.controllers[ControllerType.GAME]

    @property
    def movement_controller(self: "Router") -> MovementController:
        """Returns the movement controller."""
        return self.controllers[ControllerType.MOVEMENT]

    @property
    def inventory_controller(self: "Router") -> InventoryController:
        """Returns the inventory controller."""
        return self.controllers[ControllerType.INVENTORY]

    @property
    def interaction_controller(self: "Router") -> InteractionController:
        """Returns the interaction controller."""
        return self.controllers[ControllerType.INTERACTION]

    @property
    def dont_know_how_to_do_that_message(self: "Router") -> GameResponse:
        """Return when the router doesn't know how to handle the request."""
        return GameResponse.failure("You are unsure how to do that.")
