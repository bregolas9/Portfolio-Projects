"""Tests for the inventory service."""

from unittest.mock import MagicMock

from common.game_objective import GameObjective
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.item import Item
from common.player import Player
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.room import Room
from game_repository.game_repository import GameRepository
from game_repository.item_manager import ItemManager
from game_repository.objectives_manager import ObjectiveManager
from services.inventory_service import InventoryService
from tests.test_helpers import any_message_contents


def hammer(discovered: bool = False) -> Item:
    return Item(
        name="hammer",
        alias=["mallet"],
        description=["A tool used for smashing thumbs."],
        look_at_message={
            "line1": "It's got a heavy top and a wooden handle for smashing thumbs."
        },
        is_collectible=True,
        discovered=discovered,
        interactions={
            "use": {
                "message": ["You smash your thumb with the hammer. Ouch!"],
                "new_description": ["You smash your thumb with the hammer. Ouch!"],
            }
        },
    )


def shovel(usable: bool = False, collectible: bool = True) -> Item:
    return Item(
        name="shovel",
        alias=["spade"],
        description=["A tool used for digging holes."],
        look_at_message={
            "line1": "It's got a long handle and a flat metal blade for digging holes."
        },
        is_collectible=collectible,
        discovered=False,
        interactions={}
        if not usable
        else {
            "use": {
                "message": [
                    "You dig a hole in the floor. The owners are going to be mad."
                ],
                "new_description": [
                    "You dig a hole in the floor. The owners are going to be mad."
                ],
            }
        },
    )


def entry(contains_items: bool, use_shovel: bool = False) -> Room:
    return Room(
        name="entry",
        description={"test": "a test room"},
        inventory=[] if not contains_items else [hammer(), shovel(use_shovel)],
        exits=[],
        directional_exits={},
        aliases=["entry"],
        blockers=[],
        starting_inventory=[] if not contains_items else [hammer(), shovel(use_shovel)],
    )


def mock_repository(player_has_items: bool, room_has_items: bool) -> MagicMock:
    """Return a mock repository."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.inventory = [hammer(), shovel()] if player_has_items else []
    mock_repository.rooms = {
        "entry": entry(contains_items=room_has_items),
    }
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.items.items = [hammer(), shovel()]
    mock_repository.state_dirty = False
    return mock_repository


def test_it_should_get_inventory_contents_when_items_in_inventory():
    """Test to ensure the inventory service returns the inventory contents."""
    repository = mock_repository(player_has_items=True, room_has_items=False)
    inventory_service = InventoryService(repository)
    expected = [
        "Hammer - A tool used for smashing thumbs.",
        "Shovel - A tool used for digging holes.",
    ]
    actual = inventory_service.get_inventory_contents(repository.player)
    assert actual == expected


def test_it_should_get_inventory_contents_when_no_items_in_inventory():
    """Test to ensure the inventory service returns the inventory contents."""
    repository = mock_repository(player_has_items=False, room_has_items=True)
    inventory_service = InventoryService(repository)
    expected = []
    actual = inventory_service.get_inventory_contents(repository.player)
    assert actual == expected


def test_it_should_open_inventory():
    """Test the open_inventory method."""
    repository = mock_repository(player_has_items=True, room_has_items=False)
    inventory_service = InventoryService(repository)
    expected = [
        " - Hammer - A tool used for smashing thumbs.",
        " - Shovel - A tool used for digging holes.",
    ]
    actual = inventory_service.open_inventory(MagicMock)
    assert any_message_contents(actual.messages, expected[0])
    assert any_message_contents(actual.messages, expected[1])
    assert actual.status == RequestStatus.SUCCESS


def test_it_should_return_no_items_when_open_inventory_empty():
    """Test to make sure the open inventory method returns a message when the inventory is empty."""
    repository = mock_repository(player_has_items=False, room_has_items=False)
    inventory_service = InventoryService(repository)
    expected = "You have no items in your inventory."
    actual = inventory_service.open_inventory(MagicMock)
    assert any_message_contents(actual.messages, expected)
    assert actual.status == RequestStatus.SUCCESS


def test_take_validation_should_fail_when_item_not_in_room():
    """Test the take validation method."""
    repository = mock_repository(player_has_items=False, room_has_items=False)
    inventory_service = InventoryService(repository)
    expected = "Hmm, you can't seem to find that."
    actual = inventory_service.handle_pickup_validation(
        repository.player, entry(False), shovel()
    )
    assert actual is not None
    assert any_message_contents(actual.messages, expected)
    assert actual.status == RequestStatus.FAILURE


def test_pickup_validation_should_fail_when_item_in_player_inventory_already():
    """Test the pickup validation method for when the player already has the item

    and it's not in the room.
    """
    repository = mock_repository(player_has_items=True, room_has_items=False)
    inventory_service = InventoryService(repository)
    expected = "You already have that item in your inventory."
    actual = inventory_service.handle_pickup_validation(
        repository.player, repository.rooms["entry"], repository.player.inventory[0]
    )
    assert actual is not None
    assert any_message_contents(actual.messages, expected)
    assert actual.status == RequestStatus.FAILURE


def test_pickup_validation_should_fail_when_item_not_in_room_or_player_inventory():
    """Test the pickup validation method for when the player doesn't have the

    item and it's not in the room.
    """
    repository = mock_repository(player_has_items=False, room_has_items=False)
    inventory_service = InventoryService(repository)
    expected = "Hmm, you can't seem to find that."
    actual = inventory_service.handle_pickup_validation(
        repository.player, repository.rooms["entry"], shovel()
    )
    assert actual is not None
    assert any_message_contents(actual.messages, expected)
    assert actual.status == RequestStatus.FAILURE


def test_pick_up_method_should_fail_when_item_is_none():
    """Test the pick up method when the item is None."""
    repository = mock_repository(player_has_items=False, room_has_items=True)
    repository.items.get_item_by_name = MagicMock(return_value=None)
    inventory_service = InventoryService(repository)
    request = GameRequest(request_type=RequestType.TAKE, targets=[None])
    actual = inventory_service.pick_up(request)
    assert actual is not None
    assert any_message_contents(actual.messages, "Hmm, you can't seem to find that.")
    assert actual.status == RequestStatus.FAILURE


def test_it_should_not_pick_up_when_invalid():
    """Ensure the pick_up method fails when the validation result is failed."""
    repository = mock_repository(player_has_items=False, room_has_items=True)
    repository.get_item_by_name = MagicMock(return_value=shovel())
    inventory_service = InventoryService(repository)
    request = GameRequest(request_type=RequestType.TAKE, targets=["shovel"])
    response = GameResponse.failure("You already have that item in your inventory.")
    inventory_service.handle_pickup_validation = MagicMock(
        name="handle_pickup_validation",
        return_value=response,
    )
    actual = inventory_service.pick_up(request)
    assert actual is not None
    assert any_message_contents(
        actual.messages, "You already have that item in your inventory."
    )
    assert actual.status == RequestStatus.FAILURE


def test_it_should_pick_up_items():
    """Test to make sure the pick_up method succeeds on valid requests."""
    repository = mock_repository(player_has_items=False, room_has_items=True)
    repository.items.get_item_by_name = MagicMock(return_value=shovel())
    inventory_service = InventoryService(repository)
    request = GameRequest(request_type=RequestType.TAKE, targets=["shovel"])
    inventory_service.handle_pickup_validation = MagicMock(return_value=None)
    inventory_service.remove_item_from_room_and_add_to_player = MagicMock(
        return_value=None
    )
    response = inventory_service.pick_up(request)
    inventory_service.remove_item_from_room_and_add_to_player.assert_called_once()
    assert response is not None
    assert any_message_contents(
        response.messages, "You added an item to your inventory:"
    )


def test_item_removed_response_method():
    """Test the item removed moethod."""
    inventory_service = InventoryService(MagicMock())
    response = inventory_service.item_removed_response(shovel(), entry(True))
    assert response is not None
    assert any_message_contents(response.messages, "You dropped an item in entry:")
    assert any_message_contents(
        response.messages, f"{shovel().name.capitalize()} - {shovel().description}"
    )
    assert response.status == RequestStatus.SUCCESS


def test_remove_item_from_room_and_add_to_player():
    """Test the remove item from room and add to player method."""
    repository = mock_repository(player_has_items=False, room_has_items=True)
    inventory_service = InventoryService(repository)
    inventory_service.remove_item_from_room_and_add_to_player(
        repository.player,
        repository.rooms["entry"],
        repository.rooms["entry"].inventory[0],
    )
    assert len(repository.player.inventory) == 1
    assert len(repository.rooms["entry"].inventory) == 1
    assert repository.player.inventory[0].name == "hammer"


def test_it_should_remove_item_from_player_and_add_to_room():
    """Test to make sure the remote_item_from_player_and_add_to_room method works."""
    repository = mock_repository(player_has_items=True, room_has_items=False)
    inventory_service = InventoryService(repository)
    inventory_service.remove_item_from_player_and_add_to_room(
        repository.player,
        repository.rooms["entry"],
        repository.player.inventory[0],
    )
    assert len(repository.player.inventory) == 1
    assert len(repository.rooms["entry"].inventory) == 1
    assert repository.rooms["entry"].inventory[0].name == "hammer"


def test_item_not_in_player_inventory_response():
    """Test the item not in player inventory response method."""
    inventory_service = InventoryService(MagicMock())
    response = inventory_service.item_not_in_player_inventory_response
    assert response is not None
    assert any_message_contents(
        response.messages, "You don't have that item in your inventory."
    )
    assert response.status == RequestStatus.FAILURE


def test_item_not_collectible_response():
    """Test the item not collectible response message."""
    service = InventoryService(MagicMock())
    response = service.item_not_collectible_response
    assert response is not None
    assert any_message_contents(response.messages, "You can't pick that up.")
    assert response.status == RequestStatus.FAILURE


def test_item_already_in_room_response():
    """Test the item already in room response message."""
    service = InventoryService(MagicMock())
    response = service.item_already_in_room_response
    assert response is not None
    assert any_message_contents(response.messages, "That item is already in this room.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_handle_pickup_validation():
    """Test the handle_pickup_validation method."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    item = shovel()
    item.is_collectible = False
    repo.items = {"shovel": item}
    repo.rooms["entry"].inventory = [item]
    service = InventoryService(repo)
    response = service.handle_pickup_validation(repo.player, repo.rooms["entry"], item)
    assert response is not None
    assert any_message_contents(response.messages, "You can't pick that up.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_handle_pickup_validation_when_item_none():
    """Ensure handle_pickup_validation method fails when the item is None."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    service = InventoryService(repo)
    response = service.handle_pickup_validation(
        repo.player, repo.rooms["entry"], None  # type: ignore
    )
    assert response is not None
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_handle_drop_validation_when_none():
    """Test the handle_drop_validation method when the item is None."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    service = InventoryService(repo)
    response = service.handle_drop_validation(
        repo.player, repo.rooms["entry"], None  # type: ignore
    )
    assert response is not None
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_handle_drop_validation_when_item_not_in_room():
    """Test the handle_drop_validation method when the item is not in the room."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    item = shovel()
    repo.items = {"shovel": item}
    repo.rooms["entry"].inventory = [item]
    service = InventoryService(repo)
    response = service.handle_drop_validation(repo.player, repo.rooms["entry"], item)
    assert response is not None
    assert any_message_contents(
        response.messages, "You don't have that item in your inventory."
    )
    assert response.status == RequestStatus.FAILURE


def test_it_should_handle_drop_validation_when_item_not_in_player_inventory():
    """Test the handle_drop_validation method when the item is in the room."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    item = shovel()
    repo.items = {"shovel": item}
    repo.rooms["entry"].inventory = [item]
    repo.player.inventory = [item]
    service = InventoryService(repo)
    response = service.handle_drop_validation(repo.player, repo.rooms["entry"], item)
    assert response is not None
    assert any_message_contents(response.messages, "That item is already in this room.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_drop_item():
    """Test the drop_item method."""
    repo = mock_repository(player_has_items=True, room_has_items=False)
    hammer = repo.player.inventory[0]
    repo.items.get_item_by_name = MagicMock(return_value=hammer)
    repo.current_location = repo.rooms["entry"]
    service = InventoryService(repo)
    response = service.drop(GameRequest(RequestType.DROP, hammer.name))
    assert response is not None
    assert any_message_contents(response.messages, "You dropped an item in entry:")
    assert any_message_contents(
        response.messages, f"{hammer.name.capitalize()} - {hammer.description}"
    )
    assert response.status == RequestStatus.SUCCESS


def test_drop_should_return_not_found_response():
    """Make sure the drop method returns the not found response when the item

    is empty or None.
    """
    repo = mock_repository(player_has_items=True, room_has_items=False)
    repo.items.get_item_by_name = MagicMock(return_value=None)
    service = InventoryService(repo)
    response = service.drop(GameRequest(RequestType.DROP, [None]))
    assert response is not None
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_return_invalid_validation_results():
    """Test to make sure drop method returns validation results when invalid."""
    repo = mock_repository(player_has_items=True, room_has_items=False)
    hammer = repo.player.inventory[0]
    room = repo.rooms["entry"]
    repo.items.get_item_by_name = MagicMock(return_value=hammer)
    repo.current_location = MagicMock(return_value=room)
    validation_result = GameResponse.failure("Invalid")
    service = InventoryService(repo)
    service.handle_drop_validation = MagicMock(
        name="handle_drop_validation", return_value=validation_result
    )
    response = service.drop(GameRequest(RequestType.DROP, hammer.name))
    assert response is not None
    assert any_message_contents(response.messages, "Invalid")
    assert response.status == RequestStatus.FAILURE


def test_it_should_look_at_items():
    """Test to make sure you can look at items."""
    repo = mock_repository(player_has_items=True, room_has_items=False)
    repo.objectives = MagicMock(ObjectiveManager)
    the_hammer = hammer()
    repo.player.inventory = [the_hammer]
    repo.items.get_item_by_name = MagicMock(return_value=the_hammer)
    repo.current_location = repo.rooms["entry"]
    service = InventoryService(repo)
    response = service.look_at(GameRequest(RequestType.LOOK, ["hammer"]))
    assert response is not None
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(
        response.messages,
        "It's got a heavy top and a wooden handle for smashing thumbs.",
    )


def test_it_should_not_look_at_invalid_items():
    """Test to make sure you can't look at items that don't exist."""
    repo = mock_repository(player_has_items=True, room_has_items=False)
    repo.player.inventory = []
    repo.items.get_item_by_name = MagicMock(return_value=None)
    repo.current_location = repo.rooms["entry"]
    service = InventoryService(repo)
    response = service.look_at(GameRequest(RequestType.LOOK, ["hammer"]))
    assert response is not None
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")


def test_it_should_not_look_at_items_not_in_player_inventory_or_room():
    """Test to make sure you can't look at items outside the room or inventory."""
    repo = mock_repository(player_has_items=False, room_has_items=False)
    repo.player.inventory = []
    repo.items.get_item_by_name = MagicMock(return_value=shovel())
    repo.current_location = repo.rooms["entry"]
    service = InventoryService(repo)
    response = service.look_at(GameRequest(RequestType.LOOK, ["shovel"]))
    assert response is not None
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")


def test_should_add_look_at_line_method():
    """Test to make sure that if an item is not found,
    the should_add_look_at_line method returns True."""
    repo = mock_repository(player_has_items=True, room_has_items=False)
    repo.player.inventory = []
    repo.items.get_item_by_name = MagicMock(return_value=None)
    repo.current_location = repo.rooms["entry"]
    service = InventoryService(repo)
    assert service.should_add_look_at_line("hammer")


def test_pick_up_should_fail_when_request_targets_empty():
    """Pick up method should return not found response when targets list empty."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    repo.items.get_item_by_name = MagicMock(return_value=None)
    service = InventoryService(repo)
    response = service.pick_up(GameRequest(RequestType.TAKE, []))
    assert response is not None
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")
    assert response.status == RequestStatus.FAILURE


def test_drop_should_fail_when_request_targets_empty():
    """Drop method should return not found response when targets list empty."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    repo.items.get_item_by_name = MagicMock(return_value=None)
    service = InventoryService(repo)
    response = service.drop(GameRequest(RequestType.DROP, []))
    assert response is not None
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")
    assert response.status == RequestStatus.FAILURE


def test_inspect_should_fail_when_request_targets_empty():
    """Inspect method should return not found response when targets list empty."""
    repo = mock_repository(player_has_items=False, room_has_items=True)
    repo.items.get_item_by_name = MagicMock(return_value=None)
    service = InventoryService(repo)
    response = service.look_at(GameRequest(RequestType.INSPECT, []))
    assert response is not None
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")
    assert response.status == RequestStatus.FAILURE


def test_if_it_should_strike_messages():
    """Test to make sure it should strike a message."""
    objective = MagicMock(GameObjective)
    objective.name = "test"
    objective.is_complete = MagicMock(return_value=True)
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.get_objective_by_name = MagicMock(return_value=objective)
    repo.player = MagicMock(Player)
    service = InventoryService(repo)
    assert service.should_strike_message("test")
    objective.is_complete = MagicMock(return_value=False)
    repo.objectives.get_objective_by_name = MagicMock(return_value=objective)
    assert not service.should_strike_message("test")


def test_it_should_strike_missing_objectives():
    """Test to make sure that things which aren't objectives don't get stricken."""
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.get_objective_by_name = MagicMock(return_value=None)
    repo.player = MagicMock(Player)
    service = InventoryService(repo)
    assert not service.should_strike_message("test")
