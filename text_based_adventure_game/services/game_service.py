"""The service that handles game events."""

from typing import Tuple

from common.game_message import GameMessage
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from game_repository.game_repository import GameRepository


class GameService:
    """The service that handles game events."""

    def __init__(self: "GameService", game_repository: GameRepository) -> None:
        """Initialize the game service."""
        self.repository = game_repository

    def exit(self: "GameService", _: GameRequest) -> GameResponse:
        """Exit the game."""
        self.repository.game_active = False
        return GameResponse(
            [],
            RequestStatus.SUCCESS,
        )

    def game_story(self: "GameService", request: GameRequest) -> GameResponse:
        """Print game stories for the user."""
        if len(request.targets) == 0:
            return GameResponse.failure("No story found.")
        game_story = self.repository.stories.get_story(request.targets[0])
        status = RequestStatus.SUCCESS
        if game_story is None or len(game_story) == 0:
            return GameResponse.failure("No story found.")
        messages = []
        for story in game_story:
            messages.append(GameMessage.blank_line())
            messages.append(GameMessage.paragraph(story))
        return GameResponse(messages, status)

    def save_game(self: "GameService", _: GameRequest) -> GameResponse:
        """Save the game."""
        try:
            self.repository.save_game_state()
            return GameResponse.success("Your game was saved successfully.")
        except Exception as e:
            return GameResponse.failure(
                f"An error occurred while saving your game: {e}"
            )

    def load_game(self: "GameService", _: GameRequest, new: bool) -> GameResponse:
        """Load the game."""
        return self.repository.try_load_game_state(new=new)

    def provide_help(self: "GameService", _: GameRequest) -> GameResponse:
        """Provide help contents."""
        command_header = "Available Commands:"
        commands = self.repository.language.help_contents
        return GameResponse.success_with_header_and_strings(command_header, commands)

    def list_objective(self: "GameService", _: GameRequest) -> GameResponse:
        """List the current objectives."""
        header = "Current Objectives:"
        messages = []
        for objective in self.repository.objectives.objectives.values():
            messages.append(
                f"{objective.name} - complete: {objective.is_complete(self.repository.player)}"
            )
        return GameResponse.success_with_header_and_strings(header, messages)

    def give_aliases(self: "GameService", request: GameRequest) -> GameResponse:
        """Get aliases for specified target."""
        if len(request.targets) == 0:
            return self.no_alias_provided_response

        target_item_name = request.targets[0]
        if target_item_name is None:
            return self.no_alias_provided_response

        item_name = self.repository.find_target(target_item_name, True)
        if item_name is None:
            return self.alias_not_found_response(target_item_name)

        possible_room = self.repository.get_room_by_name(item_name)
        if possible_room is not None:
            return self.get_alias_response(possible_room.aliases, item_name)

        possible_item = self.repository.items.get_item_by_name_by_room(
            item_name, self.repository.player
        )
        if possible_item is not None:
            return self.get_alias_response(possible_item.alias, item_name)

        other_aliases = self.repository.language.get_request_type_aliases(item_name)
        if len(other_aliases) > 0:
            return self.get_alias_response(other_aliases, item_name)

        return self.alias_not_found_response(item_name)

    def scroll(self: "GameService", request: GameRequest) -> GameResponse:
        """Change the scroll speed of the game."""
        if len(request.targets) == 0 or request.targets[0] is None:
            return self.invalid_scroll_speed_response
        existing_speed = self.repository.scroll_delay
        scroll_speed = request.targets[0]
        new_speed, udpated = self.get_new_scroll_speed(existing_speed, scroll_speed)
        if not udpated:
            return GameResponse.failure("Text printing speed not changed.")
        self.repository.scroll_delay = new_speed
        return GameResponse.success(
            self.get_scroll_speed_update_description(scroll_speed)
        )

    def get_new_scroll_speed(
        self: "GameService", existing_speed: float, speed_target: str
    ) -> Tuple[float, bool]:
        """Get a new scroll speed given an input phrase."""
        new_speed = existing_speed
        if speed_target in self.repository.language.fast_words:
            new_speed = GameRepository.fast_scroll_delay
        elif speed_target in self.repository.language.medium_words:
            new_speed = GameRepository.normal_scroll_delay
        elif speed_target in self.repository.language.slow_words:
            new_speed = GameRepository.slow_scroll_delay
        elif speed_target in self.repository.language.off_words:
            new_speed = GameRepository.off_scroll_delay
        else:
            return (existing_speed, False)
        return (new_speed, new_speed != existing_speed)

    def get_scroll_speed_update_description(
        self: "GameService", player_word: str
    ) -> str:
        """Get a description of the scroll speed."""
        speed_descriptor = "UNKNOWN SPEED"
        if (
            player_word in self.repository.language.fast_words
            or player_word in self.repository.language.medium_words
            or player_word in self.repository.language.slow_words
        ):
            speed_descriptor = player_word
        elif player_word in self.repository.language.off_words:
            speed_descriptor = "off"

        if speed_descriptor == "UNKNOWN SPEED":
            return "Text printing speed not changed."
        elif speed_descriptor == "off":
            return f"Text printing effects turned off."
        else:
            return f"Text printing speed changed to {speed_descriptor}."

    def draw(self: "GameService", request: GameRequest) -> GameResponse:
        """Draws great art."""
        return GameResponse.art(
            self.repository.art_manager.get_art_by_name(request.targets[0])
        )

    def get_hints(self: "GameService", _: GameRequest) -> GameResponse:
        """Get hints for the current objective."""
        # get back the first incomplete objective
        objectives = self.repository.objectives.objectives.values()
        player = self.repository.player
        incomplete = list(
            filter(lambda objective: not objective.is_complete(player), objectives)
        )[:1]
        # extract the hint
        objective = incomplete[0]
        objective.increment_hint_count()
        # return successful response from hint
        return GameResponse.success_with_header_and_strings(
            "You begin to ponder deeply:", objective.hints
        )

    @staticmethod
    def get_alias_response(aliases: list[str], item_name: str) -> GameResponse:
        """Create a response for a list of aliases."""
        if len(aliases) == 0:
            return GameResponse.failure(f"No aliases found for '{item_name}'.")

        return GameResponse.success_with_header_and_strings(
            f"Aliases for '{item_name}':", aliases
        )

    @property
    def no_alias_provided_response(self: "GameService") -> GameResponse:
        """Create a response for no alias provided."""
        return GameResponse.failure("Please provide an alias to get help for.")

    def alias_not_found_response(self: "GameService", item_name: str) -> GameResponse:
        """Create a response for alias not found."""
        return GameResponse.failure(f"Unable to find an alias for '{item_name}'.")

    @property
    def invalid_scroll_speed_response(self: "GameService") -> GameResponse:
        """Create a response for invalid scroll speed."""
        return GameResponse.failure("Please provide a valid scroll speed to change to.")
