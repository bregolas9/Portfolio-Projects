"""The controller that manages interactions with the game world."""

from typing import Any

from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_type import RequestType
from common.service_type import ServiceType
from services.interaction_service import InteractionService


class InteractionController:
    """The controller that manages interactions with the game world."""

    def __init__(
        self: "InteractionController", services: dict[ServiceType, Any]
    ) -> None:
        """Initialize the interaction controller."""
        self.interaction_service: InteractionService = services[ServiceType.INTERACTION]
        self.request_types: list[RequestType] = [
            RequestType.PULL,
            RequestType.CHEW,
            RequestType.USE,
            RequestType.SIT,
            RequestType.CLEAN,
            RequestType.DRINK,
            RequestType.CLIMB,
            RequestType.TURN_ON,
            RequestType.OPEN,
            RequestType.PLAY,
            RequestType.FLUSH,
        ]

    def route(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Handle routing for this controller internally."""
        match request.action:
            case RequestType.USE:
                return self.use(request)
            case RequestType.CHEW:
                return self.chew(request)
            case RequestType.PULL:
                return self.pull(request)
            case RequestType.SIT:
                return self.sit(request)
            case RequestType.CLEAN:
                return self.clean(request)
            case RequestType.DRINK:
                return self.drink(request)
            case RequestType.CLIMB:
                return self.climb(request)
            case RequestType.TURN_ON:
                return self.turn_on(request)
            case RequestType.OPEN:
                return self.open(request)
            case RequestType.PLAY:
                return self.play(request)
            case RequestType.FLUSH:
                return self.flush(request)
            case _:
                return self.dont_know_how_to_do_that_message

    def use(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Use an item in the player's inventory or in the current room."""
        return self.interaction_service.use(request)

    def chew(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Chew an item in the player's inventory."""
        return self.interaction_service.chew(request)

    def pull(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Pull on an item in the room or player's inventory."""
        return self.interaction_service.pull(request)

    def sit(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Sit on an item in the room or player's inventory."""
        return self.interaction_service.sit(request)

    def clean(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Clean an item in the room or player's inventory."""
        return self.interaction_service.clean(request)

    def drink(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Drink an item in the room or player's inventory."""
        return self.interaction_service.drink(request)

    def climb(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Climb an item in the room."""
        return self.interaction_service.climb(request)

    def turn_on(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Turn on an item in the room or player's inventory."""
        return self.interaction_service.turn_on(request)

    def open(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Open an item in the room or player's inventory."""
        return self.interaction_service.open(request)

    def play(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Play an item in the room or player's inventory."""
        return self.interaction_service.play(request)

    def flush(self: "InteractionController", request: GameRequest) -> GameResponse:
        """Flush an item in the room or player's inventory."""
        return self.interaction_service.flush(request)

    @property
    def dont_know_how_to_do_that_message(self: "InteractionController") -> GameResponse:
        """Return the message for when the game doesn't know how to do something."""
        return GameResponse.failure("You are unsure how to do that.")
