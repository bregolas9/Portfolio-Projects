"""Test the room class."""

from common.item import Item
from common.room import Room


def get_mock_room():
    """Return a mock room for testing."""
    item = Item(
        name="Test Item",
        alias=["Test Alias"],
        description=["Test Description"],
        look_at_message={"line1": "Test Look At Message"},
        is_collectible=True,
        discovered=False,
        interactions={},
    )
    return Room(
        name="Test Room",
        description={
            "default": "Test Description.",
            "Test Item": "Test description for the item.",
        },
        inventory=[item],
        starting_inventory=[item],
        exits=[],
        directional_exits={},
        aliases=[],
        blockers=[],
    )


def test_it_should_get_inventory_item_names():
    """It should get inventory item names."""
    assert get_mock_room().inventory_item_names == ["Test Item"]


def test_it_should_get_starting_inventory_item_by_name():
    """Test to make sure it can get a starting inventory item by name."""
    item = get_mock_room().get_starting_inventory_item_by_name("Test Item")
    assert item is not None
    assert item.name == "Test Item"


def test_it_should_get_room_description_with_item_description():
    """It should get an item description."""
    room = get_mock_room()
    assert room.description == "Test Description. Test description for the item. "
