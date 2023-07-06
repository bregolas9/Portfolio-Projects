"""A module that contains the GameMessage class."""


from common.message_type import MessageType


class GameMessage:
    """Represent a message to be printed to the user."""

    def __init__(
        self: "GameMessage",
        message_type: MessageType,
        contents: str | list[str] = "",
    ) -> None:
        """Initialize a GameMessage instance."""
        self.message_type = message_type
        self.contents = contents

    def dictionary(self: "GameMessage") -> dict:
        """Return the dictionary of the GameMessage."""
        return {
            "message_type": self.message_type.name,
            "contents": str(self),
        }

    def __repr__(self: "GameMessage") -> str:
        """Return the representation of the GameMessage."""
        return str(self.dictionary())

    def __str__(self: "GameMessage") -> str:
        """Return the representation of the GameMessage."""
        if (
            isinstance(self.contents, str)
            and not self.message_type == MessageType.BLANK_LINE
        ):
            return self.contents
        match self.message_type:
            case MessageType.SINGLE_LINE:
                return " ".join(self.contents)
            case MessageType.BLANK_LINE:
                return ""
            case MessageType.PARAGRAPH:
                return " ".join(self.contents)
            case MessageType.ART:
                return "\n".join(self.contents)
            case _:  # pragma: no cover
                raise NotImplementedError(f"Unknown message type: {self.message_type}")

    def should_print_blank_line(self: "GameMessage") -> bool:
        """Return whether the message should print a blank line."""
        return self.message_type == MessageType.BLANK_LINE

    def should_wrap(self: "GameMessage") -> bool:
        """Return whether the message should be wrapped."""
        if isinstance(self.contents, str):
            return len(self.contents) > 80
        elif self.message_type == MessageType.PARAGRAPH:
            return True
        else:
            return False

    @staticmethod
    def single_line(contents: str) -> "GameMessage":
        """Return a GameMessage with a single line message."""
        return GameMessage(MessageType.SINGLE_LINE, contents)

    @staticmethod
    def blank_line() -> "GameMessage":
        """Return a GameMessage with a blank line message."""
        return GameMessage(MessageType.BLANK_LINE)

    @staticmethod
    def paragraph(contents: str) -> "GameMessage":
        """Return a GameMessage with a paragraph message."""
        return GameMessage(MessageType.PARAGRAPH, contents)

    @staticmethod
    def art(contents: list[str]) -> "GameMessage":
        """Return a GameMessage with a literal message."""
        return GameMessage(MessageType.ART, contents)
