"""Test the language manager class."""


from unittest.mock import patch

from common.request_type import RequestType
from game_repository.file_manager import FileManager
from language.language_manager import LanguageManager


def mock_language_helper():
    """Language data for testing."""
    return {
        "move_requests": ["go", "move", "walk", "run", "travel", "head"],
        "move_north": ["north", "n", "up", "u"],
        "move_south": ["south", "s", "down", "d"],
        "move_east": ["east", "e", "right", "r"],
        "move_west": ["west", "w", "left", "l"],
        "look_requests": ["look"],
        "inspect_requests": ["look at", "examine", "inspect", "check", "view"],
        "take_requests": ["take", "get", "grab", "steal", "pick up"],
        "drop_requests": ["drop", "trash", "discard", "throw away"],
        "exit_requests": ["exit", "quit", "leave", "end", "stop"],
        "game_story_requests": ["print"],
        "save_requests": ["save", "savegame"],
        "load_requests": ["load", "loadgame"],
        "new_game_requests": ["new", "newgame"],
        "inventory_requests": ["inventory", "items", "tools"],
        "use_requests": ["use"],
        "chew_requests": ["chew", "eat", "taste"],
        "pull_requests": ["pull", "tug", "yank"],
        "play_requests": ["play"],
        "flush_requests": ["flush"],
        "alias": ["alias"],
        "sit_requests": ["sit", "rest", "sit on"],
        "scroll_requests": ["scroll", "text speed", "type"],
        "fast_words": ["fast", "faster", "quick", "quickly", "q", "speed", "s"],
        "medium_words": ["medium", "m", "normal"],
        "slow_words": ["slow", "slower", "sl", "slw"],
        "off_words": ["off", "none"],
        "hints": ["hint", "hints"],
        "game_map": ["map"],
        "climb_requests": ["climb", "scale", "ascend", "clamber"],
        "turn_on_requests": ["turn on", "start", "turn"],
        "open_requests": ["open"],
        "words_to_remove": [
            "a",
            "an",
            "the",
            "in",
            "on",
            "to",
            "from",
            "with",
            "and",
            "or",
            "for",
            "of",
            "",
        ],
        "yes_words": [
            "y",
            "yes",
            "yeah",
            "yep",
            "yup",
            "sure",
            "ok",
            "okay",
            "fine",
            "alright",
            "affirmative",
            "aye",
            "roger",
            "right",
            "indeed",
            "correct",
            "agreed",
            "certainly",
        ],
        "help_requests": ["help", "?"],
        "help_contents": [
            "Move - Move to a new room.",
            "Look - Look around the room.",
            "Inventory - View your inventory.",
            "Take - Take an item from the room and place in your inventory.",
            "Drop - Drop an item out of your inventory into the room.",
            "Inspect - Inspect an item in the room or in your inventory.",
            "Chew - Chew on an item in the room or in your inventory.",
            "Pull - Pull on an item in the room or in your inventory.",
            "Save - Save your game.",
            "Load - Load a saved game.",
            "New - Start a new game. ",
            "Exit - Exit the game. ",
            "Map - View game map.",
            "Hint - Get a hint.",
            "Help - View this help message.",
        ],
        "objective_requests": ["objective", "goal", "objectives", "goals"],
        "clean_requests": [
            "clean",
            "clean up",
            "tidy",
            "tidy up",
            "straighten",
            "straighten up",
            "organize",
            "neaten",
            "neaten up",
        ],
        "drink_requests": ["drink", "sip", "gulp"],
        "draw_requests": ["draw"],
    }


def test_it_should_get_request_types():
    """Test to make sure it can get all of the request types."""
    with patch.object(LanguageManager, "__init__", return_value=None):
        manager = LanguageManager()
        manager.language = mock_language_helper()
        for alias in manager.move_requests:
            assert manager.get_request_type(alias) == RequestType.MOVE
        for alias in manager.look_requests:
            assert manager.get_request_type(alias) == RequestType.LOOK
        for alias in manager.inspect_requests:
            assert manager.get_request_type(alias) == RequestType.INSPECT
        for alias in manager.take_requests:
            assert manager.get_request_type(alias) == RequestType.TAKE
        for alias in manager.drop_requests:
            assert manager.get_request_type(alias) == RequestType.DROP
        for alias in manager.exit_requests:
            assert manager.get_request_type(alias) == RequestType.EXIT
        for alias in manager.game_story_requests:
            assert manager.get_request_type(alias) == RequestType.GAME_STORY
        for alias in manager.save_requests:
            assert manager.get_request_type(alias) == RequestType.SAVE_GAME
        for alias in manager.load_requests:
            assert manager.get_request_type(alias) == RequestType.LOAD_GAME
        for alias in manager.new_game_requests:
            assert manager.get_request_type(alias) == RequestType.NEW_GAME
        for alias in manager.inventory_requests:
            assert manager.get_request_type(alias) == RequestType.INVENTORY
        for alias in manager.help_requests:
            assert manager.get_request_type(alias) == RequestType.HELP
        for alias in manager.yes_words:
            assert manager.is_confirmed(alias) is True
        for alias in manager.use_requests:
            assert manager.get_request_type(alias) == RequestType.USE
        for alias in manager.chew_requests:
            assert manager.get_request_type(alias) == RequestType.CHEW
        for alias in manager.pull_requests:
            assert manager.get_request_type(alias) == RequestType.PULL
        for alias in manager.objective_requests:
            assert manager.get_request_type(alias) == RequestType.OBJECTIVES
        for alias in manager.alias_requests:
            assert manager.get_request_type(alias) == RequestType.ALIAS
        for alias in manager.sit_requests:
            assert manager.get_request_type(alias) == RequestType.SIT
        for alias in manager.scroll_requests:
            assert manager.get_request_type(alias) == RequestType.SCROLL
        for alias in manager.clean_requests:
            assert manager.get_request_type(alias) == RequestType.CLEAN
        for alias in manager.drink_requests:
            assert manager.get_request_type(alias) == RequestType.DRINK
        for alias in manager.game_map:
            assert manager.get_request_type(alias) == RequestType.GAME_MAP
        for alias in manager.hints:
            assert manager.get_request_type(alias) == RequestType.HINT
        for alias in manager.climb_requests:
            assert manager.get_request_type(alias) == RequestType.CLIMB
        for alias in manager.turn_on_requests:
            assert manager.get_request_type(alias) == RequestType.TURN_ON
        for alias in manager.open_requests:
            assert manager.get_request_type(alias) == RequestType.OPEN
        for alias in manager.play_requests:
            assert manager.get_request_type(alias) == RequestType.PLAY
        for alias in manager.flush_requests:
            assert manager.get_request_type(alias) == RequestType.FLUSH
        for alias in manager.draw_requests:
            assert manager.get_request_type(alias) == RequestType.DRAW
        assert manager.unnecessary_words == manager.language["words_to_remove"]
        assert manager.get_request_type("not a request") == RequestType.UNKNOWN


def test_it_should_get_directional_aliases():
    """Test to make sure it handles directional aliases."""
    with patch.object(LanguageManager, "__init__", return_value=None):
        manager = LanguageManager()
        manager.language = mock_language_helper()
        for alias in manager.language["move_north"]:
            assert manager.get_directional_alias(alias) == "north"
        for alias in manager.language["move_south"]:
            assert manager.get_directional_alias(alias) == "south"
        for alias in manager.language["move_east"]:
            assert manager.get_directional_alias(alias) == "east"
        for alias in manager.language["move_west"]:
            assert manager.get_directional_alias(alias) == "west"
        assert manager.get_directional_alias("not a direction") is None


def test_it_should_load_language_data():
    """Test to make sure it loads language data."""
    with patch.object(
        FileManager, "load_language", return_value=mock_language_helper()
    ):
        manager = LanguageManager()
        manager.load_language()
        assert manager.language == mock_language_helper()


def test_it_should_load_help_contents():
    """Test to make sure it loads help contents."""
    manager = LanguageManager()
    manager.language = mock_language_helper()
    assert manager.help_contents == mock_language_helper()["help_contents"]


def test_it_should_load_direction_contents():
    """Test to make sure it loads help contents."""
    manager = LanguageManager()
    manager.language = mock_language_helper()
    assert manager.west_requests == mock_language_helper()["move_west"]
    assert manager.east_requests == mock_language_helper()["move_east"]
    assert manager.north_requests == mock_language_helper()["move_north"]
    assert manager.south_requests == mock_language_helper()["move_south"]


def test_it_should_find_command_targets():
    """Test the find_command_targets method to make sure it works."""
    manager = LanguageManager()
    manager.language = mock_language_helper()
    assert manager.find_command_target("take") == "take"
    assert manager.find_command_target("move") == "move"
    assert manager.find_command_target("look") == "look"
    assert manager.find_command_target("inspect") == "inspect"
    assert manager.find_command_target("drop") == "drop"
    assert manager.find_command_target("exit") == "exit"
    assert manager.find_command_target("save") == "save"
    assert manager.find_command_target("load") == "load"
    assert manager.find_command_target("new") == "new"
    assert manager.find_command_target("inventory") == "inventory"
    assert manager.find_command_target("help") == "help"
    assert manager.find_command_target("use") == "use"
    assert manager.find_command_target("chew") == "chew"
    assert manager.find_command_target("pull") == "pull"
    assert manager.find_command_target("sit") == "sit"
    assert manager.find_command_target("alias") == "alias"
    assert manager.find_command_target("west") == "west"
    assert manager.find_command_target("east") == "east"
    assert manager.find_command_target("north") == "north"
    assert manager.find_command_target("south") == "south"
    assert manager.find_command_target("yes") == "yes"
    assert manager.find_command_target("fast") == "fast"
    assert manager.find_command_target("slow") == "slow"
    assert manager.find_command_target("medium") == "medium"
    assert manager.find_command_target("off") == "off"
    assert manager.find_command_target("scroll") == "scroll"
    assert manager.find_command_target("clean") == "clean"
    assert manager.find_command_target("drink") == "drink"
    assert manager.find_command_target("map") == "game_map"
    assert manager.find_command_target("hint") == "hint"
    assert manager.find_command_target("climb") == "climb"
    assert manager.find_command_target("turn on") == "turn on"
    assert manager.find_command_target("open") == "open"
    assert manager.find_command_target("play") == "play"
    assert manager.find_command_target("flush") == "flush"
    assert manager.find_command_target("not a command") is None


def test_it_should_get_request_type_aliases():
    """Test to make sure it returns a list of aliases for a request type."""
    manager = LanguageManager()
    manager.language = mock_language_helper()
    assert manager.get_request_type_aliases("move") == manager.move_requests
    assert manager.get_request_type_aliases("look") == manager.look_requests
    assert manager.get_request_type_aliases("inspect") == manager.inspect_requests
    assert manager.get_request_type_aliases("take") == manager.take_requests
    assert manager.get_request_type_aliases("drop") == manager.drop_requests
    assert manager.get_request_type_aliases("exit") == manager.exit_requests
    assert manager.get_request_type_aliases("save") == manager.save_requests
    assert manager.get_request_type_aliases("load") == manager.load_requests
    assert manager.get_request_type_aliases("new") == manager.new_game_requests
    assert manager.get_request_type_aliases("inventory") == manager.inventory_requests
    assert manager.get_request_type_aliases("help") == manager.help_requests
    assert manager.get_request_type_aliases("use") == manager.use_requests
    assert manager.get_request_type_aliases("chew") == manager.chew_requests
    assert manager.get_request_type_aliases("pull") == manager.pull_requests
    assert manager.get_request_type_aliases("sit") == manager.sit_requests
    assert manager.get_request_type_aliases("alias") == manager.alias_requests
    assert manager.get_request_type_aliases("west") == manager.west_requests
    assert manager.get_request_type_aliases("east") == manager.east_requests
    assert manager.get_request_type_aliases("north") == manager.north_requests
    assert manager.get_request_type_aliases("south") == manager.south_requests
    assert manager.get_request_type_aliases("yes") == manager.yes_words
    assert manager.get_request_type_aliases("fast") == manager.fast_words
    assert manager.get_request_type_aliases("slow") == manager.slow_words
    assert manager.get_request_type_aliases("medium") == manager.medium_words
    assert manager.get_request_type_aliases("off") == manager.off_words
    assert manager.get_request_type_aliases("scroll") == manager.scroll_requests
    assert manager.get_request_type_aliases("clean") == manager.clean_requests
    assert manager.get_request_type_aliases("drink") == manager.drink_requests
    assert manager.get_request_type_aliases("hint") == manager.hints
    assert manager.get_request_type_aliases("map") == manager.game_map
    assert manager.get_request_type_aliases("climb") == manager.climb_requests
    assert manager.get_request_type_aliases("turn on") == manager.turn_on_requests
    assert manager.get_request_type_aliases("open") == manager.open_requests
    assert manager.get_request_type_aliases("play") == manager.play_requests
    assert manager.get_request_type_aliases("flush") == manager.flush_requests
    assert manager.get_request_type_aliases("not a request") == []
