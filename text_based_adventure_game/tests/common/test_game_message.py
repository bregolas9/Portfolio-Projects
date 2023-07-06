"""Test the game message object."""

from common.game_message import GameMessage
from common.message_type import MessageType


def test_it_should_handle_lists_of_strings():
    """Test that the game message object can handle lists of strings."""
    message = GameMessage(MessageType.SINGLE_LINE, ["Hello", "World"])
    assert str(message) == "Hello World"

    message = GameMessage(MessageType.BLANK_LINE, ["Hello", "World"])
    assert str(message) == ""

    message = GameMessage(MessageType.PARAGRAPH, ["Hello", "World"])
    assert str(message) == "Hello World"

    message = GameMessage(MessageType.ART, ["Hello", "World"])
    assert str(message) == "Hello\nWorld"


def test_it_should_handle_single_strings():
    """Test that the game message object can handle single strings."""
    message = GameMessage(MessageType.SINGLE_LINE, "Hello World")
    assert str(message) == "Hello World"

    message = GameMessage(MessageType.BLANK_LINE, "Hello World")
    assert str(message) == ""

    message = GameMessage(MessageType.PARAGRAPH, "Hello World")
    assert str(message) == "Hello World"


def test_if_it_should_wrap():
    """Test to make sure the game message object wraps correctly."""
    message = GameMessage(MessageType.SINGLE_LINE, "A" * 100)
    assert str(message) == "A" * 100
    assert message.should_wrap()
    message = GameMessage(MessageType.PARAGRAPH, ["A" * 100])
    assert message.should_wrap()


def test_it_should_have_dict():
    """Test to make sure the dict method works correctly."""
    message = GameMessage(MessageType.SINGLE_LINE, "Hello World")
    assert message.dictionary() == {
        "message_type": MessageType.SINGLE_LINE.name,
        "contents": "Hello World",
    }


def test_repr_works():
    """Test to make sure that the repr method works correctly."""
    message = GameMessage(MessageType.SINGLE_LINE, "Hello World")
    assert message.__repr__() == str(message.dictionary())


def test_literal_works():
    message = GameMessage.art(["test"])
    assert message.message_type == MessageType.ART
    assert message.contents == ["test"]
