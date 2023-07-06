import builtins
from unittest.mock import MagicMock, patch

import pytest

from common.controller_type import ControllerType
from common.game_response import GameResponse
from common.player import Player
from common.request_status import RequestStatus
from common.service_type import ServiceType
from controllers.game_controller import GameController
from controllers.inventory_controller import InventoryController
from controllers.movement_controller import MovementController
from ForkOff import AdventureGame
from game_repository.file_manager import FileManager
from game_repository.game_repository import GameRepository
from game_repository.objectives_manager import ObjectiveManager
from language.language_manager import LanguageManager
from language.text_parser import TextParser
from router.router import Router
from services.game_service import GameService
from services.inventory_service import InventoryService
from services.movement_service import MovementService


def get_mock_services():
    """Return a mock services object."""
    return MagicMock({ServiceType.GAME: MagicMock(GameService)})


def get_mock_repo():
    """Return a mock repo object."""
    mock_repo = MagicMock(GameRepository)
    mock_repo.language = MagicMock(LanguageManager)
    mock_repo.language.yes_words = ["y", "yes"]
    mock_repo.game_active = False
    mock_repo.state_dirty = False
    mock_repo.game_won = False
    return mock_repo


def get_mock_parser():
    """Return a mock parser object."""
    mock_parser = MagicMock(TextParser)
    mock_parser.handle_game_input.return_value = None
    mock_parser.print_single_message.return_value = None
    return mock_parser


def test_adventure_game_runs():
    """Test the adventure game run method."""

    with patch.object(builtins, "input", return_value="y") as mock_input:
        with patch.object(AdventureGame, "initialize_game", return_value=None):
            game = AdventureGame()
            game.exit_game = MagicMock(name="exit_game", return_value=None)
            game.services = get_mock_services()
            game.text_parser = get_mock_parser()
            game.game_repository = get_mock_repo()
            game.initialize_game(False)
            game.try_handle_load_request = MagicMock(
                name="handle_load_request", return_value=RequestStatus.SUCCESS
            )
            game.run()
            game.text_parser.handle_game_input.assert_called()
            game.try_handle_load_request.assert_called_once()
            game.text_parser.display_look_request_on_startup.assert_called_once()
            game.exit_game.assert_called_once()


def test_it_should_run_and_ask_to_save_when_dirty():
    """Test for a save request on dirty state."""
    with patch.object(builtins, "input", return_value="y") as mock_input:
        with patch.object(AdventureGame, "initialize_game", return_value=None):
            game = AdventureGame()
            game.exit_game = MagicMock(name="exit_game", return_value=None)
            game.services = get_mock_services()
            game.text_parser = get_mock_parser()
            game.game_repository = get_mock_repo()
            game.try_handle_load_request = MagicMock(
                name="handle_load_request", return_value=RequestStatus.SUCCESS
            )
            game.handle_save_request = MagicMock(
                name="handle_save_request", return_value=None
            )
            game.user_confirmed = MagicMock(name="user_confirmed", return_value=True)
            game.game_repository.state_dirty = True
            game.run()
            game.text_parser.handle_game_input.assert_called()
            game.try_handle_load_request.assert_called_once()
            game.text_parser.display_look_request_on_startup.assert_called_once()
            game.handle_save_request.assert_called_once()
            game.exit_game.assert_called_once()


def test_it_should_run_and_ask_to_save_when_dirty_and_user_not_confirmed():
    """Test for a save request on dirty state."""
    with patch.object(builtins, "input", return_value="y") as mock_input:
        with patch.object(AdventureGame, "initialize_game", return_value=None):
            game = AdventureGame()
            game.exit_game = MagicMock(name="exit_game", return_value=None)
            game.services = get_mock_services()
            game.text_parser = get_mock_parser()
            game.game_repository = get_mock_repo()
            game.try_handle_load_request = MagicMock(
                name="handle_load_request", return_value=RequestStatus.SUCCESS
            )
            game.handle_save_request = MagicMock(
                name="handle_save_request", return_value=None
            )
            game.user_confirmed = MagicMock(name="user_confirmed", return_value=False)
            game.game_repository.state_dirty = True
            game.run()
            game.text_parser.handle_game_input.assert_called()
            game.try_handle_load_request.assert_called_once()
            game.text_parser.display_look_request_on_startup.assert_called_once()
            game.handle_save_request.assert_not_called()
            game.exit_game.assert_called_once()


def test_adventure_game_handles_save_request():
    """Test to make sure the adventure game can handle a save request."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        game.text_parser = MagicMock(TextParser)
        response = GameResponse.success("saved")
        game.text_parser.handle_game_input = MagicMock(
            name="handle_game_input", return_value=response
        )
        game.handle_save_request()
        game.text_parser.handle_game_input.assert_called_once_with("savegame", False)


def test_it_should_handle_load_requests():
    """Test to see if the adventure game can handle load requests."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        with patch.object(builtins, "input", return_value="y") as mock_input:
            game = AdventureGame()
            game.text_parser = MagicMock(TextParser)
            game.text_parser.print_single_message = MagicMock(return_value=None)
            response = GameResponse.success("loaded")
            game.text_parser.handle_game_input = MagicMock(
                name="handle_game_input", return_value=response
            )
            game.user_confirmed = MagicMock(name="user_confirmed", return_value=True)
            FileManager.has_saved_game = MagicMock(return_value=True)
            game.try_handle_load_request()
            game.text_parser.handle_game_input.assert_called_once_with(
                "loadgame", False
            )
            game.user_confirmed.assert_called_once_with("y")


def test_it_should_handle_new_game_requests():
    """Test to see if the adventure game can handle load requests."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        with patch.object(builtins, "input", return_value="n") as mock_input:
            FileManager.has_saved_game = MagicMock(return_value=False)
            game = AdventureGame()
            game.text_parser = MagicMock(TextParser)
            response = GameResponse.success("new game")
            game.text_parser.handle_game_input = MagicMock(
                name="handle_game_input", return_value=response
            )
            game.text_parser.print_single_message = MagicMock(
                name="print_single_message", return_value=None
            )
            game.try_handle_load_request()
            game.text_parser.handle_game_input.assert_called_once_with("newgame", False)


def test_it_should_confirm_responses():
    """Test to make sure the user_confirmed function works correctly."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        game.game_repository = get_mock_repo()
        game.game_repository.language = MagicMock(LanguageManager)
        game.game_repository.language.is_confirmed = MagicMock(return_value=True)
        assert game.user_confirmed("y") == True
        game.game_repository.language.is_confirmed = MagicMock(return_value=False)
        assert game.user_confirmed("n") == False


def test_it_should_initialize_text_parser():
    """Test the initialization of the text parser."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        parser = game.initialize_text_parser(
            MagicMock(Router), MagicMock(GameRepository)
        )
        assert isinstance(parser, TextParser)


def test_it_should_initialize_a_router():
    """Test to ensure it can initialize a router."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        router = game.initialize_router(
            {ControllerType.GAME: MagicMock(GameController)}
        )
        assert isinstance(router, Router)


def test_it_should_initialize_controllers():
    """Test to make sure all the necessary controllers are included."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        services = get_mock_services()
        controllers = game.initialize_controllers(services=services)
        assert isinstance(controllers[ControllerType.GAME], GameController)
        assert isinstance(controllers[ControllerType.MOVEMENT], MovementController)
        assert isinstance(controllers[ControllerType.INVENTORY], InventoryController)


def test_it_should_initialize_services():
    """Test to make sure it initializes the services correctly."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        repo = MagicMock(GameRepository)
        services = game.initialize_services(repo)
        assert isinstance(services[ServiceType.MOVEMENT], MovementService)
        assert isinstance(services[ServiceType.INVENTORY], InventoryService)
        assert isinstance(services[ServiceType.GAME], GameService)


def test_it_should_initialize_game_repository():
    """Test to ensure it initializes the game repository correctly."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        with patch.object(GameRepository, "load_default_state", return_value=None):
            repo = game.initialize_game_repository(False)
            assert isinstance(repo, GameRepository)


def test_it_initializes_the_game_correctly():
    """Test to make sure all the initializer functions are called."""
    game = AdventureGame()
    game.services = None  # type: ignore
    game.controllers = None  # type: ignore
    game.router = None  # type: ignore
    game.text_parser = None  # type: ignore
    game.game_repository = None  # type: ignore
    repo = MagicMock(GameRepository)
    services = get_mock_services()
    controllers = {
        ControllerType.GAME: MagicMock(GameController),
        ControllerType.MOVEMENT: MagicMock(MovementController),
        ControllerType.INVENTORY: MagicMock(InventoryController),
    }
    game.initialize_game_repository = MagicMock(
        name="initialize_game_repository", return_value=repo
    )
    game.initialize_services = MagicMock(
        name="initialize_services", return_value=services
    )
    game.initialize_controllers = MagicMock(
        name="initialize_controllers", return_value=controllers
    )
    game.initialize_router = MagicMock(
        name="initialize_router", return_value=MagicMock(Router)
    )
    game.initialize_text_parser = MagicMock(
        name="initialize_text_parser", return_value=MagicMock(TextParser)
    )
    game.initialize_game(False)
    game.initialize_game_repository.assert_called_once()
    game.initialize_services.assert_called_once_with(repo)
    game.initialize_controllers.assert_called_once_with(services)
    game.initialize_router.assert_called_once_with(controllers)
    game.initialize_text_parser.assert_called_once_with(game.router, repo)


def test_it_should_print_an_exit_message():
    """Test to make sure the print_exit_message function works correctly."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        with patch.object(builtins, "input", return_value="y") as mock_input:
            game = AdventureGame()
            game.text_parser = MagicMock(TextParser)
            game.print_exit_message()
            mock_input.assert_called_once()


def test_it_should_exit_the_game():
    """Test to make sure it exits the game when called."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        game.game_repository = MagicMock(GameRepository)
        game.game_repository.game_won = False
        game.print_exit_message = MagicMock(
            name="print_exit_message", return_value=None
        )
        with pytest.raises(SystemExit):
            game.exit_game()
        game.print_exit_message.assert_called_once()


def test_it_should_exit_the_game_and_not_print_ending_when_won():
    """Test to make sure it exits the game when called."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        game.game_repository = MagicMock(GameRepository)
        game.game_repository.player = MagicMock(Player)
        game.game_repository.player.won = True
        game.text_parser = MagicMock(TextParser)
        game.roll_end_credits = MagicMock(name="roll_end_credits", return_value=None)
        with pytest.raises(SystemExit):
            with patch.object(builtins, "input", return_value=""):
                game.exit_game()
        game.roll_end_credits.assert_not_called()


def test_it_should_handle_new_game_when_player_wants_new_but_has_saved_game():
    """Test to make sure that the game exits when a user denies a new game."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        with patch.object(builtins, "input", return_value="n"):
            game = AdventureGame()
            game.user_confirmed = MagicMock(name="user_confirmed", return_value=False)
            game.text_parser = MagicMock(TextParser)
            game.text_parser.handle_game_input = MagicMock(
                return_value=RequestStatus.SUCCESS
            )
            game.game_repository = MagicMock(GameRepository)
            game.game_repository.language = MagicMock(LanguageManager)
            game.game_repository.language.yes_words = ["y"]
            FileManager.has_saved_game = MagicMock(
                name="has_saved_game", return_value=True
            )
            status = game.try_handle_load_request()
            assert status == RequestStatus.SUCCESS


def test_it_should_handle_game_over():
    """Test to make sure the player wins and the game ends."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        repo = MagicMock(GameRepository)
        repo.player = MagicMock(Player)
        repo.player.won = False
        repo.objectives = MagicMock(ObjectiveManager)
        repo.objectives.all_objectives_complete = MagicMock(return_value=True)
        game.game_repository = repo
        game.check_for_game_over()
        assert game.game_repository.player.won == True


def test_it_should_print_ending():
    """Test to make sure it prints the ending."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        game.game_repository = MagicMock(GameRepository)
        game.text_parser = MagicMock(TextParser)
        game.text_parser.handle_game_input = MagicMock(return_value=None)
        game.print_ending()
        game.text_parser.handle_game_input.assert_called_once_with(
            "wax lyrical ending", True
        )


def test_it_should_roll_end_credits():
    """Test to make sure it rolls the end credits."""
    with patch.object(AdventureGame, "initialize_game", return_value=None):
        game = AdventureGame()
        game.game_repository = MagicMock(GameRepository)
        game.game_repository.scroll_delay = 0
        GameRepository.slow_scroll_delay = 0
        game.print_ending = MagicMock(name="print_ending", return_value=None)
        game.game_repository.player = MagicMock(Player)
        game.game_repository.player.won = True
        game.game_repository.player.watched_end_credits = False
        game.roll_end_credits()
        game.print_ending.assert_called_once()
        assert game.game_repository.player.watched_end_credits == True
