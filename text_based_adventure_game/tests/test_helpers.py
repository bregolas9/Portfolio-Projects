"""Helpful methods for testing."""

from common.game_message import GameMessage


def any_message_contents(messages: list[GameMessage], test_message: str) -> bool:
    """Test if a message is in the contents of a response."""
    results = []
    for message in messages:
        if isinstance(message.contents, str):
            results.append(test_message in message.contents)
    return any(results)
