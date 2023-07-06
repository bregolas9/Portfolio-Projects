"""The controller that handles game events."""


from typing import Any

from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_type import RequestType
from common.service_type import ServiceType
from services.game_service import GameService


class GameController:
    """The controller that handles game events."""

    def __init__(self: "GameController", services: dict[ServiceType, Any]) -> None:
        """Initialize the game controller."""
        self.game_service: GameService = services[ServiceType.GAME]
        self.request_types = [
            RequestType.EXIT,
            RequestType.GAME_STORY,
            RequestType.SAVE_GAME,
            RequestType.LOAD_GAME,
            RequestType.NEW_GAME,
            RequestType.HELP,
            RequestType.OBJECTIVES,
            RequestType.ALIAS,
            RequestType.SCROLL,
            RequestType.HINT,
            RequestType.GAME_MAP,
            RequestType.DRAW,
        ]

    def route(self: "GameController", request: GameRequest) -> GameResponse:
        """Route the given game request and return the game response."""
        match request.action:
            case RequestType.EXIT:
                return self.exit(request)
            case RequestType.GAME_STORY:
                return self.game_story(request)
            case RequestType.SAVE_GAME:
                return self.save_game(request)
            case RequestType.LOAD_GAME:
                return self.load_game(request)
            case RequestType.NEW_GAME:
                return self.new_game(request)
            case RequestType.HELP:
                return self.provide_help(request)
            case RequestType.OBJECTIVES:
                return self.list_objective(request)
            case RequestType.ALIAS:
                return self.alias(request)
            case RequestType.SCROLL:
                return self.scroll(request)
            case RequestType.HINT:
                return self.hint(request)
            case RequestType.GAME_MAP:
                return self.draw(request)
            case RequestType.DRAW:
                return self.draw(request)
            case _:
                return self.dont_know_how_to_do_that_message

    def list_objective(self: "GameController", request: GameRequest) -> GameResponse:
        """List the current objectives."""
        return self.game_service.list_objective(request)

    def exit(self: "GameController", request: GameRequest) -> GameResponse:
        """Exit the game."""
        return self.game_service.exit(request)

    def game_story(self: "GameController", request: GameRequest) -> GameResponse:
        """Return the game story."""
        return self.game_service.game_story(request)

    def save_game(self: "GameController", request: GameRequest) -> GameResponse:
        """Save the game."""
        return self.game_service.save_game(request)

    def load_game(self: "GameController", request: GameRequest) -> GameResponse:
        """Load the game."""
        return self.game_service.load_game(request, False)

    def new_game(self: "GameController", request: GameRequest) -> GameResponse:
        """Start a new game."""
        return self.game_service.load_game(request, True)

    def provide_help(self: "GameController", request: GameRequest) -> GameResponse:
        """Provide help to the player."""
        return self.game_service.provide_help(request)

    def alias(self: "GameController", request: GameRequest) -> GameResponse:
        """Provide aliases for a target."""
        return self.game_service.give_aliases(request)

    def scroll(self: "GameController", request: GameRequest) -> GameResponse:
        """Change the scroll speed in the game."""
        return self.game_service.scroll(request)

    def hint(self: "GameController", request: GameRequest) -> GameResponse:
        """Gives the user a hint"""
        return self.game_service.get_hints(request)

    def draw(self: "GameController", request: GameRequest) -> GameResponse:
        """Draws art in the game."""
        return self.game_service.draw(request)

    @property
    def dont_know_how_to_do_that_message(self: "GameController") -> GameResponse:
        """Return the message for when the game doesn't know how to do something."""
        return GameResponse.failure("You are unsure how to do that.")
