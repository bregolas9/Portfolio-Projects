"""Test the game controller to ensure it works correctly."""

from unittest.mock import MagicMock, Mock, patch

from common.game_request import GameRequest
from common.game_response import GameResponse
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.service_type import ServiceType
from controllers.game_controller import GameController
from services.game_service import GameService
from services.inventory_service import InventoryService
from services.movement_service import MovementService
from tests.test_helpers import any_message_contents


def test_it_should_handle_exits():
    """Test that the game controller can handle an exit request."""

    mock_service = Mock(GameService)
    services = {ServiceType.GAME: mock_service}

    with patch.object(
        mock_service,
        "exit",
        return_value=GameResponse.success("a message"),
    ) as mock_exit:
        game_controller = GameController(services)
        response = game_controller.exit(GameRequest(RequestType.EXIT, ["a message"]))

        mock_exit.assert_called_once()
        assert response.status == RequestStatus.SUCCESS
        assert any_message_contents(response.messages, "a message")


def test_it_should_handle_game_stories():
    """Test that the game controller can handle a request to print a game story."""

    mock_service = Mock(GameService)
    services = {ServiceType.GAME: mock_service}

    mock_service.game_story.return_value = GameResponse.success("a message")

    game_controller = GameController(services)
    response = game_controller.game_story(
        GameRequest(RequestType.GAME_STORY, ["anything"])
    )

    assert mock_service.game_story.call_count == 1
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "a message")


def test_it_should_handle_new_games():
    """Test if it handles a new game request."""
    mock_service = MagicMock(GameService)
    response = GameResponse.success("A new game has been started.")
    mock_service.load_game = MagicMock(name="load_game", return_value=response)
    services = {ServiceType.GAME: mock_service}

    game_controller = GameController(services)
    request = GameRequest(RequestType.NEW_GAME, ["anything"])
    response = game_controller.new_game(request=request)

    mock_service.load_game.assert_called_once_with(request, True)
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "A new game has been started.")


def test_it_should_handle_load_game():
    """Test if it handles a load game request."""
    mock_service = MagicMock(GameService)
    mock_service.load_game = MagicMock(
        name="load_game",
        return_value=GameResponse.success("A game has been loaded."),
    )
    services = {ServiceType.GAME: mock_service}

    game_controller = GameController(services)
    request = GameRequest(RequestType.LOAD_GAME, ["anything"])
    response = game_controller.load_game(request)

    mock_service.load_game.assert_called_once_with(request, False)
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "A game has been loaded.")


def test_it_should_handle_save_game():
    """Test if the controller can route save game requests."""
    mock_service = MagicMock(GameService)
    mock_service.save_game = MagicMock(
        name="save_game",
        return_value=GameResponse.success("A game has been saved."),
    )
    services = {ServiceType.GAME: mock_service}

    game_controller = GameController(services)
    request = GameRequest(RequestType.SAVE_GAME, ["anything"])
    response = game_controller.save_game(request)

    mock_service.save_game.assert_called_once_with(request)
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "A game has been saved.")


def test_it_should_route_exit_requests():
    """Test to make sure it can route an exit request."""
    request = GameRequest(RequestType.EXIT, ["anything"])
    response = GameResponse.success("test message")
    mock_service = MagicMock(GameService)
    controller = GameController(services={ServiceType.GAME: mock_service})
    controller.exit = MagicMock(name="exit", return_value=response)
    result = controller.route(request)
    assert result == response
    controller.exit.assert_called_once_with(request)


def test_it_should_route_load_requests():
    """Test to make sure it can route a load request."""
    request = GameRequest(RequestType.LOAD_GAME, ["anything"])
    response = GameResponse.success("test message")
    mock_service = MagicMock(GameService)
    controller = GameController(services={ServiceType.GAME: mock_service})
    controller.load_game = MagicMock(name="load_game", return_value=response)
    result = controller.route(request)
    assert result == response
    controller.load_game.assert_called_once_with(request)


def test_it_should_route_newgame_requests():
    """Test to make sure it can route a newgame request."""
    request = GameRequest(RequestType.NEW_GAME, ["anything"])
    response = GameResponse.success("test message")
    mock_service = MagicMock(GameService)
    controller = GameController(services={ServiceType.GAME: mock_service})
    controller.new_game = MagicMock(name="new_game", return_value=response)
    result = controller.route(request)
    assert result == response
    controller.new_game.assert_called_once_with(request)


def test_it_should_route_save_requests():
    """Test to make sure it can route a save request."""
    request = GameRequest(RequestType.SAVE_GAME, ["anything"])
    response = GameResponse.success("test message")
    mock_service = MagicMock(GameService)
    controller = GameController(services={ServiceType.GAME: mock_service})
    controller.save_game = MagicMock(name="save_game", return_value=response)
    result = controller.route(request)
    assert result == response
    controller.save_game.assert_called_once_with(request)


def test_it_should_route_game_story_requests():
    """Test to make sure it can route a game story request."""
    request = GameRequest(RequestType.GAME_STORY, ["anything"])
    response = GameResponse.success("test message")
    mock_service = MagicMock(GameService)
    controller = GameController(services={ServiceType.GAME: mock_service})
    controller.game_story = MagicMock(name="game_story", return_value=response)
    result = controller.route(request)
    assert result == response
    controller.game_story.assert_called_once_with(request)


def test_it_should_not_route_unknown_requests():
    """Test to make sure it does not route unknown requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.UNKNOWN, ["anything"])
    controller = GameController(services=services)
    result = controller.route(request)
    assert any_message_contents(result.messages, "You are unsure how to do that.")
    assert result.status == RequestStatus.FAILURE


def test_it_should_route_help_requests():
    """Test to ensure that the controller routes help requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.HELP, ["anything"])
    controller = GameController(services=services)
    controller.provide_help = MagicMock(
        name="provide_help",
        return_value=GameResponse.success("Help is on the way!"),
    )
    result = controller.route(request)
    assert any_message_contents(result.messages, "Help is on the way!")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_help_request_to_game_service():
    """Test to make sure it routes the request to the game service."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.HELP, ["anything"])
    services[ServiceType.GAME].provide_help = MagicMock(
        name="provide_help",
        return_value=GameResponse.success("Help is on the way!"),
    )
    controller = GameController(services=services)
    result = controller.provide_help(request)
    assert any_message_contents(result.messages, "Help is on the way!")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_goals_request_to_game_service():
    """Test to make sure it routes the request to the game service."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.OBJECTIVES, ["anything"])
    services[ServiceType.GAME].list_objective = MagicMock(
        name="list_objective",
        return_value=GameResponse.success("Help is on the way!"),
    )
    controller = GameController(services=services)
    result = controller.list_objective(request)
    assert any_message_contents(result.messages, "Help is on the way!")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_objective_requests():
    """Test to ensure that the controller routes objective requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.OBJECTIVES, ["anything"])
    controller = GameController(services=services)
    controller.list_objective = MagicMock(
        name="list_objective",
        return_value=GameResponse.success("Help is on the way!"),
    )
    result = controller.route(request)
    assert any_message_contents(result.messages, "Help is on the way!")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_alias_requests():
    """Test to ensure that the controller routes objective requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.ALIAS, ["anything"])
    controller = GameController(services=services)
    expected_response = GameResponse.success("alias")
    controller.alias = MagicMock(
        name="alias",
        return_value=expected_response,
    )
    result = controller.route(request)
    assert any_message_contents(result.messages, "alias")
    controller.alias.assert_called_once_with(request)
    assert result.status == RequestStatus.SUCCESS


def test_it_should_call_game_service_aliases():
    """Testing to make sure game service aliases are called."""
    mock_game_service = MagicMock(GameService)
    expected_response = GameResponse.success("success")
    mock_game_service.give_aliases = MagicMock(return_value=expected_response)
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: mock_game_service,
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.ALIAS, [])
    controller = GameController(services=services)
    response = controller.alias(request)
    assert response is not None
    assert response.status == RequestStatus.SUCCESS


def test_it_should_route_scroll_requests():
    """Test to make sure it can route scroll requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.SCROLL, ["fast"])
    controller = GameController(services=services)
    controller.game_service = MagicMock(GameService)
    controller.game_service.scroll = MagicMock(
        return_value=GameResponse.success("fast")
    )
    result = controller.route(request)
    assert any_message_contents(result.messages, "fast")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_map_requests():
    """Test to make sure it can route map requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.GAME_MAP, ["test"])
    controller = GameController(services=services)
    controller.game_service = MagicMock(GameService)
    controller.game_service.draw = MagicMock(return_value=GameResponse.success("test"))
    result = controller.route(request)
    assert any_message_contents(result.messages, "test")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_hint_requests():
    """Test to make sure it can route hint requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.HINT, ["test"])
    controller = GameController(services=services)
    controller.game_service = MagicMock(GameService)
    controller.game_service.get_hints = MagicMock(
        return_value=GameResponse.success("test")
    )
    result = controller.route(request)
    assert any_message_contents(result.messages, "test")
    assert result.status == RequestStatus.SUCCESS


def test_it_should_route_draw_requests():
    """Test to make sure it can route draw requests."""
    services = {
        ServiceType.MOVEMENT: MagicMock(MovementService),
        ServiceType.GAME: MagicMock(GameService),
        ServiceType.INVENTORY: MagicMock(InventoryService),
    }
    request = GameRequest(RequestType.DRAW, ["test"])
    controller = GameController(services=services)
    controller.game_service = MagicMock(GameService)
    controller.game_service.draw = MagicMock(return_value=GameResponse.success("test"))
    result = controller.route(request)
    assert any_message_contents(result.messages, "test")
    assert result.status == RequestStatus.SUCCESS
