"""The Game Request object is the primary way to communicate player intent.

Game requests have an action and a list of targets. The action uses a RequestType
to indicate what the player wants to do. The targets are a list of strings that
indicate what the player wants to do the action to. For example, if the player
wants to 'use' the 'key' on the 'door', the action would be RequestType.USE and
the targets would be ['key', 'door'].
"""


import json

from common.request_type import RequestType


class GameRequest:
    """A request to perform an action in the game."""

    def __init__(
        self: "GameRequest", request_type: RequestType, targets: list[str | None]
    ) -> None:
        """Create a new game request."""
        self.action = request_type
        self.targets = targets

    def __repr__(self) -> str:
        """Representation of the item."""
        return json.dumps(self.__dict__, indent=4, sort_keys=True)  # pragma: no cover
