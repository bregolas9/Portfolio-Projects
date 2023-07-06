"""A text parser that converts human language into game instructions."""

import textwrap
import time

from common.game_message import GameMessage
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.message_type import MessageType
from common.request_status import RequestStatus
from common.request_type import RequestType
from game_repository.game_repository import GameRepository
from router.router import Router


class TextParser:
    """A class that represents the text parser."""

    def __init__(
        self: "TextParser", router: Router, repository: GameRepository
    ) -> None:
        """Initialize the text parser."""
        self.router = router
        self.repository = repository

    def is_empty(self: "TextParser", text: list[str]) -> bool:
        """Return True if the text is empty.

        Args:
            text: The list of strings to check.

        Returns:
            True if the list is empty or the first item is an empty string,
            False otherwise.
        """
        return len(text) == 0 or (len(text) > 0 and text[0] == "")

    def get_request_type(self: "TextParser", text: str, from_user: bool) -> RequestType:
        """Return the request type for the given text.

        Args:
            text: The first word from the user input to check for a request type.
            from_user: True if the text is from the user, False otherwise.

        Returns:
            The request type for the given text.
        """
        request_type = self.repository.language.get_request_type(text.lower())
        if request_type == RequestType.LOAD_GAME:
            if not self.confirm_load_game():
                return RequestType.LOAD_GAME_DENIED
        elif request_type == RequestType.GAME_STORY:
            if from_user:
                return RequestType.UNKNOWN
        elif request_type == RequestType.OBJECTIVES:
            if not self.repository.environment.is_development:
                return RequestType.UNKNOWN
        return request_type

    def parse_text(self: "TextParser", text: str, from_user: bool) -> GameRequest:
        """Parse the given text and return the parsed text.

        Args:
            text: The user input text to be parsed into a game request.
            from_user: True if the text is from the user, False otherwise.

        Returns:
            A GameRequest object with the action and target.
        """
        # split the text into an array of words without the common articles
        # and prepositions
        split_text = self.remove_unnecessary_words(text.split(" "))

        if self.is_empty(split_text):
            return GameRequest(RequestType.UNKNOWN, [""])
        elif len(split_text) == 1:
            return self.handle_single_word_request(split_text, from_user)
        elif len(split_text) == 2:
            return self.handle_two_word_request(split_text, from_user)
        else:
            return self.handle_multi_word_request(split_text, from_user)

    def handle_single_word_request(
        self: "TextParser", words: list[str], from_user: bool
    ) -> GameRequest:
        """Handle a single word request."""
        request_type = self.get_request_type(words[0], from_user)
        if request_type == RequestType.GAME_MAP:
            return GameRequest(request_type, ["game_map"])
        target = None

        # If the request type is unknown, it's possible that the word is a target
        # for movement.
        if request_type == RequestType.UNKNOWN:
            request_type = RequestType.MOVE
            target = self.find_valid_target(words, from_user)

        return GameRequest(request_type, [target])

    def handle_two_word_request(
        self: "TextParser", words: list[str], from_user: bool
    ) -> GameRequest:
        """Handle a two word request."""
        request_type = self.get_request_type(f"{words[0]} {words[1]}", from_user)
        if request_type == RequestType.GAME_MAP:
            return GameRequest(request_type, ["game_map"])
        target = ""
        if request_type == RequestType.UNKNOWN:
            request_type = self.get_request_type(words[0], from_user)
            target = self.find_valid_target(words[1:], from_user)
            if request_type == RequestType.ALIAS and target == "":
                target = words[1]
        if request_type == RequestType.UNKNOWN:
            request_type = RequestType.MOVE
            target = self.find_valid_target(words, from_user)

        return GameRequest(request_type, [target])

    def handle_multi_word_request(
        self: "TextParser", words: list[str], from_user
    ) -> GameRequest:
        """Handle requests that are more than two words long."""
        request_type = self.get_request_type(f"{words[0]} {words[1]}", from_user)
        if request_type == RequestType.GAME_MAP:
            return GameRequest(request_type, ["game_map"])
        targets = self.find_all_valid_targets(words[2:], from_user)
        if request_type == RequestType.UNKNOWN:
            request_type = self.get_request_type(words[0], from_user)
            targets = self.find_all_valid_targets(words[1:], from_user)
            if request_type == RequestType.ALIAS and len(targets) == 0:
                targets = [" ".join(words[1:])]
        if request_type == RequestType.UNKNOWN:
            request_type = RequestType.MOVE
            targets = self.find_all_valid_targets(words, from_user)

        return GameRequest(request_type, targets)  # type: ignore

    def find_all_valid_targets(
        self: "TextParser", words: list[str], from_user: bool
    ) -> list[str | None]:
        """Return a list of all the valid targets present in the given list of words."""
        word_count = len(words)
        min_word = 0
        max_word = word_count
        targets = []
        while word_count > 0:
            target = self.find_valid_target(words[min_word:max_word], from_user)
            if target != "":
                targets.append(target)
                words = words[:min_word] + words[max_word:]
                word_count = len(words)
                min_word = 0
                max_word = word_count
                continue
            if max_word == len(words):
                min_word = 0
                max_word = word_count - 1
                word_count = max_word
            else:
                min_word += 1
                max_word += 1
        return targets

    def remove_unnecessary_words(self: "TextParser", words: list[str]) -> list[str]:
        """Return the given list of words without articles.

        Args:
            words: The list of words to remove articles from.

        Returns:
            The given list of words without articles.
        """
        words_to_remove = self.repository.language.unnecessary_words
        return list(filter(lambda word: word.lower() not in words_to_remove, words))

    def find_valid_target(self: "TextParser", words: list[str], from_user: bool) -> str:
        """Check the list of words for a valid target.

        Args:
            words: The list of words to check for a valid target.

        Returns:
            The name of a valid target if it exists, otherwise None.
        """
        if len(words) == 0:
            return ""
        elif len(words) == 1:
            target = self.repository.find_target(words[0].lower(), from_user)
            return "" if target is None else target.lower()
        else:
            target = self.repository.find_target(" ".join(words).lower(), from_user)
            return "" if target is None else target.lower()

    def handle_user_input(self: "TextParser") -> None:
        """Request input from the user and handle the input."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line("What would you like to do?"),
        ]
        self.print_list_of_messages(messages, False)
        user_input = input("    ")
        request = self.parse_text(user_input.strip(), True)
        if request.action == RequestType.UNKNOWN and request.targets == [""]:
            return
        if request.action == RequestType.LOAD_GAME_DENIED:
            self.handle_load_game_denied()
            return
        response = self.router.route(request)
        self.print_response(response, True)

    def scroll_print(self: "TextParser", text: str) -> None:
        """Print the text to the console as if it's being typed.

        Args:
            text: The text to print.

        Returns:
            None
        """
        for character in text:
            print(character, end="", flush=True)
            if not self.repository.environment.is_development:
                time.sleep(self.repository.scroll_delay)
        print()

    def print_response(
        self: "TextParser", game_response: GameResponse, add_spaces: bool
    ) -> None:
        """Print the response text in a consistent way.

        Args:
            game_response: The GameResponse object to print.

        Returns:
            None
        """
        self.print_list_of_messages(game_response.messages, add_spaces)

    def print_list_of_messages(
        self: "TextParser", messages: list[GameMessage], add_spaces: bool
    ) -> None:
        """Print a list of messages."""
        for message in messages:
            self.print_single_message(message, add_spaces)

    def print_single_message(
        self: "TextParser", message: GameMessage, add_spaces: bool
    ) -> None:
        """Print a GameResponse message that is only a string."""
        if message.should_print_blank_line():
            print()
        elif message.should_wrap():
            wrapped_message = textwrap.wrap(str(message), width=80)
            for line in wrapped_message:
                self.scroll_print_with_spaces(line, add_spaces)
        elif message.message_type == MessageType.ART:
            old_delay = self.repository.scroll_delay
            self.repository.scroll_delay = GameRepository.art_scroll_delay
            for line in message.contents:
                self.scroll_print_with_spaces(line, add_spaces)
            self.repository.scroll_delay = old_delay
        else:
            self.scroll_print_with_spaces(str(message), add_spaces)

    def scroll_print_with_spaces(
        self: "TextParser", message: str, with_spaces: bool
    ) -> None:
        """Scroll print the message with spaces if desired."""
        if with_spaces:
            self.scroll_print(f"    {message}")
        else:
            self.scroll_print(message)

    def display_look_request_on_startup(self: "TextParser") -> None:
        """When the game first starts up, the user should see the room description."""
        request = GameRequest(RequestType.LOOK, [None])
        response = self.router.route(request)
        self.print_response(response, True)

    def handle_game_input(
        self: "TextParser", game_input: str, add_spaces: bool
    ) -> RequestStatus:
        """Handle printing from the AdventureGame class."""
        request = self.parse_text(game_input.strip(), False)
        if request.action == RequestType.LOAD_GAME_DENIED:
            result = self.handle_load_game_denied()
            self.print_response(result, add_spaces)
            return result.status
        result = self.router.route(request)
        self.print_response(result, add_spaces)
        return result.status

    def confirm_load_game(self: "TextParser") -> bool:
        """Confirm with the user that they want to load a game.

        Returns:
            True if the user wants to load a game, otherwise False.
        """
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line("Are you sure you want to load a saved game?"),
        ]
        self.print_list_of_messages(messages, False)
        user_input = input("    ")
        return self.repository.language.is_confirmed(user_input.lower())

    def handle_load_game_denied(self: "TextParser") -> GameResponse:
        """Handle the user choosing not to load a game."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line("You've chosen not to load a game."),
        ]
        return GameResponse(messages, RequestStatus.FAILURE)
