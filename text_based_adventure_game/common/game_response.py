"""A response to a game request."""

from common.game_message import GameMessage
from common.request_status import RequestStatus


class GameResponse:
    """A class that represents the game response."""

    def __init__(
        self: "GameResponse", messages: list[GameMessage], status: RequestStatus
    ) -> None:
        """Initialize the game response."""
        self.messages = messages
        self.status = status

    def dictionary(self: "GameResponse") -> dict:
        """Return the dictionary of the game response."""
        return {
            "messages": [str(message) for message in self.messages],
            "status": self.status.name,
        }

    def __repr__(self) -> str:
        """Return the representation of the game response."""
        return str(self.dictionary())

    @staticmethod
    def success(message: str) -> "GameResponse":
        """Return a successful game response."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line(message),
        ]
        return GameResponse(messages, RequestStatus.SUCCESS)

    @staticmethod
    def failure(message: str) -> "GameResponse":
        """Return a failed game response with a blank line above it."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line(message),
        ]
        return GameResponse(messages, RequestStatus.FAILURE)

    @staticmethod
    def success_with_header(header: str, message: str) -> "GameResponse":
        """Return a successful game response with a header."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line(header),
            GameMessage.blank_line(),
            GameMessage.single_line(message),
        ]
        return GameResponse(messages, RequestStatus.SUCCESS)

    @staticmethod
    def failure_with_header(header: str, message: str) -> "GameResponse":
        """Return a failed game response with a header."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line(header),
            GameMessage.blank_line(),
            GameMessage.single_line(message),
        ]
        return GameResponse(messages, RequestStatus.FAILURE)

    @staticmethod
    def success_with_header_and_strings(
        header: str, content: list[str]
    ) -> "GameResponse":
        """Return a successful game response with a header and messages."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.single_line(header),
            GameMessage.blank_line(),
        ]
        for message in content:
            messages.append(GameMessage.single_line(f" - {message}"))
        return GameResponse(messages, RequestStatus.SUCCESS)

    @staticmethod
    def success_with_messages(messages: list[GameMessage]) -> "GameResponse":
        """Return a successful game response with messages."""
        return GameResponse(messages, RequestStatus.SUCCESS)

    @staticmethod
    def failure_with_messages(messages: list[GameMessage]) -> "GameResponse":
        """Return a failed game response with messages."""
        return GameResponse(messages, RequestStatus.FAILURE)

    @staticmethod
    def art(contents: list[str]) -> "GameResponse":
        """Return a game response with literal contents."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.art(contents),
        ]
        return GameResponse(messages, RequestStatus.SUCCESS)
