"""A class designed to handle the stories of the game."""

from game_repository.file_manager import FileManager


class StoryManager:
    """A class that manages the game stories."""

    def __init__(self: "StoryManager") -> None:
        """Initialize the story manager."""
        self.stories: dict[str, list[str]] = dict()

    def load_stories(self: "StoryManager") -> None:
        """Load the game stories."""
        self.stories = FileManager.load_game_stories()

    def get_story(self: "StoryManager", story_name: str | None) -> list[str]:
        """Get a story by name."""
        return self.stories.get(story_name, [])
