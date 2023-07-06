"""A repository which manages access to shared game state."""

import sys
from typing import NoReturn

from common.environment import Environment
from common.game_response import GameResponse
from common.load_error import FileOperationError
from common.player import Player
from common.room import Room
from game_repository.art_manager import ArtManager
from game_repository.file_manager import FileManager
from game_repository.item_manager import ItemManager
from game_repository.objectives_manager import ObjectiveManager
from language.language_manager import LanguageManager
from language.story_manager import StoryManager


class GameRepository:
    """The repository which manages access to game state."""

    normal_scroll_delay = 0.01
    slow_scroll_delay = 0.02
    fast_scroll_delay = 0.005
    art_scroll_delay = 0.002
    off_scroll_delay = 0

    def __init__(self: "GameRepository", is_development: bool = False) -> None:
        """Initialize the game repository."""
        self.game_active: bool = True
        self.state_dirty: bool = False
        self.player: Player = Player.default_player()
        self.items: ItemManager = ItemManager()
        self.objectives: ObjectiveManager = ObjectiveManager()
        self.rooms: dict[str, Room] = dict()
        self.language: LanguageManager = LanguageManager()
        self.stories: StoryManager = StoryManager()
        self.environment: Environment = Environment(is_development)
        self.scroll_delay: float = GameRepository.normal_scroll_delay
        self.art_manager: ArtManager = ArtManager()

    def load_default_state(self: "GameRepository"):
        """Try to load the default game state."""
        self.language.load_language()
        self.stories.load_stories()
        self.items.load_items(new=True)
        self.art_manager.load_art()

    def try_load_game_state(
        self: "GameRepository", new: bool
    ) -> GameResponse | NoReturn:
        """Load the game state."""
        items_result = self.items.load_items(new=new)
        if isinstance(items_result, FileOperationError):
            if new:
                print(items_result.message)
                sys.exit(1)
            return GameResponse.failure(items_result.message)
        room_result = self.load_room_state(new=new)
        if isinstance(room_result, FileOperationError):
            if new:
                print(room_result.message)
                sys.exit(1)
            return GameResponse.failure(room_result.message)
        player_result = self.load_player_state(new=new)
        if isinstance(player_result, FileOperationError):
            if new:
                print(player_result.message)
                sys.exit(1)
            return GameResponse.failure(player_result.message)
        objectives_result = self.objectives.load_objectives(new=new)
        if isinstance(objectives_result, FileOperationError):
            if new:
                print(objectives_result.message)
                sys.exit(1)
            return GameResponse.failure(objectives_result.message)

        self.state_dirty = False

        message = "New game started." if new else "Game loaded successfully."
        return GameResponse.success(message)

    def load_room_state(self: "GameRepository", new: bool) -> None | FileOperationError:
        """Load the room state."""
        room_state = FileManager.get_room_file(new)
        if isinstance(room_state, FileOperationError):
            return room_state

        for room in room_state:
            inventory = self.items.get_list_of_items(room["inventory"])
            starting_inventory = self.items.get_list_of_items(
                room["starting_inventory"]
            )
            self.rooms[room["name"]] = Room(
                name=room["name"],
                description=room["description"],
                short_description=room["short_description"],
                exits=room["exits"],
                directional_exits=room["directional_exits"],
                aliases=room["aliases"],
                blockers=room["blockers"],
                inventory=inventory,
                starting_inventory=starting_inventory,
            )

    def load_player_state(
        self: "GameRepository", new: bool
    ) -> None | FileOperationError:
        """Load the player state."""
        player_state = FileManager.get_player_file(new=new)
        if isinstance(player_state, FileOperationError):
            return player_state
        player_location = self.get_room_by_name(player_state["location"])
        if player_location is None:
            player_location = self.rooms.get("entry")
        player_inventory = self.items.get_list_of_items(
            player_state.get("inventory", [])
        )
        self.player = Player(
            name=player_state.get("name", ""),
            location=player_location,
            visited_rooms=player_state.get("visited_rooms", []),
            inventory=player_inventory,
            won=player_state.get("won", False),
            watched_end_credits=player_state.get("watched_end_credits", False),
        )

    def save_game_state(self: "GameRepository") -> None:
        """Save the game state."""
        FileManager.save_player_file(self.player)
        FileManager.save_room_file(self.rooms)
        FileManager.save_items_file(self.items.items)
        FileManager.save_objectives_file(self.objectives.objectives)
        self.state_dirty = False

    def room_is_connected(self: "GameRepository", room: Room, target: str) -> bool:
        """Determine if the room is connected to the target room."""
        return target in room.exits

    def get_room_by_name(self: "GameRepository", name: str | None) -> Room | None:
        """Find the room with the given name."""
        for room in self.rooms.values():
            if room.name == name or name in room.aliases:
                return room
        return None

    def get_room_by_direction(
        self: "GameRepository", direction: str | None
    ) -> Room | None:
        """Find the room in the given direction."""
        if direction is None:
            return None
        parsed_direction = self.language.get_directional_alias(direction)
        if parsed_direction is None:
            return None
        directional_exit = self.current_location.directional_exit(parsed_direction)
        return self.get_room_by_name(
            "" if directional_exit is None else directional_exit
        )

    def move_player(self: "GameRepository", room: Room) -> None:
        """Move the player to a new location."""
        has_visited_before = room.name in self.player.visited_rooms
        self.player.location = room
        if not has_visited_before:
            self.player.visited_rooms.append(room.name)
        # mark the state as dirty since the player location is updated.
        self.state_dirty = True

    def find_target(self: "GameRepository", target: str, from_user: bool) -> str | None:
        """Find the target item which could be a room or an object."""
        if not from_user:
            return target

        if target == "":
            return None

        other_target = self.language.find_command_target(target)
        if other_target is not None:
            return other_target

        room = self.get_room_by_name(target)
        if room is not None:
            return room.name

        room = self.get_room_by_direction(target)
        if room is not None:
            return room.name

        inventory_item = self.items.get_item_by_name_by_room(target, self.player)
        if inventory_item is not None:
            return inventory_item.name

        return None

    @property
    def current_location(self: "GameRepository") -> Room:
        """Return the player's current location."""
        if self.player is None:
            return self.rooms["entry"]
        return self.player.location
