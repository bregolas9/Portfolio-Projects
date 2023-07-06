"""Test the movement controller."""

from unittest.mock import MagicMock
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.service_type import ServiceType
from controllers.movement_controller import MovementController
from services.movement_service import MovementService
from tests.test_helpers import any_message_contents


def test_movement_controller_move_method_is_called():
    """Test that the move method in the movement controller is called."""
    request = GameRequest(RequestType.MOVE, "somewhere")
    response = GameResponse.success("test message")
    mock_service = MagicMock(MovementService)
    mock_service.move = MagicMock(name="move", return_value=response)

    movement_controller = MovementController(
        services={ServiceType.MOVEMENT: mock_service}
    )
    movement_controller.move(request)
    mock_service.move.assert_called_once()


def test_movement_controller_look_method_is_called():
    """Test what happens when the look method is called."""
    request = GameRequest(RequestType.LOOK, "somewhere")
    response = GameResponse.success("test message")
    mock_service = MagicMock(MovementService)
    mock_service.look = MagicMock(name="look", return_value=response)

    movement_controller = MovementController(
        services={ServiceType.MOVEMENT: mock_service}
    )
    movement_controller.look(request)
    mock_service.look.assert_called_once()


def test_it_should_route_move_requests():
    """Test to make sure it can route a move request."""
    request = GameRequest(RequestType.MOVE, "somewhere")
    response = GameResponse.success("test message")
    mock_service = MagicMock(MovementService)
    controller = MovementController(services={ServiceType.MOVEMENT: mock_service})
    controller.move = MagicMock(name="move", return_value=response)
    result = controller.route(request)
    controller.move.assert_called_once_with(request)
    assert result == response


def test_it_should_route_look_requests():
    """Test to make sure it can route a move request."""
    request = GameRequest(RequestType.LOOK, "somewhere")
    response = GameResponse.success("test message")
    mock_service = MagicMock(MovementService)
    controller = MovementController(services={ServiceType.MOVEMENT: mock_service})
    controller.look = MagicMock(name="look", return_value=response)
    result = controller.route(request)
    assert result == response
    controller.look.assert_called_once_with(request)


def test_it_should_not_route_unknown_requests():
    """Test to make sure it does not route unknown requests."""
    services = {ServiceType.MOVEMENT: MovementService(MagicMock)}
    request = GameRequest(RequestType.UNKNOWN, "somewhere")
    controller = MovementController(services=services)
    result = controller.route(request)
    assert any_message_contents(result.messages, "You are unsure how to do that.")
    assert result.status == RequestStatus.FAILURE
