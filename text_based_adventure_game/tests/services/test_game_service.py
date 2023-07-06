"""Test the game service to ensure it performs correctly."""


from unittest.mock import MagicMock, PropertyMock

from common.environment import Environment
from common.game_objective import GameObjective
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.item import Item
from common.player import Player
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.room import Room
from game_repository.art_manager import ArtManager
from game_repository.game_repository import GameRepository
from game_repository.item_manager import ItemManager
from game_repository.objectives_manager import ObjectiveManager
from language.language_manager import LanguageManager
from language.story_manager import StoryManager
from services.game_service import GameService
from tests.test_helpers import any_message_contents


def test_game_service_should_update_game_active_flag():
    """The game service should update the game active flag."""
    mock_repository = MagicMock(GameRepository)
    game_service = GameService(mock_repository)
    mock_repository.game_active = PropertyMock(return_value=True)
    game_service.exit(GameRequest(RequestType.EXIT, ["a message"]))
    assert mock_repository.game_active is False


def test_game_service_should_return_game_stories():
    """The game service should find and return stories."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.stories = MagicMock(StoryManager)
    mock_repository.stories.get_story = MagicMock(
        return_value=["here is an introduction"]
    )
    game_service = GameService(mock_repository)
    request = GameRequest(RequestType.GAME_STORY, ["introduction"])
    response = game_service.game_story(request)
    assert any_message_contents(response.messages, "here is an introduction")
    assert response.status == RequestStatus.SUCCESS


def test_game_service_save_game_method_should_fail_when_raises():
    """Test the save game method of the game service."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.save_game_state = MagicMock(side_effect=Exception("error"))
    expected_response = GameResponse.failure(
        "An error occurred while saving your game: error"
    )
    game_service = GameService(mock_repository)
    result = game_service.save_game(GameRequest(RequestType.SAVE_GAME, ["a message"]))
    assert any_message_contents(
        result.messages, "An error occurred while saving your game: error"
    )
    assert result.status == expected_response.status


def test_game_service_save_game_method_should_pass_when_ok():
    """Test the save game method of the game service for a successful save."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.save_game_state = MagicMock()
    expected_response = GameResponse.success("Your game was saved successfully.")
    game_service = GameService(mock_repository)
    result = game_service.save_game(GameRequest(RequestType.SAVE_GAME, ["a message"]))
    assert any_message_contents(result.messages, "Your game was saved successfully.")
    assert result.status == expected_response.status
    mock_repository.save_game_state.assert_called_once()


def test_load_game_should_succeed():
    """Load game method should call load_game_state and return success response."""
    mock_repository = MagicMock(GameRepository)
    response = GameResponse.success("Game loaded.")
    mock_repository.try_load_game_state = MagicMock(return_value=response)
    game_service = GameService(mock_repository)
    result = game_service.load_game(
        GameRequest(RequestType.LOAD_GAME, ["a message"]), False
    )
    assert any_message_contents(result.messages, "Game loaded.")
    assert result.status == RequestStatus.SUCCESS
    mock_repository.try_load_game_state.assert_called_once()


def test_new_game_should_succeed():
    """New game method should call new_game_state and return success response."""
    mock_repository = MagicMock(GameRepository)
    response = GameResponse.success("A new game has been started.")
    mock_repository.try_load_game_state = MagicMock(return_value=response)
    game_service = GameService(mock_repository)
    result = game_service.load_game(
        GameRequest(RequestType.NEW_GAME, ["a message"]), True
    )
    assert any_message_contents(result.messages, "A new game has been started.")
    assert result.status == RequestStatus.SUCCESS
    mock_repository.try_load_game_state.assert_called_once()


def test_game_service_should_be_helpful():
    """The help method should return valid commands."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.language.help_contents = ["HELP", "CONTENTS"]
    service = GameService(mock_repository)
    request = GameRequest(RequestType.HELP, [])
    response = service.provide_help(request)
    assert any_message_contents(response.messages, "Available Commands:")
    assert any_message_contents(response.messages, " - HELP")
    assert any_message_contents(response.messages, " - CONTENTS")


def test_it_should_return_failure_when_no_game_story_exists():
    """Test to make sure it returns a failed status when a game story doesn't exist."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.stories = MagicMock(StoryManager)
    mock_repository.stories.get_story = MagicMock(return_value=None)

    game_service = GameService(mock_repository)
    request = GameRequest(RequestType.GAME_STORY, ["introduction"])

    response = game_service.game_story(request)

    assert any_message_contents(response.messages, "No story found.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_fail_when_a_game_story_request_targets_empty():
    """Make sure it fails when a game story request targets list is empty."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.stories = MagicMock(StoryManager)
    mock_repository.stories.get_story = MagicMock(return_value=None)
    game_service = GameService(mock_repository)
    request = GameRequest(RequestType.GAME_STORY, [])
    response = game_service.game_story(request)
    assert any_message_contents(response.messages, "No story found.")
    assert response.status == RequestStatus.FAILURE


def test_it_should_list_objectives():
    """Make sure it can list objectives."""
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(GameRepository)
    mock_repository.player.inventory = []
    mock_repository.player.location = MagicMock(Room)
    mock_repository.player.location.inventory = []
    mock_repository.objectives = MagicMock(ObjectiveManager)
    objective = GameObjective("objective1", [], ["requirement1"], [])
    mock_repository.objectives.objectives = {"objective1": objective}
    mock_repository.environment = MagicMock(Environment)
    mock_repository.environment.is_development = True
    game_service = GameService(mock_repository)
    request = GameRequest(RequestType.OBJECTIVES, [])
    response = game_service.list_objective(request)
    assert any_message_contents(response.messages, "objective1 - complete: False")


def test_it_should_get_alias_responses():
    """Test to make sure the get_alias_response method works."""
    aliases = ["one", "two", "three"]
    item_name = "numbers"
    mock_repository = MagicMock(GameRepository)
    game_service = GameService(mock_repository)
    response = game_service.get_alias_response(aliases, item_name)
    assert any_message_contents(response.messages, "Aliases for 'numbers':")
    assert any_message_contents(response.messages, " - one")
    assert any_message_contents(response.messages, " - two")
    assert any_message_contents(response.messages, " - three")


def test_it_should_not_get_alias_response_when_empty():
    """Test to make sure it returns a failed response when the list is empty."""
    aliases = []
    item_name = "numbers"
    mock_repository = MagicMock(GameRepository)
    game_service = GameService(mock_repository)
    response = game_service.get_alias_response(aliases, item_name)
    assert any_message_contents(response.messages, "No aliases found for 'numbers'.")


def test_it_should_give_other_aliases():
    """Test to make sure the give_aliases method works for commands that aren't items and rooms."""
    request = GameRequest(RequestType.ALIAS, ["help"])
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.location = MagicMock(Room)
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.find_target = MagicMock(return_value="help")
    mock_repository.get_room_by_name = MagicMock(return_value=None)
    mock_repository.items.get_item_by_name_by_room = MagicMock(return_value=None)
    mock_repository.language.get_request_type_aliases = MagicMock(return_value=["help"])
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "Aliases for 'help':")
    assert any_message_contents(response.messages, " - help")


def test_it_should_give_item_aliases():
    """Test to make sure the give_aliases method works for items."""
    request = GameRequest(RequestType.ALIAS, ["item"])
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.location = MagicMock(Room)
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.find_target = MagicMock(return_value="item")
    mock_repository.get_room_by_name = MagicMock(return_value=None)
    item = MagicMock(Item)
    item.name = "item"
    item.alias = ["item", "another word for item"]
    mock_repository.items.get_item_by_name_by_room = MagicMock(return_value=item)
    mock_repository.language.get_request_type_aliases = MagicMock(return_value=None)
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "Aliases for 'item':")
    assert any_message_contents(response.messages, " - item")
    assert any_message_contents(response.messages, " - another word for item")


def test_it_should_give_room_aliases():
    """Test to make sure the give_aliases method works for rooms."""
    request = GameRequest(RequestType.ALIAS, ["room"])
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.location = MagicMock(Room)
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.find_target = MagicMock(return_value="room")
    room = MagicMock(Room)
    room.name = "room"
    room.aliases = ["room", "another word for room"]
    mock_repository.get_room_by_name = MagicMock(return_value=room)
    mock_repository.items.get_item_by_name_by_room = MagicMock(return_value=None)
    mock_repository.language.get_request_type_aliases = MagicMock(return_value=None)
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "Aliases for 'room':")
    assert any_message_contents(response.messages, " - room")
    assert any_message_contents(response.messages, " - another word for room")


def test_it_should_fail_to_give_aliases_when_empty():
    """Test to make sure it fails when the list of targets is empty."""
    request = GameRequest(RequestType.ALIAS, [])
    mock_repository = MagicMock(GameRepository)
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Please provide an alias to get help for."
    )


def test_it_should_not_get_aliases_when_not_found():
    """Test to make sure the give_aliases method fails when no valid alias targets are found."""
    request = GameRequest(RequestType.ALIAS, ["room"])
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.location = MagicMock(Room)
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.find_target = MagicMock(return_value=None)
    mock_repository.get_room_by_name = MagicMock(return_value=None)
    mock_repository.items.get_item_by_name_by_room = MagicMock(return_value=None)
    mock_repository.language.get_request_type_aliases = MagicMock(return_value=[])
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Unable to find an alias for 'room'."
    )


def test_it_should_not_get_aliases_when_list_of_none():
    """Test to make sure the give_aliases method fails when a list of None objects are the target."""
    request = GameRequest(RequestType.ALIAS, [None])
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.location = MagicMock(Room)
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.find_target = MagicMock(return_value=None)
    mock_repository.get_room_by_name = MagicMock(return_value=None)
    mock_repository.items.get_item_by_name_by_room = MagicMock(return_value=None)
    mock_repository.language.get_request_type_aliases = MagicMock(return_value=[])
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Please provide an alias to get help for."
    )


def test_it_should_provide_an_alias_not_found_response():
    """Test to make sure the not found response method works."""
    repo = MagicMock(GameRepository)
    service = GameService(repo)
    response = service.alias_not_found_response("test")
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Unable to find an alias for 'test'."
    )


def test_it_should_not_get_aliases_when_not_found_but_find_target_found():
    """Test to make sure the give_aliases method fails when no valid alias targets are found."""
    request = GameRequest(RequestType.ALIAS, ["room"])
    mock_repository = MagicMock(GameRepository)
    mock_repository.player = MagicMock(Player)
    mock_repository.player.location = MagicMock(Room)
    mock_repository.items = MagicMock(ItemManager)
    mock_repository.language = MagicMock(LanguageManager)
    mock_repository.find_target = MagicMock(return_value="room")
    mock_repository.get_room_by_name = MagicMock(return_value=None)
    mock_repository.items.get_item_by_name_by_room = MagicMock(return_value=None)
    mock_repository.language.get_request_type_aliases = MagicMock(return_value=[])
    service = GameService(mock_repository)
    response = service.give_aliases(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Unable to find an alias for 'room'."
    )


def test_it_should_scroll_slowly():
    """Test to make sure the scroll speed changes to slow."""
    request = GameRequest(RequestType.SCROLL, ["slow"])
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.scroll(request)
    assert response.status == RequestStatus.SUCCESS
    assert repo.scroll_delay == GameRepository.slow_scroll_delay


def test_it_should_scroll_normally():
    """Test to make sure the scroll speed changes to normal/medium."""
    request = GameRequest(RequestType.SCROLL, ["medium"])
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.scroll(request)
    assert response.status == RequestStatus.SUCCESS
    assert repo.scroll_delay == GameRepository.normal_scroll_delay


def test_it_should_scroll_fast():
    """Test to make sure the scroll speed changes to fast."""
    request = GameRequest(RequestType.SCROLL, ["fast"])
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.scroll(request)
    assert response.status == RequestStatus.SUCCESS
    assert repo.scroll_delay == GameRepository.fast_scroll_delay


def test_it_should_turn_scrolling_off():
    """Test to make sure the scroll speed changes to off."""
    request = GameRequest(RequestType.SCROLL, ["off"])
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.scroll(request)
    assert response.status == RequestStatus.SUCCESS
    assert repo.scroll_delay == GameRepository.off_scroll_delay


def test_it_should_not_change_scrolling_if_invalid_request():
    """Test to make sure it fails correctly."""
    request = GameRequest(RequestType.SCROLL, ["invalid"])
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.scroll(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(response.messages, "Text printing speed not changed.")


def test_it_should_not_change_scrolling_if_no_request():
    """Test to make sure a None request fails correctly."""
    request = GameRequest(RequestType.SCROLL, [None])
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.scroll(request)
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Please provide a valid scroll speed to change to."
    )


def test_it_should_handle_map_requests():
    request = GameRequest(RequestType.GAME_MAP, ["game_map"])
    repo = MagicMock(GameRepository)
    repo.art_manager = MagicMock(ArtManager)
    repo.art_manager.art = {"game_map": ["map"]}
    repo.art_manager.get_art_by_name = MagicMock(return_value=["map"])
    service = GameService(repo)
    response = service.draw(request)
    assert response.status == RequestStatus.SUCCESS
    assert response.messages[1].contents == ["map"]


def test_it_should_get_hints():
    objective1 = GameObjective("test1", ["hint1"], [], [])
    objective2 = GameObjective("test2", ["hint2"], [], [])
    objective1.is_complete = MagicMock(return_value=False)
    objective2.is_complete = MagicMock(return_value=False)
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.objectives = {"test1": objective1, "test2": objective2}
    repo.player = MagicMock(Player)
    service = GameService(repo)
    response = service.get_hints(MagicMock())
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "hint1")
    assert any_message_contents(response.messages, "You begin to ponder deeply:")


def test_it_should_get_hints2():
    objective1 = GameObjective("test1", ["hint1"], [], [])
    objective2 = GameObjective("test2", ["hint2"], [], [])
    objective1.is_complete = MagicMock(return_value=True)
    objective2.is_complete = MagicMock(return_value=False)
    repo = MagicMock(GameRepository)
    repo.objectives = MagicMock(ObjectiveManager)
    repo.objectives.objectives = {"test1": objective1, "test2": objective2}
    repo.player = MagicMock(Player)
    service = GameService(repo)
    response = service.get_hints(MagicMock())
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "hint2")
    assert any_message_contents(response.messages, "You begin to ponder deeply:")


def test_get_scroll_speed_update_description():
    """Test to make sure the scroll speed update description works correctly."""
    repo = MagicMock(GameRepository)
    repo.language = MagicMock(LanguageManager)
    repo.language.fast_words = ["fast"]
    repo.language.slow_words = ["slow"]
    repo.language.medium_words = ["medium"]
    repo.language.off_words = ["off"]
    repo.scroll_delay = 1
    service = GameService(repo)
    response = service.get_scroll_speed_update_description("invalid")
    assert response == "Text printing speed not changed."
