"""Test the objectives manager class."""

from unittest.mock import MagicMock, patch

from common.game_objective import GameObjective
from common.item import Item
from common.load_error import FileOperationError
from common.player import Player
from game_repository.file_manager import FileManager
from game_repository.objectives_manager import ObjectiveManager


def test_it_should_not_load_objectives_when_failure():
    """Test to make sure it does not load the objectives."""
    with patch.object(
        FileManager, "get_objectives_file", return_value=FileOperationError("oops")
    ) as mock_file_load:
        manager = ObjectiveManager()
        response = manager.load_objectives(True)
        assert response == mock_file_load.return_value


def test_it_should_load_objectives_when_successful():
    """Test to make sure it loads objectives from a mock source when successful."""
    objectives = [
        {
            "name": "unlock the bedroom door",
            "requires": [],
            "interactions": [
                {"interaction_type": "use_with", "item": "fork", "complete": False}
            ],
        }
    ]
    with patch.object(FileManager, "get_objectives_file", return_value=objectives):
        manager = ObjectiveManager()
        response = manager.load_objectives(True)
        assert not isinstance(response, FileOperationError)
        assert len(manager.objectives) == 1
        objective = manager.objectives.get("unlock the bedroom door")
        assert objective is not None
        assert objective.name == "unlock the bedroom door"


def test_it_should_get_objective_by_name():
    """Test to make sure it gets objectives by name."""
    objective = GameObjective("test", [], [], [])
    manager = ObjectiveManager()
    manager.objectives[objective.name] = objective
    assert manager.get_objective_by_name("test") == objective


def test_it_should_find_related_objectives():
    """Test to make sure it finds related objectives."""
    item = MagicMock(Item)
    item.name = "test item"
    interactions = [{"interaction_type": "use", "item": "test item", "complete": False}]
    objective = GameObjective("test", [], [item.name], interactions)
    manager = ObjectiveManager()
    manager.objectives[objective.name] = objective
    assert manager.find_related_objectives(item, "use") == [objective]


def test_it_should_load_objectives():
    """Test to make sure it can load objectives."""
    objectives = [
        {
            "name": "unlock the bedroom door",
            "requires": [],
            "interactions": [
                {"interaction_type": "use_with", "item": "fork", "complete": False}
            ],
        }
    ]
    with patch.object(FileManager, "get_objectives_file", return_value=objectives):
        manager = ObjectiveManager()
        response = manager.load_objectives(True)
        assert not isinstance(response, FileOperationError)
        assert len(manager.objectives) == 1
        objective = manager.objectives.get("unlock the bedroom door")
        assert objective is not None
        assert objective.name == "unlock the bedroom door"


def test_it_should_tell_all_objectives_complete():
    """Test to make sure when all objectives are complete, it works."""
    objective = MagicMock(GameObjective)
    objective.name = "test"
    objective.is_complete = MagicMock(return_value=True)
    player = MagicMock(Player)
    manager = ObjectiveManager()
    manager.objectives = {"test": objective}
    assert manager.all_objectives_complete(player)


def test_it_should_tell_not_all_objectives_complete():
    """Test to make sure when not all objectives are complete, it works."""
    objective = MagicMock(GameObjective)
    objective.name = "test"
    objective.is_complete = MagicMock(return_value=False)
    player = MagicMock(Player)
    manager = ObjectiveManager()
    manager.objectives = {"test": objective}
    assert not manager.all_objectives_complete(player)
