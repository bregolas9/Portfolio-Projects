"""Testing for the inventory controller."""

from typing import Any
from unittest.mock import MagicMock

from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.service_type import ServiceType
from controllers.inventory_controller import InventoryController
from services.inventory_service import InventoryService
from tests.test_helpers import any_message_contents


def mock_inventory_service() -> dict[ServiceType, Any]:
    """Return a mock inventory service for test setup."""
    mock_service = MagicMock(InventoryService)
    inventory_response = GameResponse.success("You have no items")
    drop_response = GameResponse.success("Dropped item")
    take_response = GameResponse.success("Picked up item")
    use_response = GameResponse.success("You used the item!")
    inspect_response = GameResponse.success("You looked at the item!")

    mock_service.open_inventory = MagicMock(
        name="open_inventory", return_value=inventory_response
    )
    mock_service.pick_up = MagicMock(name="pick_up", return_value=take_response)
    mock_service.use_item = MagicMock(name="use_item", return_value=use_response)
    mock_service.look_at = MagicMock(name="look_at", return_value=inspect_response)
    mock_service.drop = MagicMock(name="drop", return_value=drop_response)
    return {ServiceType.INVENTORY: mock_service}


def test_it_should_pick_up_items():
    """Test to ensure the inventory controller can route TAKE requests."""
    inventory_controller = InventoryController(mock_inventory_service())
    request = GameRequest(RequestType.TAKE, "random item")
    response = inventory_controller.route(request)
    assert any_message_contents(response.messages, "Picked up item")
    assert response.status == RequestStatus.SUCCESS
    inventory_controller.inventory_service.pick_up.assert_called_once_with(request)


def test_it_should_drop_items():
    """Test to ensure the inventory controller can route DROP requests."""
    inventory_controller = InventoryController(mock_inventory_service())
    request = GameRequest(RequestType.DROP, "random item")
    response = inventory_controller.route(request)
    assert any_message_contents(response.messages, "Dropped item")
    assert response.status == RequestStatus.SUCCESS
    inventory_controller.inventory_service.drop.assert_called_once_with(request)


def test_it_should_show_inventory_contents():
    """Test to ensure it returns the contents of the inventory."""
    inventory_controller = InventoryController(mock_inventory_service())
    request = GameRequest(RequestType.INVENTORY, "random item")
    response = inventory_controller.route(request)
    assert any_message_contents(response.messages, "You have no items")
    assert response.status == RequestStatus.SUCCESS
    inventory_controller.inventory_service.open_inventory.assert_called_once_with(
        request
    )


def test_it_should_not_route_unknown_requests():
    """Test to ensure it returns an error for unknown requests."""
    inventory_controller = InventoryController(mock_inventory_service())
    request = GameRequest(RequestType.UNKNOWN, "random item")
    response = inventory_controller.route(request)
    assert any_message_contents(response.messages, "You are unsure how to do that.")
    assert response.status == RequestStatus.FAILURE
    inventory_controller.inventory_service.open_inventory.assert_not_called()


def test_it_should_route_look_at_requests():
    """Test to make sure look at/inspect requests are routed."""
    inventory_controller = InventoryController(mock_inventory_service())
    request = GameRequest(RequestType.INSPECT, "random item")
    response = inventory_controller.route(request)
    assert any_message_contents(response.messages, "You looked at the item!")
    assert response.status == RequestStatus.SUCCESS
    inventory_controller.inventory_service.look_at.assert_called_once_with(request)
