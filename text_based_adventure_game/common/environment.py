"""Represents the environment."""


class Environment:
    """An enum that represents the environment."""

    def __init__(self: "Environment", is_developement: bool) -> None:
        """Initialize the environment."""
        self.is_development = is_developement
