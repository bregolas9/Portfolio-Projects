"""The service which handles movement in the game."""

from common.game_message import GameMessage
from common.game_objective import GameObjective
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from common.room import Room
from game_repository.game_repository import GameRepository


class MovementService:
    """The service which handles player movement."""

    def __init__(self: "MovementService", repository: GameRepository) -> None:
        """Initialize the movement service."""
        self.repository = repository

    def look(self: "MovementService", request: GameRequest) -> GameResponse:
        """Repeat the long description of the room occupied by the player.

        Returns various responses if the room does not exist, the user
        is trying the look method on a target which is not a room, or
        the room is not the room they are standing in.
        """
        if len(request.targets) == 0 or request.targets[0] is None:
            return self.look_response()
        target = self.repository.find_target(request.targets[0], True)
        current_location = self.repository.current_location
        room = self.repository.get_room_by_name(request.targets[0])
        if target == current_location.name:
            return self.look_response()
        elif target is None:
            return self.non_existent_room_response
        elif room is None or target != room.name:
            return self.this_is_not_a_room_response
        else:
            return self.too_far_to_see_response

    def get_look_description(
        self: "MovementService", visited_before: bool
    ) -> list[GameMessage]:
        """Return the description of a room when looking."""
        location = self.repository.current_location
        dropped_item_messages = self.get_dropped_item_description()
        messages = [
            GameMessage.blank_line(),
            GameMessage.paragraph(
                location.short_description if visited_before else location.description
            ),
        ]
        if len(dropped_item_messages) > 0:
            temp = GameResponse.success_with_header_and_strings(
                "You previously dropped some items on the floor:", dropped_item_messages
            )
            messages += temp.messages
        return messages

    def get_dropped_item_description(self: "MovementService") -> list[str]:
        """Describe any collectible items that are discovered as being on the floor."""
        return [
            f"{item.name.capitalize()} - {item.description}"
            for item in self.repository.current_location.inventory
            if item.is_collectible and item.discovered
        ]

    def move(self: "MovementService", request: GameRequest) -> GameResponse:
        """Move the player in the given direction."""
        if len(request.targets) == 0:
            return self.generic_cant_do_that_response
        room = self.repository.get_room_by_name(request.targets[0])
        if room is None:
            room = self.repository.get_room_by_direction(request.targets[0])
        if room is None:
            return self.generic_cant_do_that_response
        elif self.is_blocked(room):
            return self.blocked_room_response(self.get_blocked_message(room))
        elif self.already_here(room):
            return self.already_here_response
        elif not self.can_move(request.targets[0]):
            return self.path_not_connected_response
        else:
            has_visited_before = room.name in self.repository.player.visited_rooms
            self.repository.move_player(room)
            return self.look_response(has_visited_before)

    def is_blocked(self: "MovementService", room: Room) -> bool:
        """Determine if the room is blocked."""
        blockers = room.blockers
        if len(blockers) == 0:
            return False
        objectives: list[GameObjective] = []
        for blocker in blockers:
            objective = self.repository.objectives.get_objective_by_name(
                blocker["name"]
            )
            if objective is not None:
                objectives.append(objective)
        return not all(
            objective.is_complete(self.repository.player) for objective in objectives
        )

    def get_blocked_message(self: "MovementService", room: Room) -> str:
        """Get the message to display when the room is blocked."""
        blockers = room.blockers
        if len(blockers) == 0:
            return ""
        for blocker in blockers:
            objective = self.repository.objectives.get_objective_by_name(
                blocker["name"]
            )
            if objective is not None and not objective.is_complete(
                self.repository.player
            ):
                return blocker["message"]
        return "Tell the developer that they messed up..."

    def can_move(self: "MovementService", room_name: str | None) -> bool:
        """Determine if the player can move to the given room."""
        if room_name is None:
            return False
        new_room = self.repository.get_room_by_name(room_name)
        if new_room is None:
            new_room = self.repository.get_room_by_direction(room_name)
        current_room = self.repository.current_location
        return (
            new_room is not None
            and self.is_connected(current_room, new_room.name)
            and not self.is_blocked(new_room)
        )

    def is_connected(self: "MovementService", room: Room, target: str) -> bool:
        """Determine if the room is connected to the target room."""
        return target in room.exits

    def already_here(self: "MovementService", room: Room) -> bool:
        """Determine if the player is already in the given room."""
        current_location = self.repository.current_location
        return (
            room.name == current_location.name or room.name in current_location.aliases
        )

    def look_response(
        self: "MovementService", visited_before: bool = False
    ) -> GameResponse:
        """Respond to a look command."""
        return GameResponse(
            self.get_look_description(visited_before), RequestStatus.SUCCESS
        )

    @property
    def non_existent_room_response(self: "MovementService") -> GameResponse:
        """The message to display when the room doesn't exist."""
        return GameResponse.failure("Hmm, it seems like that room doesn't exist.")

    def blocked_room_response(self: "MovementService", message: str) -> GameResponse:
        """Display when the room is blocked."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.paragraph(message),
        ]
        return GameResponse(messages, RequestStatus.FAILURE)

    @property
    def already_here_response(self: "MovementService") -> GameResponse:
        """The message to display when the player is already in the room."""
        return GameResponse.failure("Hmm, it seems like you're already there.")

    @property
    def path_not_connected_response(self: "MovementService") -> GameResponse:
        """The message to display when the path is not connected."""
        return GameResponse.failure("Hmm, it seems like you can't go that way.")

    @property
    def too_far_to_see_response(self: "MovementService") -> GameResponse:
        """Display when the user is trying to look at an adjacent room."""
        return GameResponse.failure(
            "Hmm, it seems like you can't quite see that room from here."
            + " Try moving closer."
        )

    @property
    def generic_cant_do_that_response(self: "MovementService") -> GameResponse:
        """The response to return for a look command when the room can't be found.

        It's possible that the single word command was in error.
        """
        return GameResponse.failure("Hmm, it seems like you can't do that.")

    @property
    def this_is_not_a_room_response(self: "MovementService") -> GameResponse:
        """The response to return for a look command when the target provided is not a room."""
        return GameResponse.failure(
            "You can only use the look command to look at rooms,"
            " try the inspect command instead."
        )
