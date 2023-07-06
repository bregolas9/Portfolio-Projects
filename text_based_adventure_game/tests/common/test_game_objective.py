"""Test the game objective class."""

from unittest.mock import MagicMock

from common.game_objective import GameObjective
from common.item import Item
from common.player import Player
from common.room import Room


def test_it_should_return_repr():
    """Test it should return repr."""
    objective = GameObjective("test", ["test"], ["test"], [{"test": "test"}])
    assert repr(objective) == "test, ['test'], ['test'], [{'test': 'test'}]"


def test_it_should_be_incomplete_when_not_all_requirements_met():
    """Test it should be incomplete when not all requirements met."""
    player = MagicMock(Player)
    player.inventory = []
    room = MagicMock(Room)
    player.location = room
    objective = GameObjective("test", [], ["test"], [])
    objective.in_player_inventory = MagicMock(return_value=False)
    objective.in_room_inventory = MagicMock(return_value=False)
    assert objective.is_complete(player) is False


def test_it_should_be_incomplete_when_interactions_not_met():
    """Make sure it fails when interactions are not met."""
    player = MagicMock(Player)
    player.inventory = []
    room = MagicMock(Room)
    player.location = room
    objective = GameObjective(
        "test",
        [],
        ["test"],
        [{"interaction_type": "use", "item": "flashlight", "complete": False}],
    )
    objective.in_player_inventory = MagicMock(return_value=True)
    objective.in_room_inventory = MagicMock(return_value=True)
    assert not objective.is_complete(player)


def test_it_should_be_complete_when_valid():
    """Make sure it passes when requirements and interactions are complete."""
    player = MagicMock(Player)
    player.inventory = []
    room = MagicMock(Room)
    player.location = room
    objective = GameObjective(
        "test",
        [],
        ["test"],
        [{"interaction_type": "use", "item": "flashlight", "complete": True}],
    )
    objective.in_player_inventory = MagicMock(return_value=True)
    objective.in_room_inventory = MagicMock(return_value=True)
    assert objective.is_complete(player)


def test_complete_interaction_objective():
    """Make sure it updates an interaction when complete."""
    objective = GameObjective(
        "test",
        [],
        [],
        [{"interaction_type": "use", "item": "flashlight", "complete": False}],
    )
    objective.complete_interaction_objective("flashlight", "use")
    assert objective.interactions[0]["complete"] is True


def test_in_room_inventory():
    """Make sure it checks if an item is in the room inventory."""
    room = MagicMock(Room)
    item = MagicMock(Item)
    item.name = "flashlight"
    item.is_collectible = False
    room.inventory = [item]
    assert GameObjective.in_room_inventory(room, "flashlight") is True


def test_it_can_increment_hint_count():
    objective = GameObjective("test", ["test"], ["test"], [{"test": "test"}])
    assert objective.hint_count == 0
    objective.increment_hint_count()
    assert objective.hint_count == 1


def test_for_list_of_hints():
    objective = GameObjective(
        "test", ["test1", "test2", "test3"], ["test"], [{"test": "test"}]
    )
    assert objective.hints == []
    objective.increment_hint_count()
    assert objective.hints == ["test1"]
    objective.increment_hint_count()
    assert objective.hints == ["test1", "test2"]
    objective.increment_hint_count()
    assert objective.hints == ["test1", "test2", "test3"]
    objective.increment_hint_count()
    assert objective.hints == ["test1", "test2", "test3"]
