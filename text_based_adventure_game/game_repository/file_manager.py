"""Loads and saves the game state using JSON files. Used to help the game repository."""

import copy
import json
import os
import sys
from typing import Any, NoReturn

from common.game_objective import GameObjective
from common.item import Item
from common.load_error import FileOperationError
from common.player import Player
from common.room import Room


class FileManager:
    """Load state from json files to support the game repository."""

    default_player_file = "data/player.json"
    default_room_file = "data/rooms.json"
    saved_player_file = "save_data/player.json"
    saved_room_file = "save_data/rooms.json"
    language_file = "data/language.json"
    stories_file = "data/game_stories.json"
    default_items_file = "data/items.json"
    saved_items_file = "save_data/items.json"
    default_objectives_file = "data/objectives.json"
    saved_objectives_file = "save_data/objectives.json"
    game_art_file = "data/game_art.json"

    @staticmethod
    def has_saved_game() -> bool:  # pragma: no cover
        """Check to see if a saved game exists."""
        player_file = FileManager.join_base_path(FileManager.saved_player_file)
        room_file = FileManager.join_base_path(FileManager.saved_room_file)
        items_file = FileManager.join_base_path(FileManager.saved_items_file)
        objectives_file = FileManager.join_base_path(FileManager.saved_objectives_file)
        return (
            os.path.exists(player_file)
            and os.path.exists(room_file)
            and os.path.exists(items_file)
            and os.path.exists(objectives_file)
        )

    @staticmethod
    def bad_operation_message(operation_type: str, file_name: str) -> str:
        """Print a message to the user for bad file operations."""
        return (
            f"An unexpected error occurred while {operation_type} the {file_name} file."
        )

    @staticmethod
    def handle_bad_load(operation_type: str, file_name: str) -> NoReturn:
        """Handle a bad load operation."""
        print(FileManager.bad_operation_message(operation_type, file_name))
        sys.exit(1)

    @staticmethod
    def get_player_file(new: bool) -> dict[str, Any] | FileOperationError:
        """Get the player file data."""
        default_player_file = FileManager.join_base_path(
            FileManager.default_player_file
        )
        saved_player_file = FileManager.join_base_path(FileManager.saved_player_file)
        try:
            if new:
                with open(default_player_file, "r") as player_file:
                    return json.loads(player_file.read())
            else:
                with open(saved_player_file, "r") as player_file:
                    return json.loads(player_file.read())
        except Exception:
            return FileOperationError(
                FileManager.bad_operation_message("loading", "player")
            )

    @staticmethod
    def get_room_file(new: bool) -> list[dict[str, Any]] | FileOperationError:
        """Get the room file data."""
        default_room_file = FileManager.join_base_path(FileManager.default_room_file)
        saved_room_file = FileManager.join_base_path(FileManager.saved_room_file)
        try:
            if new:
                with open(default_room_file, "r") as room_file:
                    return json.loads(room_file.read())
            else:
                with open(saved_room_file, "r") as room_file:
                    return json.loads(room_file.read())
        except Exception:
            return FileOperationError(
                FileManager.bad_operation_message("loading", "room")
            )

    @staticmethod
    def get_items_file(new: bool) -> list[dict[str, Any]] | FileOperationError:
        """Get the room file."""
        default_items_file = FileManager.join_base_path(FileManager.default_items_file)
        saved_items_file = FileManager.join_base_path(FileManager.saved_items_file)
        try:
            if new:
                with open(default_items_file, "r") as items_file:
                    return json.loads(items_file.read())
            else:
                with open(saved_items_file, "r") as items_file:
                    return json.loads(items_file.read())
        except Exception:
            return FileOperationError(
                FileManager.bad_operation_message("loading", "items")
            )

    @staticmethod
    def get_objectives_file(new: bool) -> list[dict[str, Any]] | FileOperationError:
        """Load the game objectives."""
        default_objectives_file = FileManager.join_base_path(
            FileManager.default_objectives_file
        )
        saved_objectives_file = FileManager.join_base_path(
            FileManager.saved_objectives_file
        )
        try:
            if new:
                with open(default_objectives_file, "r") as objectives_file:
                    return json.loads(objectives_file.read())
            else:
                with open(saved_objectives_file, "r") as objectives_file:
                    return json.loads(objectives_file.read())
        except Exception:
            return FileOperationError(
                FileManager.bad_operation_message("loading", "objectives")
            )

    @staticmethod
    def load_language() -> dict[str, list[str]]:
        """Load the language values."""
        language_file_path = FileManager.join_base_path(FileManager.language_file)
        try:
            with open(language_file_path, "r") as language_file:
                return json.loads(language_file.read())
        except Exception:
            FileManager.handle_bad_load("loading", "language")

    @staticmethod
    def load_game_stories() -> dict[str, list[str]]:
        """Load the game stories."""
        stories_file_path = FileManager.join_base_path(FileManager.stories_file)
        try:
            with open(stories_file_path, "r") as stories_file:
                return json.loads(stories_file.read())
        except Exception:
            FileManager.handle_bad_load("loading", "stories")

    @staticmethod
    def save_player_file(player: Player) -> None:
        """Save the player file."""
        serializable_player = copy.deepcopy(vars(player))
        serializable_player["inventory"] = [item.name for item in player.inventory]
        serializable_player["location"] = player.location.name
        saved_player_file_path = FileManager.join_base_path(
            FileManager.saved_player_file
        )
        try:
            # check to see if save_data folder exists
            if not os.path.exists(FileManager.join_base_path("save_data")):
                os.makedirs(FileManager.join_base_path("save_data"))
            with open(saved_player_file_path, "w") as player_file:
                player_file.write(
                    json.dumps(serializable_player, indent=4, sort_keys=False)
                )
        except Exception:
            FileManager.bad_operation_message("saving", "player")

    @staticmethod
    def save_room_file(rooms: dict[str, Room]) -> None:
        """Save the rooms in the room file."""
        saved_room_file_path = FileManager.join_base_path(FileManager.saved_room_file)
        serializable_rooms = []
        for room in rooms.values():
            serializable_room = copy.deepcopy(vars(room))
            serializable_room["inventory"] = [item.name for item in room.inventory]
            serializable_room["starting_inventory"] = [
                item.name for item in room.starting_inventory
            ]
            serializable_room["description"] = room._description
            del serializable_room["_description"]
            serializable_rooms.append(serializable_room)

        try:
            # check to see if save_data folder exists
            if not os.path.exists(FileManager.join_base_path("save_data")):
                os.makedirs(FileManager.join_base_path("save_data"))
            with open(saved_room_file_path, "w") as room_file:
                room_file.write(
                    json.dumps(serializable_rooms, indent=4, sort_keys=False)
                )
        except Exception:
            FileManager.bad_operation_message("saving", "rooms")

    @staticmethod
    def save_items_file(items: dict[str, Item]) -> None:
        """Save the items in the items file."""
        saved_items_file_path = FileManager.join_base_path(FileManager.saved_items_file)
        serializable_items = []
        for item in items.values():
            serializable_item = copy.deepcopy(vars(item))
            serializable_item["description"] = item._description
            del serializable_item["_description"]
            serializable_items.append(serializable_item)

        try:
            # check to see if save_data folder exists
            if not os.path.exists(FileManager.join_base_path("save_data")):
                os.makedirs(FileManager.join_base_path("save_data"))
            with open(saved_items_file_path, "w") as items_file:
                items_file.write(
                    json.dumps(serializable_items, indent=4, sort_keys=False)
                )
        except Exception:
            FileManager.bad_operation_message("saving", "items")

    @staticmethod
    def save_objectives_file(objectives: dict[str, GameObjective]) -> None:
        """Save the objectives to the objectives file."""
        saved_objectives_file = FileManager.join_base_path(
            FileManager.saved_objectives_file
        )
        serializable_objectives = []
        for objective in objectives.values():
            serializable_objective = copy.deepcopy(vars(objective))
            serializable_objective["requires"] = serializable_objective["requirements"]
            serializable_objective["hints"] = serializable_objective["_hints"]
            del serializable_objective["_hints"]
            del serializable_objective["hint_count"]
            del serializable_objective["requirements"]
            serializable_objectives.append(serializable_objective)

        try:
            # check to see if save_data folder exists
            if not os.path.exists(FileManager.join_base_path("save_data")):
                os.makedirs(FileManager.join_base_path("save_data"))
            with open(saved_objectives_file, "w") as objectives_file:
                objectives_file.write(
                    json.dumps(serializable_objectives, indent=4, sort_keys=False)
                )
        except Exception:
            FileManager.bad_operation_message("saving", "objectives")

    @staticmethod
    def load_art() -> dict[str, list[str]]:
        """Load the game_map."""
        game_art_file_path = FileManager.join_base_path(FileManager.game_art_file)
        try:
            with open(game_art_file_path, "r") as game_art_file:
                return json.loads(game_art_file.read())
        except Exception:
            FileManager.handle_bad_load("loading", "game art")

    @staticmethod
    def join_base_path(file_name: str) -> str:
        """Join the base path to the file name."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_path, file_name).replace("\\", "/")
        return full_path
