"""Test the features of the game repository."""
import builtins
from unittest.mock import MagicMock, patch

import pytest

from common.item import Item
from common.load_error import FileOperationError
from common.player import Player
from common.request_status import RequestStatus
from common.room import Room
from game_repository.file_manager import FileManager
from game_repository.game_repository import GameRepository
from game_repository.item_manager import ItemManager
from game_repository.objectives_manager import ObjectiveManager
from language.language_manager import LanguageManager
from language.story_manager import StoryManager
from tests.test_helpers import any_message_contents


def test_game_repository_room_is_connected_when_connected():
    """Test the room_is_connected method when a room should be connected."""

    current_room = Room(
        name="current",
        description={"test": "a test room"},
        exits=["other"],
        directional_exits={"west": "other"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    other_room = Room(
        name="other",
        description={"test": "a test room"},
        exits=["current"],
        directional_exits={"east": "current"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.try_load_game_state = MagicMock(return_value=None)
    game_repository.rooms = {
        current_room.name: current_room,
        other_room.name: other_room,
    }
    assert game_repository.room_is_connected(current_room, "other")


def test_game_repository_room_is_connected_when_not_connected():
    """Test the room_is_connected method when a room should not be connected."""

    current_room = Room(
        name="current",
        description={"test": "a test room"},
        exits=[],
        directional_exits={},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    other_room = Room(
        name="other",
        description={"test": "a test room"},
        exits=["current"],
        directional_exits={"east": "current"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.try_load_game_state = MagicMock(return_value=None)
    game_repository.rooms = {
        current_room.name: current_room,
        other_room.name: other_room,
    }
    assert not game_repository.room_is_connected(current_room, "other")


def test_move_player_updates_player_location():
    """Test that the player location is updated when the player moves."""

    current_room = Room(
        name="current",
        description={"test": "a test room"},
        exits=["other"],
        directional_exits={"east": "other"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    other_room = Room(
        name="other",
        description={"test": "a test room"},
        exits=["current"],
        directional_exits={"west": "current"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.try_load_game_state = MagicMock(return_value=None)
    game_repository.rooms = {
        current_room.name: current_room,
        other_room.name: other_room,
    }
    game_repository.player = Player("Test Player", current_room, [], [], False, False)
    game_repository.move_player(other_room)
    assert game_repository.player.location == other_room


def test_current_location():
    """Test that the current location is returned correctly."""

    current_room = Room(
        name="current",
        description={"test": "a test room"},
        exits=["other"],
        directional_exits={},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.try_load_game_state = MagicMock(return_value=None)
    game_repository.rooms = {
        current_room.name: current_room,
    }
    game_repository.player = Player("Test Player", current_room, [], [], False, False)
    assert game_repository.current_location == current_room


def test_get_room_by_name_when_exists():
    """Test the get_room_by_name method when the room exists."""
    expected_room = Room(
        name="expected",
        description={"test": "a test room"},
        exits=[],
        directional_exits={},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.try_load_game_state = MagicMock(return_value=None)
    game_repository.rooms = {
        expected_room.name: expected_room,
    }
    assert game_repository.get_room_by_name("expected") == expected_room


def test_get_room_by_name_when_not_exist():
    """Test the get_room_by_name method when the room does not exist."""
    game_repository = GameRepository()
    game_repository.rooms = {}
    assert game_repository.get_room_by_name("expected") is None


def test_find_target_in_room_when_exists():
    """Test the find_target method when the target exists."""
    expected_target = "room"
    room = Room(
        name="room",
        description={"test": "a test room"},
        exits=[],
        directional_exits={},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.language = MagicMock(LanguageManager)
    game_repository.language.find_command_target = MagicMock(return_value=None)
    game_repository.get_room_by_name = MagicMock(return_value=room)
    assert game_repository.find_target(expected_target, True) == room.name


def test_find_target_in_room_when_not_exist():
    """Test the find_target method with the target does not exist."""
    expected_target = "room"
    room = Room(
        name="room",
        description={"test": "a test room"},
        exits=[],
        directional_exits={},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.language = MagicMock(LanguageManager)
    game_repository.language.language = MagicMock()
    game_repository.language.find_command_target = MagicMock(return_value=None)
    game_repository.rooms = {"room": room}
    game_repository.language.get_directional_alias = MagicMock(return_value=None)
    game_repository.items = MagicMock(ItemManager)
    game_repository.items.get_item_by_name = MagicMock(return_value=None)
    game_repository.items.get_item_by_name_by_room = MagicMock(return_value=None)
    game_repository.get_room_by_direction = MagicMock(return_value=None)
    game_repository.get_room_by_name = MagicMock(return_value=None)
    assert game_repository.find_target(expected_target, True) is None


def test_get_directional_exit():
    """Test to ensure that the directional exit is returned correctly."""
    room = Room(
        name="room",
        description={"test": "a test room"},
        exits=["other"],
        directional_exits={"north": "other"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    other_room = Room(
        name="other",
        description={"test": "a test room"},
        exits=["room"],
        directional_exits={"south": "room"},
        blockers=[],
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    game_repository = GameRepository()
    game_repository.language = MagicMock(LanguageManager)
    game_repository.language.get_directional_alias = MagicMock(return_value="north")

    game_repository.player = Player(
        name="player",
        location=room,
        visited_rooms=[],
        inventory=[],
        won=False,
        watched_end_credits=False,
    )

    game_repository.rooms = {
        room.name: room,
        other_room.name: other_room,
    }

    assert game_repository.get_room_by_direction("north") == other_room


def test_repository_can_find_directional_targets():
    """Test to make sure that the find target method returns a room by direction."""

    repo = GameRepository()
    repo.rooms = {
        "room": Room(
            name="room",
            description={"test": "a test room"},
            exits=["other"],
            directional_exits={"north": "other"},
            blockers=[],
            aliases=[],
            inventory=[],
            starting_inventory=[],
        ),
        "other": Room(
            name="other",
            description={"test": "a test room"},
            exits=["room"],
            directional_exits={"south": "room"},
            blockers=[],
            aliases=[],
            inventory=[],
            starting_inventory=[],
        ),
    }
    repo.player = Player(
        name="player",
        location=repo.rooms["room"],
        visited_rooms=[],
        inventory=[],
        won=False,
        watched_end_credits=False,
    )
    repo.language = MagicMock(LanguageManager)
    repo.language.language = {
        "move_north": ["north", "n", "up", "u"],
        "move_south": ["south", "s", "down", "d"],
        "move_east": ["east", "e", "right", "r"],
        "move_west": ["west", "w", "left", "l"],
    }
    repo.language.get_directional_alias = MagicMock(return_value="north")
    assert repo.get_room_by_name("north") is None
    assert repo.get_room_by_direction("north") == repo.rooms["other"]


def test_it_should_find_valid_non_user_targets():
    """Test if the game repository can find valid non-user targets."""
    repo = GameRepository()
    assert repo.find_target("north", False) == "north"


def test_it_should_have_dirty_state_after_movement():
    """When a player moves, the game state should be dirty."""
    repo = GameRepository()
    repo.state_dirty = False
    repo.player = MagicMock(Player)
    repo.player.visited_rooms = []
    repo.player.location = MagicMock(Room)
    repo.rooms = {
        "north": Room(
            name="north",
            description={"test": "a test room"},
            exits=[],
            directional_exits={},
            blockers=[],
            aliases=[],
            inventory=[],
            starting_inventory=[],
        )
    }
    repo.move_player(repo.rooms["north"])
    assert repo.state_dirty == True


def test_it_should_load_state_when_load_game_state_called():
    """Test if the other load state methods are called when load_game_state is called."""

    repo = GameRepository()
    repo.load_room_state = MagicMock()
    repo.load_player_state = MagicMock()
    repo.items = MagicMock(ItemManager)
    repo.items.load_items = MagicMock()
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.load_objectives = MagicMock()

    repo.state_dirty = True

    repo.try_load_game_state(new=False)
    repo.load_room_state.assert_called_once_with(new=False)
    repo.load_player_state.assert_called_once_with(new=False)
    repo.items.load_items.assert_called_once_with(new=False)
    repo.objectives.load_objectives.assert_called_once_with(new=False)
    assert repo.state_dirty == False


def test_it_should_load_new_game_when_new_game_state_called():
    """Test if the new game load functions are called when new_game_state is called."""
    repo = GameRepository()
    repo.load_room_state = MagicMock()
    repo.load_player_state = MagicMock()
    repo.items = MagicMock(ItemManager)
    repo.items.load_items = MagicMock()
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.load_objectives = MagicMock()
    repo.state_dirty = True

    repo.try_load_game_state(new=True)
    repo.load_room_state.assert_called_once_with(new=True)
    repo.load_player_state.assert_called_once_with(new=True)
    repo.items.load_items.assert_called_once_with(new=True)
    repo.objectives.load_objectives.assert_called_once_with(new=True)
    assert repo.state_dirty == False


def test_load_room_state_runs_when_called():
    """Test to make sure the load_room_state function behaves normally."""
    game_repo = GameRepository()
    rooms = [
        {
            "name": "entry",
            "description": {
                "description1": "test description 1",
            },
            "short_description": "short description 1",
            "exits": ["cloak room", "parlor"],
            "directional_exits": {
                "north": None,
                "east": "cloak room",
                "south": "parlor",
                "west": None,
            },
            "aliases": ["entryway", "start", "foyer", "beginning"],
            "blockers": [
                {
                    "name": "turn on flashlight",
                    "message": "You can't see anything in the dark. You should find a light source.",
                }
            ],
            "starting_inventory": [
                "flashlight",
                "loafers",
                "bench",
                "light switch",
                "chandelier",
                "entry door",
                "hook",
            ],
            "inventory": [
                "flashlight",
                "loafers",
                "bench",
                "light switch",
                "chandelier",
                "entry door",
                "hook",
            ],
        },
    ]
    with patch.object(FileManager, "get_room_file", return_value={}) as mock_room_file:
        game_repo.load_room_state(True)
        with patch.object(
            FileManager, "get_room_file", return_value=rooms
        ) as mock_room_file:
            with patch.object(builtins, "print", return_value=None):
                game_repo.load_room_state(True)
                mock_room_file.assert_called_once_with(True)
                possible_entry = game_repo.rooms.get("entry")
                assert possible_entry is not None
                assert possible_entry.name == "entry"


def test_load_player_state_should_update_the_player():
    """Test to make sure the player is loaded with the correct data."""
    game_repo = GameRepository()
    game_repo.rooms = {
        "entry": Room(
            name="entry",
            description={"test": "a test room"},
            short_description="a room",
            exits=["cloak room", "parlor"],
            directional_exits={
                "north": "",
                "east": "cloak room",
                "south": "parlor",
                "west": "",
            },
            aliases=["entryway", "start", "foyer", "beginning"],
            blockers=[],
            inventory=[],
            starting_inventory=[],
        )
    }
    json_data = {
        "name": "Player",
        "location": "entry",
        "visited_rooms": ["entry"],
        "inventory": [],
    }
    FileManager.get_player_file = MagicMock(return_value=json_data)
    game_repo.load_player_state(True)
    assert game_repo.player.name == "Player"
    assert game_repo.player.location == game_repo.rooms["entry"]
    assert game_repo.player.visited_rooms == ["entry"]

    json_data = {
        "name": "Player",
        "location": None,
        "visited_rooms": ["entry"],
        "inventory": [],
    }
    game_repo.get_room_by_name = MagicMock(name="get_room_by_name", return_value=None)
    game_repo.load_player_state(True)
    assert game_repo.current_location == game_repo.rooms["entry"]
    with patch.object(builtins, "print", return_value=None):
        with patch.object(
            FileManager, "get_player_file", return_value=FileOperationError("a message")
        ):
            game_repo.load_player_state(True)


def test_it_should_find_empty_string_when_target_none():
    """It should return None when the target is an empty string."""
    game_repo = GameRepository()
    assert game_repo.find_target("", True) is None


def test_it_should_return_none_when_room_direction_missing():
    """It should return None when the direction is missing."""
    game_repo = GameRepository()
    assert game_repo.get_room_by_direction(None) == None


def test_it_should_return_entry_when_player_is_none():
    """Test to make sure current_location returns the entry when the player is None."""
    game_repo = GameRepository()
    game_repo.player = None  # type: ignore
    entry = Room(
        name="entry",
        description={"test": "a test room"},
        short_description="a room",
        exits=["cloak room", "parlor"],
        directional_exits={
            "north": "",
            "east": "cloak room",
            "south": "parlor",
            "west": "",
        },
        aliases=["entryway", "start", "foyer", "beginning"],
        blockers=[],
        inventory=[],
        starting_inventory=[],
    )
    game_repo.rooms = {"entry": entry}
    assert game_repo.current_location == game_repo.rooms["entry"]


def test_it_should_save_game_state():
    """Test to make sure the save_game_state method works."""
    FileManager.save_player_file = MagicMock()
    FileManager.save_room_file = MagicMock()
    FileManager.save_items_file = MagicMock()
    FileManager.save_objectives_file = MagicMock()
    repo = GameRepository()
    repo.state_dirty = True
    repo.save_game_state()
    FileManager.save_player_file.assert_called_once()
    FileManager.save_room_file.assert_called_once()
    FileManager.save_items_file.assert_called_once()
    FileManager.save_objectives_file.assert_called_once()
    assert repo.state_dirty == False


def test_it_should_return_file_operation_error_when_item_state_none():
    """Test to make sure that the try_load_game_state method returns FileOperationError when the item state is None."""
    error = FileOperationError("a message")
    with patch.object(ItemManager, "load_items", return_value=error):
        repo = GameRepository()
        result = repo.try_load_game_state(False)
        assert any_message_contents(result.messages, error.message)
        assert result.status == RequestStatus.FAILURE


def test_it_should_return_file_operation_error_when_room_state_none():
    """Test to make sure that the try_load_game_state method returns FileOperationError when the room state is None."""
    error = FileOperationError("a message")
    with patch.object(GameRepository, "load_room_state", return_value=error):
        with patch.object(ItemManager, "load_items", return_value=None):
            repo = GameRepository()
            repo.items = MagicMock(ItemManager)
            result = repo.try_load_game_state(False)
            assert any_message_contents(result.messages, error.message)
            assert result.status == RequestStatus.FAILURE


def test_it_should_return_file_operation_error_when_player_state_none():
    """Test to make sure that the try_load_game_state method
    returns FileOperationError when the player state is None."""
    error = FileOperationError("a message")
    with patch.object(GameRepository, "load_player_state", return_value=error):
        with patch.object(GameRepository, "load_room_state", return_value=None):
            with patch.object(ItemManager, "load_items", return_value=None):
                repo = GameRepository()
                repo.items = MagicMock(ItemManager)
                result = repo.try_load_game_state(False)
                assert any_message_contents(result.messages, error.message)
                assert result.status == RequestStatus.FAILURE


def test_it_should_return_file_operation_error_when_objectives_state_none():
    """Test to make sure that the try_load_game_state method
    returns FileOperationError when the player state is None."""
    error = FileOperationError("a message")
    with patch.object(ObjectiveManager, "load_objectives", return_value=error):
        with patch.object(GameRepository, "load_player_state", return_value=None):
            with patch.object(GameRepository, "load_room_state", return_value=None):
                with patch.object(ItemManager, "load_items", return_value=None):
                    repo = GameRepository()
                    repo.items = MagicMock(ItemManager)
                    result = repo.try_load_game_state(False)
                    assert any_message_contents(result.messages, error.message)
                    assert result.status == RequestStatus.FAILURE


def test_it_should_exit_when_new_game_and_player_state_none():
    """Test to make sure the game exits when a new game and player state can't be loaded."""
    error = FileOperationError("a message")
    repo = GameRepository()
    repo.items = MagicMock(ItemManager)
    repo.items.load_items = MagicMock(return_value=None)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.load_objectives = MagicMock(return_value=None)
    repo.load_room_state = MagicMock(return_value=None)
    with patch.object(GameRepository, "load_player_state", return_value=error):
        with patch.object(builtins, "print", return_value=None) as mock_print:
            with pytest.raises(SystemExit):
                repo.try_load_game_state(True)
            mock_print.assert_called_once_with(error.message)


def test_it_should_exit_when_new_game_and_room_state_none():
    """Test to make sure the game exits when a new game and player state can't be loaded."""
    error = FileOperationError("a message")
    repo = GameRepository()
    repo.items = MagicMock(ItemManager)
    repo.items.load_items = MagicMock(return_value=None)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.load_objectives = MagicMock(return_value=None)
    repo.load_player_state = MagicMock(return_value=None)
    with patch.object(GameRepository, "load_room_state", return_value=error):
        with patch.object(builtins, "print", return_value=None) as mock_print:
            with pytest.raises(SystemExit):
                repo.try_load_game_state(True)
            mock_print.assert_called_once_with(error.message)


def test_it_should_exit_when_new_game_and_item_state_none():
    """Test to make sure that the game exits when a new game and item state can't be loaded."""
    error = FileOperationError("a message")
    repo = GameRepository()
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.load_objectives = MagicMock(return_value=None)
    repo.load_player_state = MagicMock(return_value=None)
    repo.load_room_state = MagicMock(return_value=None)
    with patch.object(ItemManager, "load_items", return_value=error):
        with patch.object(builtins, "print", return_value=None) as mock_print:
            with pytest.raises(SystemExit):
                repo.try_load_game_state(True)
            mock_print.assert_called_once_with(error.message)


def test_it_should_exit_when_new_game_and_objective_state_none():
    """Test to make sure that the game exits when a new game and objective state can't be loaded."""
    error = FileOperationError("a message")
    repo = GameRepository()
    repo.items = MagicMock(ItemManager)
    repo.items.load_items = MagicMock(return_value=None)
    repo.load_player_state = MagicMock(return_value=None)
    repo.load_room_state = MagicMock(return_value=None)
    with patch.object(ObjectiveManager, "load_objectives", return_value=error):
        with patch.object(builtins, "print", return_value=None) as mock_print:
            with pytest.raises(SystemExit):
                repo.try_load_game_state(True)
            mock_print.assert_called_once_with(error.message)


def test_it_should_return_file_operation_error_when_room_state_error():
    """Test to make sure that the try_load_game_state method returns
    FileOperationError when the room state is an error."""
    error = FileOperationError("a message")
    with patch.object(FileManager, "get_room_file", return_value=error):
        repo = GameRepository()
        repo.items = MagicMock(ItemManager)
        repo.items.load_items = MagicMock(return_value=None)
        result = repo.try_load_game_state(False)
        assert any_message_contents(result.messages, error.message)
        assert result.status == RequestStatus.FAILURE


def test_it_should_get_item_names():
    """Test to see if it can find a target with an item name."""
    repo = GameRepository()
    repo.items = MagicMock(ItemManager)
    mock_item = Item(
        name="item",
        alias=["alias"],
        description=["a thing"],
        look_at_message={"line1": "a thing"},
        is_collectible=True,
        discovered=False,
        interactions={},
    )
    repo.language = MagicMock(LanguageManager)
    repo.language.find_command_target = MagicMock(return_value=None)
    repo.language.get_directional_alias = MagicMock(return_value=None)
    repo.items.get_item_by_name_by_room = MagicMock(return_value=mock_item)
    assert repo.find_target("item", True) == mock_item.name


def test_it_should_load_state():
    """Test to make sure that load_default_state works."""

    repo = GameRepository()
    repo.language = MagicMock(LanguageManager)
    repo.language.load_language = MagicMock()
    repo.items = MagicMock(ItemManager)
    repo.items.load_items = MagicMock()
    repo.stories = MagicMock(StoryManager)
    repo.stories.load_stories = MagicMock()
    repo.art_manager.load_art = MagicMock()
    repo.load_default_state()
    repo.language.load_language.assert_called_once()
    repo.items.load_items.assert_called_once()
    repo.stories.load_stories.assert_called_once()
    repo.art_manager.load_art.assert_called_once()


def test_find_target_should_find_other_targets():
    """Test to make sure the find_target method finds other targets."""
    repo = GameRepository()
    repo.language = MagicMock(LanguageManager)
    repo.language.find_command_target = MagicMock(return_value="target")
    result = repo.find_target("target", True)
    assert result == "target"


def test_find_target_should_find_room_targets_by_direction():
    """Test to make sure the find_target method finds room targets."""
    repo = GameRepository()
    repo.language = MagicMock(LanguageManager)
    repo.language.find_command_target = MagicMock(return_value=None)
    room = MagicMock(Room)
    room.name = "room"
    room.aliases = ["alias"]
    repo.get_room_by_name = MagicMock(return_value=None)
    repo.get_room_by_direction = MagicMock(return_value=room)

    result = repo.find_target("room", True)
    assert result == "room"
