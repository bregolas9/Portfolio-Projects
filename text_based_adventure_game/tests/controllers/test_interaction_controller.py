"""Test the interaction controller."""

from typing import Any
from unittest.mock import MagicMock

from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.service_type import ServiceType
from controllers.interaction_controller import InteractionController
from services.interaction_service import InteractionService
from tests.test_helpers import any_message_contents


def mock_interaction_service() -> dict[ServiceType, Any]:
    """Return a mock inventory service for test setup."""
    mock_service = MagicMock(InteractionService)
    use_response = GameResponse.success("You used the item.")
    chew_response = GameResponse.success("You chewed the item.")
    pull_response = GameResponse.success("You pulled the item.")
    sit_response = GameResponse.success("You sat on an item.")
    drink_response = GameResponse.success("You drank the item.")
    clean_response = GameResponse.success("You cleaned the item.")
    climb_response = GameResponse.success("You climbed the item.")
    turn_on_response = GameResponse.success("You turned on the item.")
    opened_response = GameResponse.success("You opened the item.")
    play_response = GameResponse.success("You played the item.")
    flush_response = GameResponse.success("You flushed the item.")

    mock_service.use = MagicMock(name="use", return_value=use_response)
    mock_service.chew = MagicMock(name="chew", return_value=chew_response)
    mock_service.pull = MagicMock(name="pull", return_value=pull_response)
    mock_service.sit = MagicMock(name="sit", return_value=sit_response)
    mock_service.drink = MagicMock(name="drink", return_value=drink_response)
    mock_service.clean = MagicMock(name="clean", return_value=clean_response)
    mock_service.climb = MagicMock(name="climb", return_value=climb_response)
    mock_service.turn_on = MagicMock(name="turn_on", return_value=turn_on_response)
    mock_service.open = MagicMock(name="open", return_value=opened_response)
    mock_service.play = MagicMock(name="play", return_value=play_response)
    mock_service.flush = MagicMock(name="flush", return_value=flush_response)
    return {ServiceType.INTERACTION: mock_service}


def test_it_should_route_use_requests():
    """Test to ensure it routes an item use request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.USE, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You used the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.use.assert_called_once_with(request)


def test_it_should_route_pull_requests():
    """Test to ensure it routes an item pull request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.PULL, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You pulled the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.pull.assert_called_once_with(request)


def test_it_should_route_chew_requests():
    """Test to ensure it routes an item chew request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.CHEW, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You chewed the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.chew.assert_called_once_with(request)


def test_it_should_not_route_unknown_requests():
    """Test to ensure it does not route an unknown request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.UNKNOWN, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You are unsure how to do that.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_route_sit_requests():
    """Test to ensure it routes a sit request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.SIT, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You sat on an item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.sit.assert_called_once_with(request)


def test_it_should_route_drink_requests():
    """Test to ensure it routes a drink request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.DRINK, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You drank the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.drink.assert_called_once_with(request)


def test_it_should_route_clean_requests():
    """Test to ensure it routes a clean request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.CLEAN, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You cleaned the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.clean.assert_called_once_with(request)


def test_it_should_route_climb_requests():
    """Test to ensure it routes a climb request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.CLIMB, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You climbed the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.climb.assert_called_once_with(request)


def test_it_should_route_turn_on_requests():
    """Test to ensure it routes a turn on request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.TURN_ON, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You turned on the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.turn_on.assert_called_once_with(request)


def test_it_should_route_open_requests():
    """Test to ensure it routes an open request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.OPEN, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You opened the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.open.assert_called_once_with(request)


def test_it_should_route_play_requests():
    """Test to ensure it routes a play request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.PLAY, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You played the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.play.assert_called_once_with(request)


def test_it_should_route_flush_requests():
    """Test to ensure it routes a flush request."""
    interaction_controller = InteractionController(mock_interaction_service())
    request = GameRequest(RequestType.FLUSH, ["random item"])
    response = interaction_controller.route(request)
    assert any_message_contents(response.messages, "You flushed the item.")
    assert response.status == RequestStatus.SUCCESS
    interaction_controller.interaction_service.flush.assert_called_once_with(request)
