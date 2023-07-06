"""A class designed to handle the language of the game."""

from common.request_type import RequestType
from game_repository.file_manager import FileManager


class LanguageManager:
    """Manages the language of the game."""

    def __init__(self: "LanguageManager") -> None:
        """Initialize the language manager."""
        self.language: dict[str, list[str]] = dict()

    def load_language(self: "LanguageManager") -> None:
        """Load the language file."""
        self.language = FileManager.load_language()

    def find_command_target(self: "LanguageManager", command: str) -> str | None:
        """Find the target of the command."""
        if command in self.move_requests:
            return "move"
        elif command in self.look_requests:
            return "look"
        elif command in self.take_requests:
            return "take"
        elif command in self.drop_requests:
            return "drop"
        elif command in self.exit_requests:
            return "exit"
        elif command in self.inspect_requests:
            return "inspect"
        elif command in self.save_requests:
            return "save"
        elif command in self.load_requests:
            return "load"
        elif command in self.new_game_requests:
            return "new"
        elif command in self.inventory_requests:
            return "inventory"
        elif command in self.help_requests:
            return "help"
        elif command in self.use_requests:
            return "use"
        elif command in self.chew_requests:
            return "chew"
        elif command in self.pull_requests:
            return "pull"
        elif command in self.alias_requests:
            return "alias"
        elif command in self.sit_requests:
            return "sit"
        elif command in self.west_requests:
            return "west"
        elif command in self.east_requests:
            return "east"
        elif command in self.south_requests:
            return "south"
        elif command in self.north_requests:
            return "north"
        elif command in self.yes_words:
            return "yes"
        elif command in self.fast_words:
            return "fast"
        elif command in self.medium_words:
            return "medium"
        elif command in self.slow_words:
            return "slow"
        elif command in self.scroll_requests:
            return "scroll"
        elif command in self.off_words:
            return "off"
        elif command in self.clean_requests:
            return "clean"
        elif command in self.drink_requests:
            return "drink"
        elif command in self.hints:
            return "hint"
        elif command in self.game_map:
            return "game_map"
        elif command in self.climb_requests:
            return "climb"
        elif command in self.turn_on_requests:
            return "turn on"
        elif command in self.open_requests:
            return "open"
        elif command in self.play_requests:
            return "play"
        elif command in self.flush_requests:
            return "flush"
        return None

    def get_request_type_aliases(self: "LanguageManager", item_name) -> list[str]:
        """Get aliases for a request type."""
        if item_name in self.help_requests:
            return self.help_requests
        if item_name in self.move_requests:
            return self.move_requests
        if item_name in self.inspect_requests:
            return self.inspect_requests
        if item_name in self.look_requests:
            return self.look_requests
        if item_name in self.take_requests:
            return self.take_requests
        if item_name in self.drop_requests:
            return self.drop_requests
        if item_name in self.exit_requests:
            return self.exit_requests
        if item_name in self.save_requests:
            return self.save_requests
        if item_name in self.load_requests:
            return self.load_requests
        if item_name in self.new_game_requests:
            return self.new_game_requests
        if item_name in self.chew_requests:
            return self.chew_requests
        if item_name in self.pull_requests:
            return self.pull_requests
        if item_name in self.yes_words:
            return self.yes_words
        if item_name in self.west_requests:
            return self.west_requests
        if item_name in self.east_requests:
            return self.east_requests
        if item_name in self.north_requests:
            return self.north_requests
        if item_name in self.south_requests:
            return self.south_requests
        if item_name in self.sit_requests:
            return self.sit_requests
        if item_name in self.use_requests:
            return self.use_requests
        if item_name in self.alias_requests:
            return self.alias_requests
        if item_name in self.inventory_requests:
            return self.inventory_requests
        if item_name in self.fast_words:
            return self.fast_words
        if item_name in self.slow_words:
            return self.slow_words
        if item_name in self.medium_words:
            return self.medium_words
        if item_name in self.scroll_requests:
            return self.scroll_requests
        if item_name in self.off_words:
            return self.off_words
        if item_name in self.clean_requests:
            return self.clean_requests
        if item_name in self.drink_requests:
            return self.drink_requests
        if item_name in self.hints:
            return self.hints
        if item_name in self.game_map:
            return self.game_map
        if item_name in self.climb_requests:
            return self.climb_requests
        if item_name in self.turn_on_requests:
            return self.turn_on_requests
        if item_name in self.open_requests:
            return self.open_requests
        if item_name in self.play_requests:
            return self.play_requests
        if item_name in self.flush_requests:
            return self.flush_requests
        return []

    def get_request_type(self: "LanguageManager", request_text: str) -> RequestType:
        """Convert the request text to a request type."""
        if request_text in self.move_requests:
            return RequestType.MOVE
        elif request_text in self.look_requests:
            return RequestType.LOOK
        elif request_text in self.take_requests:
            return RequestType.TAKE
        elif request_text in self.drop_requests:
            return RequestType.DROP
        elif request_text in self.exit_requests:
            return RequestType.EXIT
        elif request_text in self.inspect_requests:
            return RequestType.INSPECT
        elif request_text in self.save_requests:
            return RequestType.SAVE_GAME
        elif request_text in self.load_requests:
            return RequestType.LOAD_GAME
        elif request_text in self.new_game_requests:
            return RequestType.NEW_GAME
        elif request_text in self.inventory_requests:
            return RequestType.INVENTORY
        elif request_text in self.game_story_requests:
            return RequestType.GAME_STORY
        elif request_text in self.help_requests:
            return RequestType.HELP
        elif request_text in self.use_requests:
            return RequestType.USE
        elif request_text in self.chew_requests:
            return RequestType.CHEW
        elif request_text in self.pull_requests:
            return RequestType.PULL
        elif request_text in self.objective_requests:
            return RequestType.OBJECTIVES
        elif request_text in self.alias_requests:
            return RequestType.ALIAS
        elif request_text in self.sit_requests:
            return RequestType.SIT
        elif request_text in self.scroll_requests:
            return RequestType.SCROLL
        elif request_text in self.clean_requests:
            return RequestType.CLEAN
        elif request_text in self.drink_requests:
            return RequestType.DRINK
        elif request_text in self.hints:
            return RequestType.HINT
        elif request_text in self.game_map:
            return RequestType.GAME_MAP
        elif request_text in self.climb_requests:
            return RequestType.CLIMB
        elif request_text in self.turn_on_requests:
            return RequestType.TURN_ON
        elif request_text in self.open_requests:
            return RequestType.OPEN
        elif request_text in self.play_requests:
            return RequestType.PLAY
        elif request_text in self.flush_requests:
            return RequestType.FLUSH
        elif request_text in self.draw_requests:
            return RequestType.DRAW
        else:
            return RequestType.UNKNOWN

    def get_directional_alias(self: "LanguageManager", direction: str) -> str | None:
        """Get the directional name for given aliases."""
        if direction in self.language["move_north"]:
            return "north"
        elif direction in self.language["move_south"]:
            return "south"
        elif direction in self.language["move_east"]:
            return "east"
        elif direction in self.language["move_west"]:
            return "west"
        else:
            return None

    def is_confirmed(self: "LanguageManager", confirmation: str | None) -> bool:
        """Check if the confirmation is valid."""
        return False if confirmation is None else confirmation in self.yes_words

    @property
    def move_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid move requests."""
        return self.language.get("move_requests", [])

    @property
    def look_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid look requests."""
        return self.language.get("look_requests", [])

    @property
    def take_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid take requests."""
        return self.language.get("take_requests", [])

    @property
    def drop_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid drop requests."""
        return self.language.get("drop_requests", [])

    @property
    def exit_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid exit requests."""
        return self.language.get("exit_requests", [])

    @property
    def game_story_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid game story requests."""
        return self.language.get("game_story_requests", [])

    @property
    def inspect_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid inspect requests."""
        return self.language.get("inspect_requests", [])

    @property
    def unnecessary_words(self: "LanguageManager") -> list[str]:
        """Return the list of unnecessary words."""
        return self.language.get("words_to_remove", [])

    @property
    def inventory_requests(self: "LanguageManager") -> list[str]:
        """Return the list of inventory requests."""
        return self.language.get("inventory_requests", [])

    @property
    def save_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid save requests."""
        return self.language.get("save_requests", [])

    @property
    def load_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid load requests."""
        return self.language.get("load_requests", [])

    @property
    def new_game_requests(self: "LanguageManager") -> list[str]:
        """Return the list of valid new game requests."""
        return self.language.get("new_game_requests", [])

    @property
    def yes_words(self: "LanguageManager") -> list[str]:
        """Return the list of words which could mean yes."""
        return self.language.get("yes_words", [])

    @property
    def help_requests(self: "LanguageManager") -> list[str]:
        """Return the list of words which could mean help."""
        return self.language.get("help_requests", [])

    @property
    def use_requests(self: "LanguageManager") -> list[str]:
        """Return the list of words which could mean use."""
        return self.language.get("use_requests", [])

    @property
    def chew_requests(self: "LanguageManager") -> list[str]:
        """Return the list of words which could mean chew."""
        return self.language.get("chew_requests", [])

    @property
    def sit_requests(self: "LanguageManager") -> list[str]:
        """Return the list of words which could mean chew."""
        return self.language.get("sit_requests", [])

    @property
    def pull_requests(self: "LanguageManager") -> list[str]:
        """Return the list of words which could mean pull."""
        return self.language.get("pull_requests", [])

    @property
    def help_contents(self: "LanguageManager") -> list[str]:
        """The list of commands and their descriptions."""
        return self.language.get("help_contents", [])

    @property
    def objective_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean objective."""
        return self.language.get("objective_requests", [])

    @property
    def alias_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean alias."""
        return self.language.get("alias", [])

    @property
    def west_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean west."""
        return self.language.get("move_west", [])

    @property
    def north_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean north."""
        return self.language.get("move_north", [])

    @property
    def east_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean east."""
        return self.language.get("move_east", [])

    @property
    def south_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean south."""
        return self.language.get("move_south", [])

    @property
    def fast_words(self: "LanguageManager") -> list[str]:
        """The list of words which could mean fast."""
        return self.language.get("fast_words", [])

    @property
    def slow_words(self: "LanguageManager") -> list[str]:
        """The list of words which could mean slow."""
        return self.language.get("slow_words", [])

    @property
    def medium_words(self: "LanguageManager") -> list[str]:
        """The list of words which could mean medium."""
        return self.language.get("medium_words", [])

    @property
    def off_words(self: "LanguageManager") -> list[str]:
        """The list of words which could mean off."""
        return self.language.get("off_words", [])

    @property
    def scroll_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean scroll."""
        return self.language.get("scroll_requests", [])

    @property
    def clean_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean clean."""
        return self.language.get("clean_requests", [])

    @property
    def drink_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean drink."""
        return self.language.get("drink_requests", [])

    @property
    def hints(self: "LanguageManager") -> list[str]:
        """The list of words which could mean drink."""
        return self.language.get("hints", [])

    @property
    def game_map(self: "LanguageManager") -> list[str]:
        """The list of words which could mean drink."""
        return self.language.get("game_map", [])

    @property
    def climb_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean climb."""
        return self.language.get("climb_requests", [])

    @property
    def turn_on_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean turn on."""
        return self.language.get("turn_on_requests", [])

    @property
    def open_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean open."""
        return self.language.get("open_requests", [])

    @property
    def play_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean play."""
        return self.language.get("play_requests", [])

    @property
    def flush_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean flush."""
        return self.language.get("flush_requests", [])

    @property
    def draw_requests(self: "LanguageManager") -> list[str]:
        """The list of words which could mean draw."""
        return self.language.get("draw_requests", [])
