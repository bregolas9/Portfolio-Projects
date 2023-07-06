import builtins
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from common.game_objective import GameObjective
from common.item import Item
from common.load_error import FileOperationError
from common.player import Player
from common.room import Room
from game_repository.file_manager import FileManager


def exception_on_open(filename, mode) -> None:
    """Raise an exception when opening a file for testing."""
    raise Exception("File not found")


def default_player() -> Player:
    """A test player for testing."""
    room = Room(
        name="Test Room",
        description={"test": "a test room"},
        inventory=[],
        starting_inventory=[],
        exits=["Test Exit"],
        directional_exits={},
        aliases=["Test Alias"],
        blockers=[],
    )
    player = Player(
        name="Test Player",
        location=room,
        inventory=[],
        visited_rooms=["Test Room"],
        won=False,
        watched_end_credits=False,
    )
    return player


def default_rooms() -> dict[str, Room]:
    """Return a default listing of rooms for testing."""
    room = Room(
        name="Test Room",
        description={"test": "a test room"},
        inventory=[],
        starting_inventory=[],
        exits=["Test Exit"],
        directional_exits={},
        aliases=["Test Alias"],
        blockers=[],
    )
    return {"Test Room": room}


def default_items() -> dict[str, Item]:
    """Return a default listing of items for testing."""
    item = Item(
        name="Test Item",
        alias=["Test Alias"],
        description=["a test item"],
        look_at_message={"line1": "a test item"},
        is_collectible=True,
        discovered=False,
        interactions={},
    )
    return {"Test Item": item}


def default_objectives() -> dict[str, GameObjective]:
    objective = GameObjective("test", [], ["test requirements"], [])
    return {"test": objective}


def test_it_should_load_room_files():
    """Test to make sure it loads the room file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_room_file(False)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.saved_room_file), "r"
        )

    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_room_file(True)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.default_room_file), "r"
        )


def test_it_should_get_player_files():
    """Test to make sure it loads the player file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_player_file(False)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.saved_player_file), "r"
        )

    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_player_file(True)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.default_player_file), "r"
        )


def test_it_should_get_objectives_files():
    """Test to make sure it can open the objectives file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_objectives_file(False)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.saved_objectives_file), "r"
        )

    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_objectives_file(True)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.default_objectives_file), "r"
        )


def test_it_should_load_the_language_file():
    """Test to make sure it can load the language file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.load_language()
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.language_file), "r"
        )


def test_it_should_load_the_game_stories_file():
    """Test to make sure it can load the language file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.load_game_stories()
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.stories_file), "r"
        )


def test_file_manager_language_file_handles_raises():
    """Test to make sure the language file handles exceptions."""

    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(SystemExit):
            FileManager.load_language()


def test_file_manager_game_stories_handles_raises():
    """Test to make sure the game stories file handles exceptions."""
    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(SystemExit):
            FileManager.load_game_stories()


def test_it_should_save_player_state():
    """Test to make sure it can save player state."""
    with patch.object(builtins, "open", mock_open()) as mock_file:
        with patch.object(os, "makedirs", return_value=None) as mockdirs:
            with patch.object(os.path, "exists", return_value=False) as mockexists:
                FileManager.save_player_file(default_player())
                mock_file.assert_called_once_with(
                    FileManager.join_base_path(FileManager.saved_player_file), "w"
                )
                mockdirs.assert_called_once()
                mockexists.assert_called_once()


def test_it_should_handle_player_save_exceptions():
    """Test to make sure exceptions are handled during player state saving."""
    with patch.object(builtins, "open", exception_on_open):
        assert FileManager.save_player_file(default_player()) == None


def test_it_should_save_room_state():
    """Test to make sure it can save room state."""
    with patch.object(builtins, "open", mock_open()) as mock_file:
        with patch.object(os, "makedirs", return_value=None) as mockdirs:
            with patch.object(os.path, "exists", return_value=False) as mockexists:
                FileManager.save_room_file(default_rooms())
                mock_file.assert_called_once_with(
                    FileManager.join_base_path(FileManager.saved_room_file), "w"
                )
                mockdirs.assert_called_once()
                mockexists.assert_called_once()


def test_it_should_handle_room_save_exceptions():
    """Test to make sure it handles room saving exceptions."""
    with patch.object(builtins, "open", exception_on_open):
        assert FileManager.save_room_file(default_rooms()) == None


def test_it_should_save_item_state():
    """test to make sure it can save item state."""
    with patch.object(builtins, "open", mock_open()) as mock_file:
        with patch.object(os, "makedirs", return_value=None) as mockdirs:
            with patch.object(os.path, "exists", return_value=False) as mockexists:
                FileManager.save_items_file(default_items())
                mock_file.assert_called_once_with(
                    FileManager.join_base_path(FileManager.saved_items_file), "w"
                )
                mockdirs.assert_called_once()
                mockexists.assert_called_once()


def test_it_should_save_objectives_state():
    """test to make sure it can save objective state."""
    with patch.object(builtins, "open", mock_open()) as mock_file:
        with patch.object(os, "makedirs", return_value=None) as mockdirs:
            with patch.object(os.path, "exists", return_value=False) as mockexists:
                FileManager.save_objectives_file(default_objectives())
                mock_file.assert_called_once_with(
                    FileManager.join_base_path(FileManager.saved_objectives_file), "w"
                )
                mockdirs.assert_called_once()
                mockexists.assert_called_once()


def test_it_should_handle_objective_save_exceptions():
    """Test to make sure it handles item saving exceptions."""
    with patch.object(builtins, "open", exception_on_open):
        assert FileManager.save_objectives_file(default_objectives()) is None


def test_it_should_handle_item_save_exceptions():
    """Test to make sure it handles item saving exceptions."""
    with patch.object(builtins, "open", exception_on_open):
        assert FileManager.save_items_file(default_items()) is None


def test_it_should_handle_player_file_exceptions():
    """Make sure the get_player_file method returns FileOperationError on exception."""
    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(Exception):
            assert FileManager.get_player_file(False) == FileOperationError


def test_it_should_handle_room_file_exceptions():
    """Make sure the get_player_file method returns FileOperationError on exception."""
    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(Exception):
            assert FileManager.get_room_file(False) == FileOperationError


def test_it_should_handle_items_file_exceptions():
    """Make sure the get_items_file method returns FileOperationError on exception."""
    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(Exception):
            assert FileManager.get_items_file(False) == FileOperationError


def test_it_should_handle_objectives_file_exceptions():
    """Make sure the get_objectives_file method returns FileOperationError on exception."""
    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(Exception):
            assert FileManager.get_objectives_file(False) == FileOperationError


def test_it_should_read_from_the_items_file():
    """Test to make sure it opens the room file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_items_file(new=True)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.default_items_file), "r"
        )


def test_it_should_read_from_the_save_items_file():
    """Test to make sure it opens the items file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_items_file(new=False)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.saved_items_file), "r"
        )


def test_it_should_read_from_the_save_objectives_file():
    """Test to make sure it opens the objectives file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.get_objectives_file(new=False)
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.saved_objectives_file), "r"
        )


def test_it_should_load_the_game_map_file():
    """Test to make sure it can load the map file."""
    with patch.object(builtins, "open", mock_open(read_data="[]")):
        FileManager.load_art()
        builtins.open.assert_called_once_with(
            FileManager.join_base_path(FileManager.game_art_file), "r"
        )


def test_file_manager_game_map_handles_raises():
    """Test to make sure the game stories file handles exceptions."""
    with patch.object(builtins, "open", exception_on_open):
        with pytest.raises(SystemExit):
            FileManager.load_art()


def test_join_base_path():
    """Test to make sure the join_base_path method works."""
    with patch.object(os.path, "abspath", return_value="C:/test1/test2/test3"):
        assert FileManager.join_base_path("test") == "C:/test1/test"
