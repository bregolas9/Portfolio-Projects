"""A class that represents an error during a file operation."""


class FileOperationError:
    """An error that occurs during a file operation."""

    def __init__(self: "FileOperationError", message: str):
        """Initialize the file operation error."""
        self.message = message
