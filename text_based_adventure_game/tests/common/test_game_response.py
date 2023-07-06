"""Test the game response class."""

from common.game_message import GameMessage
from common.game_response import GameResponse
from common.request_status import RequestStatus
from tests.test_helpers import any_message_contents


def test_it_should_fail_with_headers():
    """Test to make sure it fails with headers."""
    response = GameResponse.failure_with_header("header", "message")
    assert any_message_contents(response.messages, "header")
    assert any_message_contents(response.messages, "message")
    assert response.status == RequestStatus.FAILURE


def test_it_should_have_a_dict():
    """Test to make sure it has a dictionary method."""
    messages = ["string", "string2"]
    response = GameResponse(
        messages=[
            GameMessage.single_line("string"),
            GameMessage.single_line("string2"),
        ],
        status=RequestStatus.SUCCESS,
    )
    assert response.dictionary() == {"status": "SUCCESS", "messages": messages}


def test_it_should_have_a_repr():
    """Test to make sure it has a __repr__ method."""
    response = GameResponse(
        messages=[
            GameMessage.single_line("string"),
            GameMessage.single_line("string2"),
        ],
        status=RequestStatus.SUCCESS,
    )
    assert repr(response) == str(response.dictionary())


def test_it_should_have_failure_with_messages():
    """Test to make sure the failure_with_messages method works."""
    messages = [
        GameMessage.single_line("string"),
    ]
    response = GameResponse.failure_with_messages(messages)
    assert response.status == RequestStatus.FAILURE
    assert response.messages[0].contents == "string"


def test_it_should_succeed_with_literal():
    messages = ["string1", "string2", "string3"]
    response = GameResponse.art(messages)
    assert response.status == RequestStatus.SUCCESS
    assert len(response.messages) == 2
    assert len(response.messages[1].contents) == 3
