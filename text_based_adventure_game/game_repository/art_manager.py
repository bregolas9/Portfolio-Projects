"""Manages the game art."""

from game_repository.file_manager import FileManager


class ArtManager:
    """A class to manage the art related contents."""

    def __init__(self: "ArtManager") -> None:
        """Initialize the art manager."""
        self.art: dict[str, list[str]] = dict()

    def load_art(self: "ArtManager") -> None:
        """Load the art to use in the game."""
        self.art = FileManager.load_art()

    def get_art_by_name(self: "ArtManager", art_name: str | None) -> list[str]:
        """Get game art by the name or return an empty list."""
        return [] if art_name is None else self.art.get(art_name, [])
