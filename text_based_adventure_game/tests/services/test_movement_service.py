"""Test the movement service."""

from unittest.mock import MagicMock

from common.game_message import GameMessage
from common.game_objective import GameObjective
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.item import Item
from common.player import Player
from common.request_status import RequestStatus
from common.request_type import RequestType
from common.room import Room
from game_repository.game_repository import GameRepository
from game_repository.objectives_manager import ObjectiveManager
from services.movement_service import MovementService
from tests.test_helpers import any_message_contents


def test_movement_service_can_move_method_when_room_not_exist():
    """Test the can_move method of the movement service."""

    current_room = Room(
        name="kitchen",
        description={
            "default": "a kitchen",
        },
        blockers=[],
        exits=[],
        directional_exits={"west": "entry"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(name="get_room_by_name", return_value=None)
    mock_repo.current_location = current_room

    movement_service = MovementService(mock_repo)
    result = movement_service.can_move("test")
    assert result is False
    mock_repo.get_room_by_name.assert_called_once_with("test")


def test_movement_service_can_move_method_when_room_blocked():
    """Test the can_move method of the movement service when a room is blocked."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[
            {
                "name": "test blocker",
                "message": "test message",
            }
        ],
        exits=["kitchen"],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    current_room = Room(
        name="kitchen",
        description={"test": "a kitchen"},
        blockers=[],
        exits=["test"],
        directional_exits={"east": "test"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    # No interaction requirements, but one item requirement.
    objective = GameObjective("test blocker", [], ["imaginary item"], [])
    mock_repo.current_location = current_room
    mock_repo.objectives = MagicMock(ObjectiveManager)
    mock_repo.player = MagicMock(Player)
    mock_repo.player.inventory = []
    mock_repo.player.location = current_room
    mock_repo.objectives.get_objective_by_name = MagicMock(return_value=objective)
    movement_service = MovementService(mock_repo)
    result = movement_service.can_move("test")
    assert result is False
    mock_repo.get_room_by_name.assert_called_once_with("test")


def test_movement_service_can_move_method_when_not_connected():
    """Test the can_move method when a room not connected via an exit."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    current_room = Room(
        name="kitchen",
        description={"test": "a kitchen"},
        blockers=[],
        exits=[],
        directional_exits={},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = current_room

    movement_service = MovementService(mock_repo)
    result = movement_service.can_move("test")
    assert result is False
    mock_repo.get_room_by_name.assert_called_once_with("test")


def test_movement_service_can_move_method_when_connected():
    """Test the can_move method when a room is connected via an exit."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=["kitchen"],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    current_room = Room(
        name="kitchen",
        description={"test": "a kitchen"},
        blockers=[],
        exits=["test"],
        directional_exits={"east": "test"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = current_room

    movement_service = MovementService(mock_repo)
    result = movement_service.can_move("test")
    assert result is True
    mock_repo.get_room_by_name.assert_called_once_with("test")


def test_movement_service_can_move_method_when_already_there():
    """Test the can_move method when the player is already in the room."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = test_room

    movement_service = MovementService(mock_repo)
    result = movement_service.can_move("test")
    assert result is False
    mock_repo.get_room_by_name.assert_called_once_with("test")


def test_movement_service_is_connected_when_not_connected():
    """Test the is_connected method when the rooms are not connected."""

    current_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    movement_service = MovementService(MagicMock)
    assert not movement_service.is_connected(current_room, "test")


def test_movement_service_is_connected_when_connected():
    """Test the is_connected method when the rooms are connected."""

    current_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=["test"],
        directional_exits={"east": "test"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    movement_service = MovementService(MagicMock)
    assert movement_service.is_connected(current_room, "test")


def test_movement_service_already_here_method_when_not_here():
    """Test the already_here method when the player is not in the room."""

    current_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    repo_mock = MagicMock(GameRepository)
    repo_mock.current_location = current_room

    movement_service = MovementService(repo_mock)
    assert not movement_service.already_here(test_room)


def test_movement_service_non_existent_response():
    """Test the non_existent_response method."""
    movement_service = MovementService(MagicMock)
    response = movement_service.non_existent_room_response
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like that room doesn't exist."
    )


def test_movement_service_blocked_room_response():
    """Test the non_existent_response method."""
    movement_service = MovementService(MagicMock)
    response = movement_service.blocked_room_response("test")
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(response.messages, "test")


def test_movement_service_already_here_response():
    """Test the non_existent_response method."""
    movement_service = MovementService(MagicMock)
    response = movement_service.already_here_response
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like you're already there."
    )


def test_movement_service_path_not_connected_response():
    """Test the non_existent_response method."""
    movement_service = MovementService(MagicMock)
    response = movement_service.path_not_connected_response
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like you can't go that way."
    )


def test_movement_service_move_method_when_not_connected():
    """Test the move method when the rooms are not connected."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    current_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = current_room

    movement_service = MovementService(mock_repo)
    response = movement_service.move(GameRequest(RequestType.MOVE, ["test"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like you can't go that way."
    )
    mock_repo.get_room_by_name.assert_called_with("test")


def test_movement_service_move_method_when_blocked():
    """Test the movement service move method when the room is blocked."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    current_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"east": "test"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = current_room

    movement_service = MovementService(mock_repo)
    movement_service.is_blocked = MagicMock(name="is_blocked", return_value=True)
    movement_service.blocked_room_response = MagicMock(
        return_value=GameResponse(
            [GameMessage.blank_line(), GameMessage.paragraph("test")],
            RequestStatus.FAILURE,
        )
    )
    response = movement_service.move(GameRequest(RequestType.MOVE, ["test"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(response.messages, "test")
    mock_repo.get_room_by_name.assert_called_with("test")


def test_movement_service_move_method_when_already_here():
    """Test the movement service move method when the player is already in the room."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = test_room

    movement_service = MovementService(mock_repo)
    response = movement_service.move(GameRequest(RequestType.MOVE, ["test"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like you're already there."
    )
    mock_repo.get_room_by_name.assert_called_with("test")


def test_movement_service_move_method_when_room_not_exist():
    """Test the movement service move method when the room doesn't exist."""

    mock_repo = MagicMock(GameRepository)
    mock_repo.get_room_by_name = MagicMock(name="get_room_by_name", return_value=None)
    mock_repo.get_room_by_direction = MagicMock(
        name="get_room_by_direction", return_value=None
    )

    movement_service = MovementService(mock_repo)
    response = movement_service.move(GameRequest(RequestType.MOVE, ["test"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like you can't do that."
    )
    mock_repo.get_room_by_name.assert_called_with("test")
    mock_repo.get_room_by_direction.assert_called_with("test")


def test_movement_service_move_method_when_valid():
    """Test the move method in the movement service when the player can move."""

    test_room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=["kitchen"],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    current_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=["test"],
        directional_exits={"east": "test"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.player = MagicMock(Player)
    mock_repo.player.visited_rooms = []
    mock_repo.get_room_by_name = MagicMock(
        name="get_room_by_name", return_value=test_room
    )
    mock_repo.current_location = current_room
    mock_repo.move_player = MagicMock(name="move_player", return_value=None)

    movement_service = MovementService(mock_repo)
    response = movement_service.move(GameRequest(RequestType.MOVE, ["test"]))
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "a test room ")
    mock_repo.get_room_by_name.assert_called_with("test")
    mock_repo.move_player.assert_called_with(test_room)


def test_movement_service_look_method_should_work():
    """Test the look method in the movement service."""
    room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.current_location = room
    mock_repo.find_target = MagicMock(name="find_target", return_value=room.name)

    movement_service = MovementService(mock_repo)
    response = movement_service.look(GameRequest(RequestType.LOOK, ["test"]))
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "a test room ")

    response = movement_service.look(GameRequest(RequestType.LOOK, [None]))
    assert response.status == RequestStatus.SUCCESS
    assert any_message_contents(response.messages, "a test room ")


def test_movement_service_look_method_should_not_work_if_not_in_same_room():
    """Test to make sure the look method does not describe an adjacent room."""
    room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    adjacent_room = Room(
        name="kitchen",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"east": "test"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.current_location = room
    mock_repo.find_target = MagicMock(
        name="find_target", return_value=adjacent_room.name
    )
    mock_repo.get_room_by_name = MagicMock(return_value=adjacent_room)
    movement_service = MovementService(mock_repo)
    response = movement_service.look(GameRequest(RequestType.LOOK, ["kitchen"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "Hmm, it seems like you can't quite see that room from here. "
        + "Try moving closer.",
    )


def test_movement_service_look_method_should_fail_when_room_not_exist():
    """Test the look method in the movement service when the room doesn't exist."""
    mock_repo = MagicMock(GameRepository)
    mock_repo.find_target.return_value = None
    movement_service = MovementService(mock_repo)
    response = movement_service.look(GameRequest(RequestType.LOOK, ["test"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like that room doesn't exist."
    )


def test_movement_service_get_look_description_should_print_item_contents():
    """Test the get look description method to make sure it prints the inventory."""
    mock_repo = MagicMock(GameRepository)
    test_item = Item(
        name="test item",
        alias=[],
        description=["a test item."],
        look_at_message={"line1": "a test item."},
        is_collectible=True,
        discovered=True,
        interactions={},
    )
    room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[test_item],
        starting_inventory=[test_item],
    )
    mock_repo.current_location = room
    mock_repo.player = MagicMock(Player)
    mock_repo.player.visited_rooms = [room.name]
    movement_service = MovementService(mock_repo)
    response = movement_service.get_look_description(False)
    assert any_message_contents(response, "a test room ")
    assert any_message_contents(
        response, "You previously dropped some items on the floor:"
    )
    assert any_message_contents(response, "Test item - a test item.")


def test_can_move_method_fails_when_room_name_is_none():
    """Test to make sure the can move method fails when the room name is None."""
    mock_repo = MagicMock(GameRepository)
    movement_service = MovementService(mock_repo)
    assert not movement_service.can_move(None)


def test_move_method_fails_when_request_targets_empty():
    """The move method should fail when the request targets list is empty."""
    mock_repo = MagicMock(GameRepository)
    movement_service = MovementService(mock_repo)
    response = movement_service.move(GameRequest(RequestType.MOVE, []))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages, "Hmm, it seems like you can't do that."
    )


def test_movement_service_get_blocked_message():
    """Test the get blocked message method."""
    mock_repo = MagicMock(GameRepository)
    mock_repo.objectives = MagicMock(ObjectiveManager)
    objective = MagicMock(GameObjective)
    objective.is_complete = MagicMock(return_value=False)
    mock_repo.objectives.get_objective_by_name = MagicMock(return_value=objective)
    mock_repo.player = MagicMock(Player)
    movement_service = MovementService(mock_repo)
    room = MagicMock(Room)
    room.blockers = [{"name": "test", "message": "test message"}]
    assert movement_service.get_blocked_message(room) == "test message"


def test_get_blocked_message_when_not_blocked():
    """Get blocked message shouldn't be called when not blocked, but if so, it should return a message."""
    mock_repo = MagicMock(GameRepository)
    mock_repo.objectives = MagicMock(ObjectiveManager)
    objective = MagicMock(GameObjective)
    objective.is_complete = MagicMock(return_value=True)
    mock_repo.objectives.get_objective_by_name = MagicMock(return_value=objective)
    mock_repo.player = MagicMock(Player)
    movement_service = MovementService(mock_repo)
    room = MagicMock(Room)
    room.blockers = [{"name": "test", "message": "test message"}]
    assert (
        movement_service.get_blocked_message(room)
        == "Tell the developer that they messed up..."
    )


def test_movement_service_look_method_should_not_work_if_target_is_not_a_room():
    """Test to make sure the look method does not describe an adjacent room."""
    room = Room(
        name="test",
        description={"test": "a test room"},
        blockers=[],
        exits=[],
        directional_exits={"west": "kitchen"},
        aliases=[],
        inventory=[],
        starting_inventory=[],
    )
    item = Item(
        name="flashlight",
        alias=[],
        description=["test"],
        look_at_message={},
        is_collectible=True,
        discovered=False,
        interactions={},
    )

    mock_repo = MagicMock(GameRepository)
    mock_repo.current_location = room
    mock_repo.find_target = MagicMock(name="find_target", return_value=item.name)
    movement_service = MovementService(mock_repo)
    response = movement_service.look(GameRequest(RequestType.LOOK, ["flashlight"]))
    assert response.status == RequestStatus.FAILURE
    assert any_message_contents(
        response.messages,
        "You can only use the look command to look at rooms, "
        "try the inspect command instead.",
    )
