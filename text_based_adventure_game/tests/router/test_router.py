"""Test the router module."""

from unittest.mock import MagicMock

from common.controller_type import ControllerType
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from common.request_type import RequestType
from controllers.game_controller import GameController
from controllers.interaction_controller import InteractionController
from controllers.inventory_controller import InventoryController
from controllers.movement_controller import MovementController
from router.router import Router
from tests.test_helpers import any_message_contents


def get_default_controllers(
    controller_type: ControllerType, expected_response: GameResponse
):
    """Return some mocked default controllers for ease of use."""
    movement_controller = MagicMock(MovementController)
    game_controller = MagicMock(GameController)
    inventory_controller = MagicMock(InventoryController)
    interaction_controller = MagicMock(InteractionController)
    movement_controller.request_types = [RequestType.MOVE, RequestType.LOOK]
    game_controller.request_types = [
        RequestType.EXIT,
        RequestType.GAME_STORY,
        RequestType.LOAD_GAME,
        RequestType.NEW_GAME,
        RequestType.SAVE_GAME,
    ]
    inventory_controller.request_types = [
        RequestType.TAKE,
        RequestType.DROP,
        RequestType.INVENTORY,
    ]
    interaction_controller.request_types = [
        RequestType.CHEW,
        RequestType.PULL,
        RequestType.USE,
    ]
    if controller_type == ControllerType.MOVEMENT:
        movement_controller.route = MagicMock(
            name="move", return_value=expected_response
        )
    elif controller_type == ControllerType.GAME:
        game_controller.route = MagicMock(name="route", return_value=expected_response)
    elif controller_type == ControllerType.INVENTORY:
        inventory_controller.route = MagicMock(
            name="route", return_value=expected_response
        )
    else:
        interaction_controller.route = MagicMock(
            name="route", return_value=expected_response
        )
    return {
        ControllerType.MOVEMENT: movement_controller,
        ControllerType.GAME: game_controller,
        ControllerType.INVENTORY: inventory_controller,
        ControllerType.INTERACTION: interaction_controller,
    }


def test_router_can_handle_movement():
    """Test the router to ensure it routes move requests."""

    expected_response = GameResponse.success("Moved north")
    controllers = get_default_controllers(ControllerType.MOVEMENT, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(RequestType.MOVE, ["north"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Moved north")
    assert response.status == expected_response.status
    controllers[ControllerType.MOVEMENT].route.assert_called_once_with(request)


def test_router_can_handle_exit():
    """Test to ensure the router can handle an exit request."""
    expected_response = GameResponse.success("Goodbye")
    controllers = get_default_controllers(ControllerType.GAME, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(RequestType.EXIT, ["exit"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Goodbye")
    assert response.status == expected_response.status
    controllers[ControllerType.GAME].route.assert_called_once_with(request)


def test_router_can_handle_game_stories():
    """Test that the router can handle game story requests."""
    expected_response = GameResponse.success("Game story")
    controllers = get_default_controllers(ControllerType.GAME, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(RequestType.GAME_STORY, ["game story"])
    response = router.route(request)
    assert response.status == expected_response.status
    assert any_message_contents(response.messages, "Game story")
    controllers[ControllerType.GAME].route.assert_called_once_with(request)


def test_router_can_handle_look_requests():
    """Test to make sure the router can handle LOOK requests."""
    expected_response = GameResponse.success("Looked")
    controllers = get_default_controllers(ControllerType.MOVEMENT, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.LOOK, targets=["kitchen"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Looked")
    assert response.status == expected_response.status
    controllers[ControllerType.MOVEMENT].route.assert_called_once_with(request)


def test_router_handles_invalid_requests():
    """Test the router to ensure it handles invalid requests."""
    controllers = get_default_controllers(ControllerType.GAME, MagicMock)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.UNKNOWN, targets=["unknown"])
    response = router.route(request)
    assert any_message_contents(response.messages, "You are unsure how to do that.")
    assert response.status == RequestStatus.FAILURE


def test_router_handles_save_game_requests():
    """Test the router to ensure it handles save game requests."""
    expected_response = GameResponse.success("Saved")
    controllers = get_default_controllers(ControllerType.GAME, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.SAVE_GAME, targets=["save"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Saved")
    assert response.status == expected_response.status
    controllers[ControllerType.GAME].route.assert_called_once_with(request)


def test_router_handles_new_game_requests():
    """Test the router to ensure it handles new game requests."""
    expected_response = GameResponse.success("New Game")
    controllers = get_default_controllers(ControllerType.GAME, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.NEW_GAME, targets=["anything"])
    response = router.route(request)
    assert any_message_contents(response.messages, "New Game")
    assert response.status == expected_response.status
    controllers[ControllerType.GAME].route.assert_called_once_with(request)


def test_router_handles_load_game_requests():
    """Test the router to ensure it handles load game requests."""
    expected_response = GameResponse.success("Loaded")
    controllers = get_default_controllers(ControllerType.GAME, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.LOAD_GAME, targets=["anything"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Loaded")
    assert response.status == expected_response.status
    controllers[ControllerType.GAME].route.assert_called_once_with(request)


def test_router_handles_take_requests():
    """Test the router to ensure it handles take item requests."""
    expected_response = GameResponse.success("Taken")
    controllers = get_default_controllers(ControllerType.INVENTORY, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.TAKE, targets=["item"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Taken")
    assert response.status == expected_response.status
    controllers[ControllerType.INVENTORY].route.assert_called_once_with(request)


def test_router_handles_drop_requests():
    """Test the router to ensure it handles drop item requests."""
    expected_response = GameResponse.success("Dropped")
    controllers = get_default_controllers(ControllerType.INVENTORY, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.DROP, targets=["item"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Dropped")
    assert response.status == expected_response.status
    controllers[ControllerType.INVENTORY].route.assert_called_once_with(request)


def test_router_handles_inventory_requests():
    """Test the router to ensure it handles inventory content requests."""
    expected_response = GameResponse.success("Inventory")
    controllers = get_default_controllers(ControllerType.INVENTORY, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.INVENTORY, targets=["inventory"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Inventory")
    assert response.status == expected_response.status
    controllers[ControllerType.INVENTORY].route.assert_called_once_with(request)


def test_router_handles_interaction_requests():
    """Test the router to ensure it handles interaction requests."""
    expected_response = GameResponse.success("Interacted")
    controllers = get_default_controllers(ControllerType.INTERACTION, expected_response)
    router = Router(controllers=controllers)
    request = GameRequest(request_type=RequestType.USE, targets=["interact"])
    response = router.route(request)
    assert any_message_contents(response.messages, "Interacted")
    assert response.status == expected_response.status
    controllers[ControllerType.INTERACTION].route.assert_called_once_with(request)
