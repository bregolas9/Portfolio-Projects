"""Test the item manager class."""

import builtins
from unittest.mock import MagicMock, patch

from common.item import Item
from common.load_error import FileOperationError
from common.player import Player
from common.room import Room
from game_repository.file_manager import FileManager
from game_repository.item_manager import ItemManager


def mock_item_helper(include_alias: bool = True):
    """Mock item data for testing."""
    return {
        "test": Item(
            name="something else" if include_alias else "test",
            alias=["test"] if include_alias else [],
            description=["test"],
            look_at_message={"description1": "test"},
            is_collectible=True,
            discovered=False,
            interactions={},
        )
    }


def mock_item_json():
    """Mock json data as an item."""
    return [
        {
            "name": "test",
            "alias": ["test"],
            "description": ["test"],
            "look_at_message": ["test"],
            "is_collectible": True,
            "discovered": False,
            "interactions": {},
        }
    ]


def test_it_should_load_items():
    """Test to make sure it loads items from file."""
    items = mock_item_json()
    with patch.object(FileManager, "get_items_file", return_value=items):
        manager = ItemManager()
        manager.load_items(True)
        test_item = manager.items["test"]
        assert test_item.name == "test"
        assert test_item.alias == ["test"]
        assert test_item.description == "test"
        assert test_item.look_at_message == ["test"]
        assert test_item.is_collectible is True
        assert test_item.discovered is False
        assert isinstance(test_item.interactions, dict)


def test_it_should_not_load_items_when_file_operation_error():
    """Test to make sure it does not load items when it receives a file operation error."""
    with patch.object(
        FileManager, "get_items_file", return_value=FileOperationError("a message")
    ):
        manager = ItemManager()
        result = manager.load_items(True)
        assert isinstance(result, FileOperationError)
        assert result.message == "a message"
        assert manager.items == {}


def test_it_should_get_item_by_name():
    """Test to make sure it gets item by name or alias"""
    items = mock_item_helper(True)
    manager = ItemManager()
    manager.items = items
    response = manager.get_item_by_name("test")
    assert response is not None
    assert response == items.get("test")

    items = mock_item_helper(False)
    manager.items = items
    response = manager.get_item_by_name("test")
    assert response is not None
    assert response == items.get("test")


def test_it_should_get_item_by_name_by_room():
    """Test for getting an item by name or alias based on inventory or room inventory"""
    items = mock_item_helper(True)
    inventory = [items.get("test")]
    player = MagicMock(Player)
    player.inventory = inventory
    manager = ItemManager()
    response = manager.get_item_by_name_by_room("test", player)
    assert response is not None
    assert response == inventory[0]

    player.inventory = []
    player.location = MagicMock(Room)
    player.location.inventory = inventory
    response = manager.get_item_by_name_by_room("test", player)
    assert response is not None
    assert response == inventory[0]

    items = mock_item_helper(False)
    inventory = [items.get("test")]
    player.inventory = inventory
    response = manager.get_item_by_name_by_room("test", player)
    assert response is not None
    assert response == inventory[0]

    player.inventory = []
    player.location = MagicMock(Room)
    player.location.inventory = inventory
    response = manager.get_item_by_name_by_room("test", player)
    assert response is not None
    assert response == inventory[0]

    response = manager.get_item_by_name_by_room("something else", player)
    assert response is None


def test_get_list_of_items():
    items = mock_item_helper()
    item = items.get("test")
    item_names = ["test"]
    manager = ItemManager()
    manager.get_item_by_name = MagicMock(return_value=item)
    response = manager.get_list_of_items(item_names)
    assert len(response) == 1
    assert response[0] == item
