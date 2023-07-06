"""The controller which handles player movement."""

from typing import Any
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_type import RequestType
from services.movement_service import MovementService
from common.service_type import ServiceType


class MovementController:
    """The controller which handles player movement."""

    def __init__(self: "MovementController", services: dict[ServiceType, Any]) -> None:
        """Initialize the movement controller."""
        self.movement_service: MovementService = services[ServiceType.MOVEMENT]
        self.request_types = [RequestType.MOVE, RequestType.LOOK]

    def route(self: "MovementController", request: GameRequest) -> GameResponse:
        """Route the given request and return the game response."""
        match request.action:
            case RequestType.MOVE:
                return self.move(request)
            case RequestType.LOOK:
                return self.look(request)
            case _:
                return self.dont_know_how_to_do_that_message

    def move(self: "MovementController", request: GameRequest) -> GameResponse:
        """Move the player in the given direction."""
        return self.movement_service.move(request)

    def look(self: "MovementController", request: GameRequest) -> GameResponse:
        """Look in the given direction."""
        return self.movement_service.look(request)

    @property
    def dont_know_how_to_do_that_message(self: "MovementController") -> GameResponse:
        """Return the message for when the game doesn't know how to do something."""
        return GameResponse.failure("You are unsure how to do that.")
