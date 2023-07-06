"""Test the story manager class."""


from unittest.mock import patch
from game_repository.file_manager import FileManager
from language.story_manager import StoryManager


def mock_story_helper():
    """Return mock story data for testing."""
    return {
        "introduction": ["intro story"],
    }


def test_it_should_get_stories():
    """Test to make sure it can get all of the stories."""
    with patch.object(StoryManager, "__init__", return_value=None):
        manager = StoryManager()
        manager.stories = mock_story_helper()
        assert manager.get_story("introduction") == ["intro story"]
        assert manager.get_story(None) == []


def test_it_should_load_stories():
    """Test to make sure it loads stories."""
    with patch.object(
        FileManager, "load_game_stories", return_value=mock_story_helper()
    ):
        manager = StoryManager()
        manager.load_stories()
        assert manager.stories == mock_story_helper()
