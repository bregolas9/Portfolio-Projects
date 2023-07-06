from unittest.mock import MagicMock, patch
from game_repository.file_manager import FileManager
from game_repository.art_manager import ArtManager


def test_it_should_not_load_art_when_failure():
    """Test to make sure it does not load the art."""
    expected = {"test": ["test1"]}
    with patch.object(FileManager, "load_art", return_value=expected) as mock_file_load:
        manager = ArtManager()
        assert manager.art == {}
        manager.load_art()
        assert manager.art == mock_file_load.return_value


def test_get_art_by_name():
    """Test to make sure we can get art by name."""
    manager = ArtManager()
    manager.art = {"test": ["test_art"]}
    assert manager.get_art_by_name("test") == ["test_art"]
    assert manager.get_art_by_name("string") == []
