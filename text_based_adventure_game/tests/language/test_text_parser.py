"""Test the text parser."""

import builtins
import textwrap
import time
from typing import Any
from unittest.mock import MagicMock, call, patch

from common.environment import Environment
from common.game_message import GameMessage
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.player import Player
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.room import Room
from game_repository.game_repository import GameRepository
from game_repository.item_manager import ItemManager
from language.text_parser import TextParser
from router.router import Router
from tests.test_helpers import any_message_contents


def default_repo() -> MagicMock:
    """Returns a default repository with some mock data."""
    rooms = {
        "kitchen": Room(
            name="kitchen",
            description={"description1": "the kitchen"},
            exits=[],
            directional_exits={"south": "living room"},
            aliases=[],
            blockers=[],
            inventory=[],
            starting_inventory=[],
        ),
        "living room": Room(
            name="living room",
            description={"default": "the living room"},
            exits=[],
            directional_exits={"north": "kitchen"},
            aliases=[],
            blockers=[],
            inventory=[],
            starting_inventory=[],
        ),
        "really long room name": Room(
            name="really long room name",
            description={"default": "the really long room name"},
            exits=[],
            directional_exits={"north": "kitchen"},
            aliases=[],
            blockers=[],
            inventory=[],
            starting_inventory=[],
        ),
    }
    repo = MagicMock(GameRepository)
    repo.language = MagicMock()
    repo.items = MagicMock(ItemManager)
    repo.language.move_requests = ["go", "move", "walk", "run", "travel", "head"]
    repo.language.look_requests = ["look"]
    repo.language.take_requests = ["take", "get", "grab", "steal"]
    repo.language.drop_requests = ["drop", "trash", "discard"]
    repo.language.exit_requests = ["exit", "quit", "leave", "end", "stop"]
    repo.language.unnecessary_words = ["the", "a", "an", "to", "at", "in", "on"]
    repo.language.inspect_requests = ["inspect", "examine", "look at"]
    repo.language.save_requests = ["save", "savegame"]
    repo.language.load_requests = ["load", "loadgame"]
    repo.language.new_game_requests = ["new", "newgame"]
    repo.language.yes_words = ["yes", "y", "yeah", "yep"]
    repo.language.inventory_requests = ["inventory", "items", "tools"]
    repo.language.help_requests = ["help", "?"]
    repo.language.objective_requests = ["objective", "goal", "objectives", "goals"]
    repo.rooms = rooms
    repo.find_target = MagicMock(name="find_target", return_value="valid target")
    repo.player = MagicMock(Player)
    repo.player.location = repo.rooms["kitchen"]
    repo.environment = Environment(False)
    repo.scroll_delay = 0
    return repo


def test_parser_should_parse_empty_string():
    """The text parser should parse an empty string."""

    text_parser = TextParser(MagicMock, default_repo())
    request = text_parser.parse_text("", True)
    assert request.action is RequestType.UNKNOWN
    assert request.targets == [""]


def test_parser_should_parse_one_word_as_target():
    """The text parser should parse one word as a movement target."""
    repo = default_repo()
    text_parser = TextParser(MagicMock, repo)
    text_parser.handle_single_word_request = MagicMock()
    text_parser.parse_text("north", True)
    text_parser.handle_single_word_request.assert_called_once()


def test_parser_should_parse_one_word_as_action():
    """The test parser should parse one word as an action."""
    repo = default_repo()
    text_parser = TextParser(MagicMock, repo)
    text_parser.handle_single_word_request = MagicMock()
    text_parser.parse_text("exit", True)
    text_parser.handle_single_word_request.assert_called_once()


def test_parser_should_parse_two_words():
    """The text parser should parse two words."""
    repo = default_repo()
    text_parser = TextParser(MagicMock, repo)
    text_parser.handle_two_word_request = MagicMock(
        name="handle_two_word_request", return_value=None
    )
    text_parser.parse_text("go north", True)
    text_parser.handle_two_word_request.assert_called_once()


def test_parser_should_print_instructions():
    """The text parser should print instructions."""

    text_parser = TextParser(MagicMock, MagicMock)
    text_parser.scroll_print = MagicMock(name="scroll_print", return_value=None)
    message = GameMessage.single_line("Test instructions")
    text_parser.print_single_message(message, False)
    text_parser.scroll_print.assert_called_once_with("Test instructions")


def test_parser_should_print_responses():
    """The text parser should print GameResponses."""
    text_parser = TextParser(MagicMock, MagicMock)
    text_parser.scroll_print = MagicMock(name="scroll_print", return_value=None)
    response = GameResponse.success("Test response")
    text_parser.print_response(response, True)
    text_parser.scroll_print.assert_called_once_with("    Test response")


def test_scroll_print_should_sleep():
    """The scroll print method should sleep."""

    with patch.object(time, "sleep", return_value=None) as mock_sleep:
        with patch.object(builtins, "print", return_value=None) as mock_print:
            repo = default_repo()
            repo.scroll_delay = 0.01
            repo.environment = Environment(False)
            text_parser = TextParser(MagicMock, repo)
            input_text = "Test text"
            text_parser.scroll_print(input_text)
            # It should sleep each time a letter is printed
            assert mock_sleep.call_count == len(input_text)
            # It should print each letter and then a new line at the end
            assert mock_print.call_count == len(input_text) + 1


def test_it_should_handle_invalid_input():
    """Test invalid inputs."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(
        name="get_request_type", return_value=RequestType.UNKNOWN
    )
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.get_request_type("invalid", True) == RequestType.UNKNOWN


def test_it_should_handle_find_target_with_one_word():
    """The find_valid_target method should find valid targets with one word."""
    repo = default_repo()
    repo.find_target.return_value = "kitchen"
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.find_valid_target(["kitchen"], True) == "kitchen"


def test_it_should_handle_find_target_with_two_words():
    """The find_valid_target method should find valid targets with two words."""
    repo = default_repo()
    repo.find_target.return_value = "living room"
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.find_valid_target(["living", "room"], True) == "living room"


def test_it_should_handle_find_target_when_invalid():
    """It the find_valid_target method should return None when invalid."""
    repo = default_repo()
    repo.find_target.return_value = ""
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.find_valid_target(["random", "place"], True) == ""


def test_it_should_handle_find_target_with_empty_list():
    """It the find_valid_target method should return None when empty list."""
    repo = default_repo()
    repo.find_target.return_value = ""
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.find_valid_target([], True) == ""


def test_parse_text_should_handle_variable_length_action_and_target():
    """The parse text method should handle variable length actions and targets."""
    repo = default_repo()
    repo.language.get_request_type.return_value = RequestType.MOVE
    repo.find_target.return_value = "living room"
    text_parser = TextParser(MagicMock, repo)
    result = text_parser.parse_text("go to the living room", True)
    assert result.action == RequestType.MOVE
    assert result.targets == ["living room"]


def test_parser_can_handle_game_stories():
    """Test the text parser's ability to handle a game story request."""
    repo = default_repo()
    repo.find_target.return_value = "introduction"
    mock_router = MagicMock(Router)
    router_response = GameResponse.success("here is an introduction")
    mock_router.route = MagicMock(name="route", return_value=router_response)
    text_parser = TextParser(mock_router, repo)
    text_parser.print_response = MagicMock(name="print_response", return_value=None)
    text_parser.handle_game_input("play introduction", True)
    text_parser.print_response.assert_called_once_with(router_response, True)


def test_parser_should_print_without_spaces():
    """Make sure the print_response method can print without spaces."""
    text_parser = TextParser(MagicMock, MagicMock)
    text_parser.scroll_print = MagicMock(name="scroll_print", return_value=None)
    response = GameResponse.success("Test response")
    text_parser.print_response(response, False)
    text_parser.scroll_print.assert_called_once_with("Test response")


def test_handle_user_input_should_work():
    """Test the handle_user_input method."""
    mock_router = MagicMock(Router)
    router_response = GameResponse.success("test response")
    mock_router.route = MagicMock(name="route", return_value=router_response)
    text_parser = TextParser(mock_router, MagicMock)
    text_parser.print_response = MagicMock(name="print_response", return_value=None)
    text_parser.print_single_message = MagicMock(
        name="print_single_message", return_value=None
    )
    parse_text_response = GameRequest(RequestType.MOVE, ["up"])
    text_parser.parse_text = MagicMock(
        name="parse_text", return_value=parse_text_response
    )
    with patch.object(builtins, "input", return_value="test input") as mock_input:
        text_parser.handle_user_input()
        text_parser.print_single_message.assert_called()
        mock_router.route.assert_called_once()
        text_parser.print_response.assert_called_once()
        mock_input.assert_called_once()


def test_it_should_get_game_story_request_types_when_not_user():
    """Test if the get_request_type method can return a Game Story request type."""
    mock_repo = default_repo()
    mock_repo.language.get_request_type.return_value = RequestType.GAME_STORY
    text_parser = TextParser(MagicMock, mock_repo)
    assert text_parser.get_request_type("play", False) == RequestType.GAME_STORY


def test_it_should_not_get_game_story_request_types_when_user():
    """Test if the get_request_type method can return a Game Story request type."""
    mock_repo = default_repo()
    mock_repo.language.get_request_type.return_value = RequestType.GAME_STORY
    text_parser = TextParser(MagicMock, mock_repo)
    assert text_parser.get_request_type("play", True) == RequestType.UNKNOWN


def test_it_should_handle_inspect_requests():
    """Test if the get_request_type method can return an inspect request type."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.INSPECT)
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.get_request_type("inspect", True) == RequestType.INSPECT


def test_it_should_handle_objectives_requests_when_in_development():
    """Test if the get_request_type method can return an objectives request type."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.OBJECTIVES)
    repo.environment.is_development = True
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.get_request_type("objectives", True) == RequestType.OBJECTIVES


def test_it_should_handle_objectives_requests_when_not_in_development():
    """Test if the get_request_type method can return an objectives request type."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.OBJECTIVES)
    repo.environment.is_development = False
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.get_request_type("objectives", True) == RequestType.UNKNOWN


def test_it_should_get_move_request_for_really_long_room_name():
    """Test if the text parser can find a long room name without an action specified."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.MOVE)
    repo.find_target.return_value = "really long room name"
    text_parser = TextParser(MagicMock, repo)
    split_text = ["really", "long", "room", "name"]
    request = text_parser.handle_multi_word_request(split_text, True)
    assert request.action == RequestType.MOVE
    assert request.targets == ["really long room name"]


def test_it_should_print_look_message_on_startup():
    """Test that the look description message is printed on startup."""
    repo = default_repo()
    repo.find_target.return_value = "kitchen"
    mock_router = MagicMock(Router)
    mock_router.route.return_value = GameResponse(
        repo.rooms["kitchen"].description, RequestStatus.SUCCESS
    )
    text_parser = TextParser(mock_router, repo)
    text_parser.print_response = MagicMock(name="print_response", return_value=None)
    text_parser.display_look_request_on_startup()
    text_parser.print_response.assert_called_once()


def test_it_should_return_save_requests():
    """Test to make sure the test parser can return a save request."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.SAVE_GAME)
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.get_request_type("save", True) == RequestType.SAVE_GAME


def test_it_should_return_load_requests_when_user_confirms():
    """Test to make sure the test parser can return a load request."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.LOAD_GAME)
    text_parser = TextParser(MagicMock, repo)
    text_parser.confirm_load_game = MagicMock(
        name="confirm_load_game", return_value=True
    )
    assert text_parser.get_request_type("load", True) == RequestType.LOAD_GAME
    text_parser.confirm_load_game.assert_called_once()


def test_it_should_deny_load_requests_when_user_denies():
    """Test to make sure user denial returns a load_denied request."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.LOAD_GAME)
    text_parser = TextParser(MagicMock, repo)
    text_parser.confirm_load_game = MagicMock(
        name="confirm_load_game", return_value=False
    )
    assert text_parser.get_request_type("load", True) == RequestType.LOAD_GAME_DENIED
    text_parser.confirm_load_game.assert_called_once()


def test_it_should_understand_new_game_requests():
    """Test to make sure the text parser can understand new game requests."""
    repo = default_repo()
    repo.language.get_request_type = MagicMock(return_value=RequestType.NEW_GAME)
    text_parser = TextParser(MagicMock, repo)
    assert text_parser.get_request_type("newgame", True) == RequestType.NEW_GAME


def test_it_should_handle_load_game_denied_message():
    """Test to ensure a proper response is received when load game is denied."""
    text_parser = TextParser(MagicMock, default_repo())
    result = text_parser.handle_load_game_denied()
    assert any_message_contents(result.messages, "You've chosen not to load a game.")


def test_it_should_confirm_load_game():
    """Test to ensure that it confirms with the user that they wish to load the game."""
    repo = default_repo()
    repo.language.is_confirmed = MagicMock(return_value=True)
    text_parser = TextParser(MagicMock, repo)
    text_parser.print_single_message = MagicMock(
        name="print_single_message", return_value=None
    )
    with patch.object(builtins, "input", return_value="y") as mock_input:
        assert text_parser.confirm_load_game() is True
        text_parser.print_single_message.assert_called()
        mock_input.assert_called_once()


def test_it_should_not_confirm_load_game():
    """Test to ensure that it confirms the user would not like to load the game."""
    repo = default_repo()
    repo.language.is_confirmed = MagicMock(return_value=False)
    text_parser = TextParser(MagicMock, repo)
    text_parser.print_single_message = MagicMock(
        name="print_single_message", return_value=None
    )
    with patch.object(builtins, "input", return_value="no") as mock_input:
        assert text_parser.confirm_load_game() is False
        text_parser.print_single_message.assert_called()
        mock_input.assert_called_once()


def test_it_should_handle_game_input():
    """Test to make sure it can handle input from the game."""
    text_parser = TextParser(MagicMock, default_repo())
    request = GameRequest(RequestType.MOVE, ["up"])
    text_parser.parse_text = MagicMock(name="parse_text", return_value=request)
    text_parser.router = MagicMock(Router)
    text_parser.router.route.return_value = GameResponse.success("You move up.")
    response = text_parser.handle_game_input("move up", True)
    text_parser.router.route.assert_called_once_with(request)
    assert response == RequestStatus.SUCCESS


def test_it_should_handle_game_input_when_load_game_denied():
    """Test to make sure it can handle game input when a load game is denied."""
    text_parser = TextParser(MagicMock, default_repo())
    request = GameRequest(RequestType.LOAD_GAME_DENIED, [""])
    text_parser.parse_text = MagicMock(name="parse_text", return_value=request)
    text_parser.router = MagicMock(Router)
    response = text_parser.handle_game_input("loadgame", False)
    text_parser.router.route.assert_not_called()
    assert response == RequestStatus.FAILURE


def test_handle_user_input_should_handle_load_denied():
    """Test to make sure the handle user input method can handle load denied."""
    text_parser = TextParser(MagicMock, default_repo())
    request = GameRequest(RequestType.LOAD_GAME_DENIED, [None])
    text_parser.print_single_message = MagicMock(
        name="print_single_message", return_value=None
    )
    text_parser.parse_text = MagicMock(name="parse_text", return_value=request)
    text_parser.handle_load_game_denied = MagicMock(
        name="handle_load_game_denied", return_value=None
    )
    with patch.object(builtins, "input", return_value="n") as mock_input:
        text_parser.handle_user_input()
        text_parser.print_single_message.assert_called()
        mock_input.assert_called_once()
        text_parser.handle_load_game_denied.assert_called_once()


def test_print_single_message_can_handle_spaces():
    """Test if the print instructions method can handle spaces in the instructions."""
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.scroll_print = MagicMock(name="scroll_print", return_value=None)
    message = GameMessage.single_line("test instructions")
    text_parser.print_single_message(message, True)
    text_parser.scroll_print.assert_called_once_with("    test instructions")


def test_print_single_message_can_handle_art():
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.scroll_print = MagicMock(name="scroll_print", return_value=None)
    message = GameMessage.art(["test instructions"])
    text_parser.print_single_message(message, False)
    text_parser.scroll_print.assert_called_once_with("test instructions")


def test_print_list_of_messages_should_print_multiple_messages():
    """Test to make sure print_list_of_messages prints two messages."""
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.print_single_message = MagicMock(
        name="print_single_message", return_value=None
    )
    messages = [
        GameMessage.single_line("test"),
        GameMessage.single_line("instructions"),
    ]
    text_parser.print_list_of_messages(messages, False)
    text_parser.print_single_message.assert_has_calls(
        [call(messages[0], False), call(messages[1], False)]
    )


def test_it_should_handle_single_word_requests():
    """Test to make sure it can handle single word requests."""
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.get_request_type = MagicMock(
        name="get_request_type", return_value=RequestType.HELP
    )
    text_parser.find_valid_target = MagicMock(
        name="find_valid_target", return_value=None
    )
    request = text_parser.handle_single_word_request(["help"], True)
    assert request.action == RequestType.HELP
    assert request.targets == [None]


def test_it_should_handle_map_requests():
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.get_request_type = MagicMock(
        name="get_request_type", return_value=RequestType.GAME_MAP
    )
    request = text_parser.handle_single_word_request(["map"], True)
    assert request.action == RequestType.GAME_MAP
    assert request.targets == ["game_map"]


def test_it_should_handle_unknown_move_requests():
    """Test to make sure it treats unknown requests as move requests."""
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.get_request_type = MagicMock(
        name="get_request_type", return_value=RequestType.UNKNOWN
    )
    text_parser.find_valid_target = MagicMock(
        name="find_valid_target", return_value="help"
    )
    request = text_parser.handle_single_word_request(["help"], True)
    assert request.action == RequestType.MOVE
    assert request.targets == ["help"]


def test_it_should_handle_two_word_requests():
    """Test to make sure it can handle two word requests."""

    def get_request_type_mocker(self: Any, words: str, from_user: bool):
        """Mocker for the get_request_type method."""
        if words == "go north":
            return RequestType.UNKNOWN
        else:
            return RequestType.MOVE

    text_parser = TextParser(MagicMock, default_repo())
    with patch.object(TextParser, "get_request_type", get_request_type_mocker):
        text_parser.find_valid_target = MagicMock(
            name="find_valid_target", return_value="north"
        )
        request = text_parser.handle_two_word_request(["go", "north"], True)
        assert request.action == RequestType.MOVE
        assert request.targets == ["north"]


def test_it_should_handle_two_word_map_requests():
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.get_request_type = MagicMock(
        name="get_request_type", return_value=RequestType.GAME_MAP
    )
    request = text_parser.handle_two_word_request(["get", "map"], True)
    assert request.action == RequestType.GAME_MAP
    assert request.targets == ["game_map"]


def test_it_should_handle_two_word_requests_for_location():
    """Test to make sure it can handle two word requests."""

    def get_request_type_mocker(self: Any, words: str, from_user: bool):
        """Mocker for the get_request_type method."""
        if words == "wine cellar":
            return RequestType.UNKNOWN
        else:
            return RequestType.UNKNOWN

    text_parser = TextParser(MagicMock, default_repo())
    with patch.object(TextParser, "get_request_type", get_request_type_mocker):
        text_parser.find_valid_target = MagicMock(
            name="find_valid_target", return_value="wine cellar"
        )
        request = text_parser.handle_two_word_request(["wine", "cellar"], True)
        assert request.action == RequestType.MOVE
        assert request.targets == ["wine cellar"]


def test_it_should_handle_multi_word_requests():
    """Test to make sure it handles long requests."""

    def get_request_type_mocker(self: Any, words: str, from_user: bool):
        """Mocker for the get_request_type method."""
        if words == "go wine":
            return RequestType.UNKNOWN
        else:
            return RequestType.MOVE

    text_parser = TextParser(MagicMock, default_repo())
    with patch.object(TextParser, "get_request_type", get_request_type_mocker):
        text_parser.find_valid_target = MagicMock(
            name="find_valid_target", return_value="wine cellar"
        )
        request = text_parser.handle_multi_word_request(["go", "wine", "cellar"], True)
        assert request.action == RequestType.MOVE
        assert request.targets == ["wine cellar"]


def test_it_should_handle_multiword_map_requests():
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.get_request_type = MagicMock(
        name="get_request_type", return_value=RequestType.GAME_MAP
    )
    request = text_parser.handle_multi_word_request(["get", "my", "map"], True)
    assert request.action == RequestType.GAME_MAP
    assert request.targets == ["game_map"]


def test_it_should_handle_unknown_multi_word_requests():
    """Test to make sure it handles long requests."""

    def get_request_type_mocker(self: Any, words: str, from_user: bool):
        """Mocker for the get_request_type method."""
        return RequestType.UNKNOWN

    text_parser = TextParser(MagicMock, default_repo())
    with patch.object(TextParser, "get_request_type", get_request_type_mocker):
        text_parser.find_valid_target = MagicMock(
            name="find_valid_target", return_value=""
        )
        request = text_parser.handle_multi_word_request(
            ["large", "wine", "cellar"], True
        )
        assert request.action == RequestType.MOVE
        assert request.targets == []


def test_it_should_print_wrapped_text():
    """Test to make sure it prints wrapped text."""
    textwrap.wrap = MagicMock(name="wrap", return_value=["test"])
    repo = default_repo()
    repo.scroll_delay = 0
    text_parser = TextParser(MagicMock, repo)
    message = GameMessage.paragraph("test")
    message.should_wrap = MagicMock(name="should_wrap", return_value=True)
    text_parser.print_single_message(message, False)
    textwrap.wrap.assert_called()


def test_it_should_just_scroll_print():
    """Test to make sure it prints unwrapped text."""
    message = GameMessage.paragraph("test")
    message.should_wrap = MagicMock(name="should_wrap", return_value=False)
    text_parser = TextParser(MagicMock, default_repo())
    text_parser.scroll_print_with_spaces = MagicMock(name="scroll_print_with_spaces")
    text_parser.print_single_message(message, False)
    text_parser.scroll_print_with_spaces.assert_called()


def test_find_all_valid_targets_should_return_a_list_of_targets():
    """Test to make sure that find_all_valid_targets returns a list of targets."""
    text_parser = TextParser(MagicMock, default_repo())

    def mock_find_target(target: str, from_user: bool) -> str | None:
        if target in ["kitchen", "living room", "really long room name"]:
            return target
        return ""

    text_parser.repository.find_target = mock_find_target
    targets = text_parser.find_all_valid_targets(
        ["kitchen", "living", "room", "really", "long", "room", "name"], True
    )
    assert all(
        [
            target in targets
            for target in ["kitchen", "living room", "really long room name"]
        ]
    )


def test_find_all_valid_targets_should_return_an_empty_list():
    """Test to make sure find_all_valid_targets returns an empty list when no
    targets are found."""
    text_parser = TextParser(MagicMock, default_repo())

    def mock_find_target(target: str, from_user: bool) -> str | None:
        return ""

    text_parser.repository.find_target = mock_find_target
    targets = text_parser.find_all_valid_targets(
        ["kitchen", "living", "room", "really", "long", "room", "name"], True
    )
    assert targets == []


def test_it_should_handle_a_two_word_alias_request():
    """Test to make sure it can handle a two word alias request."""
    repo = default_repo()
    repo.find_valid_target = MagicMock(return_value="")

    def mock_get_request_type(self: Any, words: str, from_user: bool) -> RequestType:
        if words == "alias":
            return RequestType.ALIAS
        else:
            return RequestType.UNKNOWN

    text_parser = TextParser(MagicMock, repo)
    text_parser.find_valid_target = MagicMock(return_value="")
    with patch.object(TextParser, "get_request_type", mock_get_request_type):
        request = text_parser.handle_two_word_request(["alias", "test"], True)
        assert request.action == RequestType.ALIAS
        assert request.targets == ["test"]


def test_it_should_handle_a_multi_word_alias_request():
    """Test to make sure it can handle a two word alias request."""
    repo = default_repo()
    repo.find_valid_target = MagicMock(return_value="")

    def mock_get_request_type(self: Any, words: str, from_user: bool) -> RequestType:
        if words == "alias":
            return RequestType.ALIAS
        else:
            return RequestType.UNKNOWN

    text_parser = TextParser(MagicMock, repo)
    text_parser.find_valid_target = MagicMock(return_value="")
    with patch.object(TextParser, "get_request_type", mock_get_request_type):
        request = text_parser.handle_multi_word_request(
            ["alias", "important", "test"], True
        )
        assert request.action == RequestType.ALIAS
        assert request.targets == ["important test"]


def test_it_should_not_error_when_enter_pressed_by_accident():
    """Test to make sure that if a users enters no text, it just reprompts."""
    repo = default_repo()
    repo.find_valid_target = MagicMock(return_value="")
    text_parser = TextParser(MagicMock, repo)
    expected = GameRequest(RequestType.UNKNOWN, [""])
    text_parser.parse_text = MagicMock(return_value=expected)
    text_parser.print_list_of_messages = MagicMock()
    text_parser.print_response = MagicMock()
    text_parser.router = MagicMock(Router)
    text_parser.router.route_request = MagicMock(return_value=expected)
    with patch.object(builtins, "input", return_value=""):
        text_parser.handle_user_input()
        text_parser.print_list_of_messages.assert_called()
        text_parser.print_response.assert_not_called()
        text_parser.router.route_request.assert_not_called()
