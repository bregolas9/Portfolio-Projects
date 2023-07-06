"""Test the interaction service."""


from typing import Any
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
from services.interaction_service import InteractionService
from tests.test_helpers import any_message_contents


def test_it_should_use_single():
    """Test to make sure the use method works for a single target."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    repo.items.get_item_by_name.return_value = item
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Success")
    interaction_mock = MagicMock(return_value=return_value)
    interaction_service.handle_single_interaction = interaction_mock
    response = interaction_service.use(GameRequest(RequestType.USE, ["item"]))
    assert response == return_value
    interaction_service.handle_single_interaction.assert_called_once_with(item, "use")


def test_is_discovered_should_work():
    """Test the is_discovered method."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    item = MagicMock(Item)
    item.discovered = True
    item.is_collectible = True
    assert interaction_service.is_discovered(item)
    item.discovered = False
    assert not interaction_service.is_discovered(item)


def test_is_discovered_should_handle_none_items():
    """Test to make sure the is_discovered method handles None items."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    assert not interaction_service.is_discovered(None)


def test_is_discovered_when_not_collectible():
    """Test to make sure the is_discovered method handles non-collectible items."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    item = MagicMock(Item)
    item.discovered = False
    item.is_collectible = False
    assert interaction_service.is_discovered(item)


def test_is_nearby_function_returns_true_when_in_player_inventory():
    """Test to make sure the is_nearby function returns true when the item is in
    the player's inventory."""
    repo = MagicMock(GameRepository)
    mock_item = MagicMock(Item)
    repo.player = MagicMock(Player)
    repo.player.inventory = [mock_item]
    repo.current_location.inventory = []
    interaction_service = InteractionService(repo)
    assert interaction_service.is_nearby(mock_item)


def test_is_nearby_function_returns_true_when_in_current_location():
    """Test to make sure the is_nearby function returns true when the item is in
    the current location."""
    repo = MagicMock(GameRepository)
    mock_item = MagicMock(Item)
    repo.player = MagicMock(Player)
    repo.player.inventory = []
    repo.current_location.inventory = [mock_item]
    interaction_service = InteractionService(repo)
    assert interaction_service.is_nearby(mock_item)


def test_is_nearby_function_returns_false_when_item_is_none():
    """Test to make sure the is_nearby function returns false when the item is None."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    assert not interaction_service.is_nearby(None)


def test_try_picking_it_up_response():
    """Test the try_picking_it_up_response method."""
    repo = MagicMock(GameRepository)
    item = MagicMock(Item)
    item.name = "Test Item"
    action = "use"
    interaction_service = InteractionService(repo)
    response = interaction_service.try_picking_it_up_response(item, action)
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item.name} but it's too far away. "
        + "Try picking it up first.",
    )


def test_default_single_interaction_response_method():
    """Test the default_single_interaction_response method."""
    repo = MagicMock(GameRepository)
    item = MagicMock(Item)
    item.name = "Test Item"
    action = "use"
    interaction_service = InteractionService(repo)
    response = interaction_service.item_default_single_interaction_response(
        item, action
    )
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item.name} but nothing interesting happens.",
    )


def test_item_not_found_resposne():
    """Test the item_not_found_response method."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    response = interaction_service.item_not_found_response
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")


def test_get_iteraction_message_response():
    """Test the get_interaction_message_response method."""
    repo = MagicMock(GameRepository)
    item = MagicMock(Item)
    item.interactions = {"test": {"message": "Test Message"}}
    interaction_service = InteractionService(repo)
    response = interaction_service.get_interaction_message_response(item, "test")
    assert any_message_contents(response.messages, "Test Message")


def test_get_iteraction_message_response_when_no_interaction():
    """Test the get_interaction_message_response method."""
    repo = MagicMock(GameRepository)
    item = MagicMock(Item)
    item.interactions = {}
    item.name = "Test Item"
    interaction_service = InteractionService(repo)
    response = interaction_service.get_interaction_message_response(item, "test")
    assert any_message_contents(
        response.messages,
        "You try to test the Test Item but nothing interesting happens.",
    )


def test_update_interaction_description():
    """Test the update_interaction_description method."""
    repo = MagicMock(GameRepository)
    item = MagicMock(Item)
    item.description = "Starting description."
    item.interactions = {
        "test": {"message": "Test Message", "new_description": "New Message"}
    }
    interaction_service = InteractionService(repo)
    interaction_service.update_interaction_description(item, "test")
    assert item.description == "New Message"
    item.description = "Starting description."
    item.interactions = {"test": {"message": "Test Message"}}
    interaction_service.update_interaction_description(item, "test")
    assert item.description == "Starting description."
    item.interactions = {}
    interaction_service.update_interaction_description(item, "test")
    assert item.description == "Starting description."


def test_interact_single_item_when_interaction_none():
    """Test a single interaction when the interaction is not defined in the template."""
    repo = MagicMock(GameRepository)
    item = MagicMock(Item)
    item.name = "Test Item"
    action = "test"
    item.interactions = {}
    interaction_service = InteractionService(repo)
    response = interaction_service.interact_single_item(item, action)
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item.name} but nothing interesting happens.",
    )


def test_interact_single_item_when_interaction_defined():
    """Test a single interaction when the interaction is defined in the template."""
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    action = "test"
    item.interactions = {
        "test": {"message": "Test Message", "new_description": "New Message"}
    }
    interaction_service = InteractionService(repo)
    interaction_service.update_interaction_description = MagicMock()
    interaction_service.handle_interaction_transformations = MagicMock()
    response = interaction_service.interact_single_item(item, action)
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.update_interaction_description.assert_called_once()
    interaction_service.handle_interaction_transformations.assert_called_once()


def test_pull_method():
    """Test to make sure the pull method works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"pull": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.pull(GameRequest(RequestType.PULL, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_chew_method():
    """Test to make sure the chew method works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"chew": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.chew(GameRequest(RequestType.CHEW, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_has_missing_items_should_be_true_when_none():
    """Test the has_missing_items method when a list of items contains a None."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    assert interaction_service.has_missing_items([None])


def test_has_missing_items_should_be_true_when_not_nearby():
    """Test the has_missing_items method when a list of items contains an item
    that is not nearby."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=False)
    item = MagicMock(Item)
    item.name = "Test Item"
    assert interaction_service.has_missing_items([item])


def test_has_missing_items_should_be_true_when_not_discovered():
    """Test the has_missing_items method when a list of items contains an item
    that is not discovered."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.discovered = False
    item.is_collectible = True
    assert interaction_service.has_missing_items([item])


def test_get_interaction_requirements_should_return_list_of_items():
    """Test to make sure a list of items is returned when the interaction
    requirements are met."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.interactions = {"test": {"requires": ["Test Item"]}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    assert interaction_service.get_interaction_requirements(item, "test") == [item]


def test_get_interaction_requirements_returns_empty_list_when_interaction_none():
    """Test to make sure an empty list is returned when the interaction
    requirements are not set."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.interactions = {}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    assert interaction_service.get_interaction_requirements(item, "test") == []


def test_get_interaction_requirements_returns_empty_list_when_requires_none():
    """Test to make sure an empty list is returned when the interaction is not none
    but the requires is not set."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.interactions = {"use": {}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    assert interaction_service.get_interaction_requirements(item, "use") == []


def test_get_transformations_returns_empty_list_when_interaction_none():
    """Test to make sure an empty list is returned when the interaction
    transformations are not set."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.interactions = {}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    assert interaction_service.get_transformations(item, "test") == []


def test_get_transformations_returns_transformations():
    """Test to make sure a list of transformations is returned when the interaction
    transformations are set."""

    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {
        "test": {"transforms": [{"from": "Test Item", "to": "Test Item 2"}]}
    }
    interaction_service = InteractionService(repo)
    assert interaction_service.get_transformations(item, "test") == [
        {"from": "Test Item", "to": "Test Item 2"}
    ]


def test_can_handle_single_interaction_when_not_nearby():
    """Test the handle_single_interaction method when item is not nearby."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=False)
    item = MagicMock(Item)
    item.name = "Test Item"
    response = interaction_service.handle_single_interaction(item, "test")
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")


def test_can_handle_single_interaction_when_item_none():
    """Test the handle_single_interaction method when item is None."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    response = interaction_service.handle_single_interaction(None, "test")
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")


def test_can_handle_single_interaction_when_not_discovered():
    """Test the handle_single_interaction method when item is not discovered."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.discovered = False
    item.is_collectible = True
    action = "test"
    response = interaction_service.handle_single_interaction(item, "test")
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item.name} but it's too far away. "
        + "Try picking it up first.",
    )


def test_can_handle_single_interaction_when_cant_handle_it():
    """Test to make sure the handle_single_interaction method returns a message
    when the interaction can't be handled."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.discovered = True
    item.is_collectible = True
    action = "test"
    interaction_service.can_interact_single_item = MagicMock(return_value=False)
    response = interaction_service.handle_single_interaction(item, "test")
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item.name} but nothing interesting happens.",
    )


def test_can_handle_single_interaction_when_valid():
    """Test to make sure that the interact_single_item method is called when valid."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.discovered = True
    item.is_collectible = True
    action = "test"
    interaction_service.can_interact_single_item = MagicMock(return_value=True)
    return_value = GameResponse.success("Success")
    interaction_service.interact_single_item = MagicMock(return_value=return_value)
    response = interaction_service.handle_single_interaction(item, action)
    assert response is not None
    assert response == return_value


def test_can_interact_single_item_returns_false_when_item_none():
    """Test the can_interact_single_item method when item is None."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    assert not interaction_service.can_interact_single_item(None, "test")


def test_can_interact_single_item_returns_false_when_not_nearby():
    """Test the can_interact_single_item method when item is not nearby."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=False)
    item = MagicMock(Item)
    item.name = "Test Item"
    assert not interaction_service.can_interact_single_item(item, "test")


def test_can_interact_single_item_returns_false_when_interactions_missing():
    """test the can_interact_single_item method when item interactions are missing."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {}
    assert not interaction_service.can_interact_single_item(item, "test")


def test_can_interact_single_item_returns_false_when_requirements_missing():
    """Test the can_interact_single_item method when item requirements are missing."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.is_collectible = False
    item.name = "Test Item"
    item.discovered = True
    interaction_service.get_interaction_requirements = MagicMock(return_value=[None])
    item.interactions = {"test": {"requires": ["missing item"]}}
    assert not interaction_service.can_interact_single_item(item, "test")


def test_can_interact_single_item_returns_false_when_not_discovered():
    """Test the can_interact_single_item method when item is not discovered."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.player.inventory = []
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"test": {"requires": ["missing item"]}}
    required_item = MagicMock(Item)
    required_item.name = "Missing Item"
    required_item.is_collectible = True
    required_item.discovered = True
    interaction_service.get_interaction_requirements = MagicMock(
        return_value=[required_item]
    )
    item.discovered = False
    item.is_collectible = True
    assert not interaction_service.can_interact_single_item(item, "test")


def test_can_interact_multiple_item_returns_false_when_not_discovered():
    """Test the can_interact_multiple_item method when item is not discovered."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.player.inventory = []
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"test": {"requires": ["missing item"]}}
    required_item = MagicMock(Item)
    required_item.name = "Missing Item"
    required_item.is_collectible = True
    required_item.discovered = True
    interaction_service.get_interaction_requirements = MagicMock(
        return_value=[required_item]
    )
    item.discovered = False
    item.is_collectible = True
    assert not interaction_service.can_interact_multiple_items([item], "test")


def test_handle_interaction_transformations_should_transform_items():
    """Test to make sure the handle_interaction_transformations method transforms
    items when it should."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    repo.player = MagicMock(Player)
    repo.player.inventory = MagicMock
    interaction_service = InteractionService(repo)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.discovered = True
    item.is_collectible = True
    item.interactions = {
        "test": {"transforms": {"from": "Test Item", "to": "Transformed Item"}}
    }
    transformed_item = MagicMock(Item)
    transformed_item.name = "Transformed Item"
    transformed_item.discovered = True
    transformed_item.is_collectible = True
    interaction_service.get_transformations = MagicMock(
        return_value=[item.interactions["test"]["transforms"]]
    )
    interaction_service.transform_item = MagicMock()
    interaction_service.handle_interaction_transformations(item, "test")
    interaction_service.transform_item.assert_called_once_with(
        "Test Item", "Transformed Item"
    )


def test_transform_item_does_nothing_when_both_items_none():
    """Make sure the transform_item method does nothing when both items are None."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.items = MagicMock(ItemManager)
    repo.player.inventory = []
    repo.current_location = MagicMock(Room)
    repo.current_location.inventory = []
    repo.items.get_item_by_name = MagicMock(return_value=None)
    interaction_service = InteractionService(repo)
    interaction_service.transform_item("from", "to")
    assert repo.player.inventory == []
    assert repo.current_location.inventory == []


def test_transform_item_removes_item_from_player_when_to_is_none():
    """Test to make sure the transform_item method removes the item from the player when
    the to item is None."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.items = MagicMock(ItemManager)
    from_item = MagicMock(Item)
    from_item.name = "From Item"
    repo.player.inventory = [from_item]
    repo.current_location = MagicMock(Room)
    repo.current_location.inventory = []

    def mock_item_by_name(name):
        if name == "From Item":
            return from_item
        return None

    repo.items.get_item_by_name = mock_item_by_name
    interaction_service = InteractionService(repo)
    interaction_service.transform_item("From Item", None)
    assert repo.player.inventory == []
    assert repo.current_location.inventory == []


def test_transform_item_removes_item_from_room_inventory_when_to_is_none():
    """Test to make sure the transform_item method removes the item from the room
    inventory when the to item is None."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.items = MagicMock(ItemManager)
    from_item = MagicMock(Item)
    from_item.name = "From Item"
    repo.player.inventory = []
    repo.current_location = MagicMock(Room)
    repo.current_location.inventory = [from_item]

    def mock_item_by_name(name):
        if name == "From Item":
            return from_item
        return None

    repo.items.get_item_by_name = mock_item_by_name
    interaction_service = InteractionService(repo)
    interaction_service.transform_item("From Item", None)
    assert repo.player.inventory == []
    assert repo.current_location.inventory == []


def test_transform_item_adds_item_to_player_inventory_when_from_none():
    """Test to make sure the transform_item method adds the item to the player when
    the from item is None."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.items = MagicMock(ItemManager)
    to_item = MagicMock(Item)
    to_item.name = "To Item"
    repo.player.inventory = []
    repo.current_location = MagicMock(Room)
    repo.current_location.inventory = []

    def mock_item_by_name(name):
        if name == "To Item":
            return to_item
        return None

    repo.items.get_item_by_name = mock_item_by_name
    interaction_service = InteractionService(repo)
    interaction_service.transform_item("From Item", "To Item")
    assert repo.player.inventory == [to_item]
    assert repo.current_location.inventory == []


def test_transform_item_adds_to_item_to_player_and_removes_from_item_from_player():
    """Test to make sure the transform_item method adds the to item to the player and
    removes the from item from the player."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.items = MagicMock(ItemManager)
    from_item = MagicMock(Item)
    from_item.name = "From Item"
    to_item = MagicMock(Item)
    to_item.name = "To Item"
    repo.player.inventory = [from_item]
    repo.current_location = MagicMock(Room)
    repo.current_location.inventory = []

    def mock_item_by_name(name):
        if name == "From Item":
            return from_item
        else:
            return to_item

    repo.items.get_item_by_name = mock_item_by_name
    interaction_service = InteractionService(repo)
    interaction_service.transform_item("From Item", "To Item")
    assert repo.player.inventory == [to_item]
    assert repo.current_location.inventory == []


def test_transform_item_adds_to_item_to_player_and_removes_from_item_from_room():
    """Test to make sure the transform_item method adds the to item to the player and
    removes the from item from the room."""
    repo = MagicMock(GameRepository)
    repo.player = MagicMock(Player)
    repo.items = MagicMock(ItemManager)
    from_item = MagicMock(Item)
    from_item.name = "From Item"
    to_item = MagicMock(Item)
    to_item.name = "To Item"
    repo.player.inventory = []
    repo.current_location = MagicMock(Room)
    repo.current_location.inventory = [from_item]

    def mock_item_by_name(name):
        if name == "From Item":
            return from_item
        else:
            return to_item

    repo.items.get_item_by_name = mock_item_by_name
    interaction_service = InteractionService(repo)
    interaction_service.transform_item("From Item", "To Item")
    assert repo.player.inventory == [to_item]
    assert repo.current_location.inventory == []


def test_try_naming_the_item_response():
    """The try_naming_the_item_response method should return the correct response."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    response = interaction_service.try_naming_the_item_response
    assert any_message_contents(
        response.messages, "You aren't sure what to do, try naming the item."
    )


def test_default_multiple_interaction_response_reroutes_single_action():
    """Redirect to default single item response when only one item passed in."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    item = MagicMock(Item)
    item.name = "test item"
    action = "use"
    response = interaction_service.item_default_multiple_interaction_response(
        [item], action
    )
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item.name} but nothing interesting happens.",
    )


def test_default_multiple_interaction_response_with_multiple_items():
    """Default multiple item response should work correctly."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    item1 = MagicMock(Item)
    item1.name = "test item 1"
    item2 = MagicMock(Item)
    item2.name = "test item 2"
    action = "use"
    response = interaction_service.item_default_multiple_interaction_response(
        [item1, item2], action
    )
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        f"You try to {action} the {item1.name} with the {item2.name} "
        + "but nothing interesting happens.",
    )


def test_chew_should_not_find_empty_lists():
    """Chew method should return not found when request.targets is empty."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.CHEW, [])
    response = interaction_service.chew(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_pull_should_not_find_empty_lists():
    """Pull method should return not found when request.targets is empty."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.PULL, [])
    response = interaction_service.pull(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_use_method_should_fail_with_empty_targets():
    """The use interaction should fail when request.targets is empty."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.USE, [])
    response = interaction_service.use(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "You aren't sure what to do, try naming the item.",
    )


def test_use_calls_multiple_interaction_when_multiple_targets():
    """Use should call the handle_multiple_interaction method with multiple targets."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    items = [MagicMock(Item), MagicMock(Item)]
    items[0].name = "test item 1"
    items[1].name = "test item 2"

    def mock_item_by_name(name: str):
        if name == "test item 1":
            return items[0]
        else:
            return items[1]

    repo.items.get_item_by_name = mock_item_by_name
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.USE, ["test item 1", "test item 2"])
    interaction_service.handle_multiple_interaction = MagicMock()
    interaction_service.use(request)
    interaction_service.handle_multiple_interaction.assert_called_once_with(
        items, "use_with"
    )


def test_can_interact_multiple_items_fails_when_an_item_is_none():
    """Method should fail when an item is None."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    assert not interaction_service.can_interact_multiple_items([None], "use_with")


def test_can_interact_multiple_items_fails_when_item_not_nearby():
    """Method should fail when items are not nearby."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=False)
    item = MagicMock(Item)
    assert not interaction_service.can_interact_multiple_items([item], "use_with")


def test_can_interact_multiple_items_fails_when_interaction_not_defined():
    """Method should fail when item interaction is not defined."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    item = MagicMock(Item)
    item.interactions = {}
    assert not interaction_service.can_interact_multiple_items([item], "use_with")


def test_can_interact_multiple_items_fails_when_missing_requirements():
    """Method should fail when item interaction is missing requirements."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    interaction_service.is_nearby = MagicMock(return_value=True)
    interaction_service.get_interaction_requirements = MagicMock(return_value=[None])
    item = MagicMock(Item)
    item.is_collectible = False
    item.interactions = {"use_with": {"requires": []}}
    assert not interaction_service.can_interact_multiple_items([item], "use_with")


def test_can_interact_multiple_item_passes_when_valid():
    """Method should pass when all requirements are met."""
    repo = MagicMock(GameRepository)
    items: Any = [MagicMock(Item), MagicMock(Item)]
    items[0].name = "test item 1"
    items[1].name = "test item 2"
    items[0].is_collectible = False
    items[1].is_collectible = False
    items[0].interactions = {"use_with": {"requires": ["test item 2"]}}
    items[1].interactions = {"use_with": {"requires": ["test item 1"]}}
    service = InteractionService(repo)
    service.has_missing_items = MagicMock(return_value=False)
    service.is_nearby = MagicMock(return_value=True)
    service.get_interaction_requirements = MagicMock(return_value=items)
    assert service.can_interact_multiple_items(items, "use_with")


def test_interact_multiple_items_should_fail_when_interaction_not_defined():
    """Method should fail when item interaction is not defined."""
    repo = MagicMock(GameRepository)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item2 = MagicMock(Item)
    item1.interactions = {}
    item2.interactions = {}
    service.item_default_multiple_interaction_response = MagicMock()
    service.interact_multiple_items([item1, item2], "use_with")
    service.item_default_multiple_interaction_response.assert_called_once()


def test_interact_multiple_items_should_pass_when_valid():
    """Method should pass when all requirements are met."""
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.get_objective_by_name = MagicMock(return_value=None)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item2 = MagicMock(Item)
    service.update_interaction_description = MagicMock()
    response = GameResponse.success("success")
    service.get_interaction_message_response = MagicMock(return_value=response)
    item1.interactions = {"use_with": {"requires": ["test item 2"]}}
    item2.interactions = {"use_with": {"requires": ["test item 1"]}}
    service.handle_interaction_transformations = MagicMock()
    actual = service.interact_multiple_items([item1, item2], "use_with")
    service.update_interaction_description.assert_called()
    service.handle_interaction_transformations.assert_called()
    service.get_interaction_message_response.assert_called_once_with(item1, "use_with")
    assert any_message_contents(actual.messages, "success")


def test_handle_multiple_interaction_should_fail_when_any_item_is_none():
    """Method should fail when any item is None."""
    repo = MagicMock(GameRepository)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item2 = None
    response = service.handle_multiple_interaction([item1, item2], "use_with")
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "You aren't sure what to do, try naming the item."
    )


def test_handle_multiple_interaction_should_fail_when_any_item_is_not_nearby():
    """Method should fail when any item is not nearby."""
    repo = MagicMock(GameRepository)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item2 = MagicMock(Item)
    service.is_nearby = MagicMock(return_value=False)
    response = service.handle_multiple_interaction([item1, item2], "use_with")
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(response.messages, "Hmm, you can't seem to find that.")


def test_handle_mutliple_interaction_should_fail_when_any_item_not_discovered():
    """Method should fail when any item is not discovered."""
    repo = MagicMock(GameRepository)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item1.name = "test item 1"
    item1.is_collectible = True
    item2 = MagicMock(Item)
    item2.name = "test item 2"
    item2.is_collectible = True
    service.is_nearby = MagicMock(return_value=True)
    service.is_discovered = MagicMock(return_value=False)
    response = service.handle_multiple_interaction([item1, item2], "use_with")
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "You try to use the test item 1 but it's too far away. "
        + "Try picking it up first.",
    )


def test_handle_multiple_interaction_should_fail_when_cant_interact():
    """Method should fail when can_interact_multiple_items fails."""
    repo = MagicMock(GameRepository)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item1.name = "test item 1"
    item2 = MagicMock(Item)
    item2.name = "test item 2"
    service.is_nearby = MagicMock(return_value=True)
    service.is_discovered = MagicMock(return_value=True)
    service.can_interact_multiple_items = MagicMock(return_value=False)
    response = service.handle_multiple_interaction([item1, item2], "use_with")
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "You try to use the test item 1 with the "
        + "test item 2 but nothing interesting happens.",
    )


def test_handle_mutliple_interaction_should_pass_when_valid():
    """Method should succeed when all requirements are met."""
    repo = MagicMock(GameRepository)
    service = InteractionService(repo)
    item1 = MagicMock(Item)
    item1.name = "test item 1"
    item2 = MagicMock(Item)
    item2.name = "test item 2"
    service.is_nearby = MagicMock(return_value=True)
    service.is_discovered = MagicMock(return_value=True)
    service.can_interact_multiple_items = MagicMock(return_value=True)
    service.interact_multiple_items = MagicMock()
    service.handle_multiple_interaction([item1, item2], "use_with")
    service.interact_multiple_items.assert_called_once()


def test_update_interaction_objectives_should_update_objectives():
    """Method should update objectives when interaction is valid."""
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    objective = GameObjective("test objective", [], [], [])
    objective.complete_interaction_objective = MagicMock()
    repo.objectives.find_related_objectives = MagicMock(return_value=[objective])
    service = InteractionService(repo)
    item = MagicMock(Item)
    item.name = "test item"
    service.update_interaction_objectives(item, "use_with")
    objective.complete_interaction_objective.assert_called_once_with(
        "test item", "use_with"
    )


def test_unhide_items_returns_when_not_defined():
    """It should return when the interaction is not defined."""
    item = MagicMock(Item)
    item.hidden = True
    item.interactions = {}
    service = InteractionService(MagicMock(GameRepository))
    service.unhide_items(item, "use_with")
    assert item.hidden


def test_unhides_items_actually_unhides_hidden_items():
    """It should actually unhide hidden items defined in the interaction."""
    test_item = MagicMock(Item)
    test_item.hidden = False
    hidden_item = MagicMock(Item)
    hidden_item.hidden = True
    test_item.interactions = {"use_with": {"unhides": ["hidden item"]}}
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    repo.items.get_item_by_name = MagicMock(return_value=hidden_item)
    service = InteractionService(repo)
    service.unhide_items(test_item, "use_with")
    assert not hidden_item.hidden


def test_unlock_items_returns_when_not_defined():
    """It should return when the interaction is not defined."""
    item = MagicMock(Item)
    item.locked = True
    item.interactions = {}
    service = InteractionService(MagicMock(GameRepository))
    service.unlock_items(item, "use_with")
    assert item.locked


def test_unlock_items_actually_unlocks_locked_items():
    """It should actually unlock items specified in the interaction."""
    test_item = MagicMock(Item)
    test_item.locked = False
    locked_item = MagicMock(Item)
    locked_item.locked = True
    test_item.interactions = {"use_with": {"unlocks": ["locked item"]}}
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    repo.items.get_item_by_name = MagicMock(return_value=locked_item)
    service = InteractionService(repo)
    service.unlock_items(test_item, "use_with")
    assert not locked_item.locked


def test_sit_should_not_find_empty_lists():
    """Pull method should return not found when request.targets is empty."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.SIT, [])
    response = interaction_service.sit(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_sit_method():
    """Test to make sure the sit method works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"sit": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.sit(GameRequest(RequestType.SIT, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_discover_items():
    """Test to make sure items can be discovered."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item1 = MagicMock(Item)
    item1.name = "Test Item"
    item1.interactions = {
        "use": {"message": "Test Message", "discovers": ["Test Item 2"]}
    }
    item2 = MagicMock(Item)
    item2.name = "Test Item 2"
    item2.discovered = False
    repo.items.get_item_by_name = MagicMock(return_value=item2)
    interaction_service = InteractionService(repo)
    interaction_service.discover_items(item1, "use")
    assert item2.discovered == True


def test_discover_items_does_nothing_when_interaction_none():
    """Test to make sure no discovery happens when interaction is None."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item1 = MagicMock(Item)
    item1.name = "Test Item"
    item1.interactions = {}
    item2 = MagicMock(Item)
    item2.name = "Test Item 2"
    item2.discovered = False
    repo.items.get_item_by_name = MagicMock(return_value=item2)
    interaction_service = InteractionService(repo)
    interaction_service.discover_items(item1, "use")
    assert item2.discovered == False


def test_it_should_clean_items():
    """Test to make sure the clean interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"clean": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.clean(GameRequest(RequestType.CLEAN, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_drink_items():
    """Test to make sure the drink interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"drink": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.drink(GameRequest(RequestType.DRINK, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_not_drink_empty_items():
    """Test to make sure the drink method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.DRINK, [])
    response = interaction_service.drink(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_it_should_not_clean_empty_items():
    """Test to make sure the clean method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.CLEAN, [])
    response = interaction_service.clean(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_it_should_climb_items():
    """Test to make sure the climb interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"climb": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.climb(GameRequest(RequestType.CLIMB, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_not_climb_empty_items():
    """Test to make sure the climb method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.CLIMB, [])
    response = interaction_service.climb(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_it_should_turn_on_items():
    """Test to make sure the turn on interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"turn_on": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.turn_on(
        GameRequest(RequestType.TURN_ON, ["Test Item"])
    )
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_not_turn_on_empty_items():
    """Test to make sure the turn on method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.TURN_ON, [])
    response = interaction_service.turn_on(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_it_should_open_items():
    """Test to make sure the open interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"open": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.open(GameRequest(RequestType.OPEN, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_not_open_empty_items():
    """Test to make sure the open method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.OPEN, [])
    response = interaction_service.open(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_it_should_play_items():
    """Test to make sure the play interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"play": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.play(GameRequest(RequestType.PLAY, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_not_play_empty_items():
    """Test to make sure the play method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.PLAY, [])
    response = interaction_service.play(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )


def test_it_should_flush_items():
    """Test to make sure the flush interaction works."""
    repo = MagicMock(GameRepository)
    repo.items = MagicMock(ItemManager)
    item = MagicMock(Item)
    item.name = "Test Item"
    item.interactions = {"flush": {"message": "Test Message"}}
    repo.items.get_item_by_name = MagicMock(return_value=item)
    interaction_service = InteractionService(repo)
    return_value = GameResponse.success("Test Message")
    interaction_service.handle_single_interaction = MagicMock(return_value=return_value)
    response = interaction_service.flush(GameRequest(RequestType.FLUSH, ["Test Item"]))
    assert any_message_contents(response.messages, "Test Message")
    interaction_service.handle_single_interaction.assert_called_once()


def test_it_should_not_flush_empty_items():
    """Test to make sure the flush method fails correctly on empty targets."""
    repo = MagicMock(GameRepository)
    interaction_service = InteractionService(repo)
    request = GameRequest(RequestType.FLUSH, [])
    response = interaction_service.flush(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, you can't seem to find that.",
    )
