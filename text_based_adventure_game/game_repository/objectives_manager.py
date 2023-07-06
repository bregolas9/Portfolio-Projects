"""A class to manage game objectives."""


from common.game_objective import GameObjective
from common.item import Item
from common.load_error import FileOperationError
from common.player import Player
from game_repository.file_manager import FileManager


class ObjectiveManager:
    """A class to manage game objectives."""

    def __init__(self: "ObjectiveManager") -> None:
        """Initialize the objective manager."""
        self.objectives: dict[str, GameObjective] = dict()

    def load_objectives(
        self: "ObjectiveManager", new: bool
    ) -> None | FileOperationError:
        """Load the objectives file."""
        objectives_state = FileManager.get_objectives_file(new)
        if isinstance(objectives_state, FileOperationError):
            return objectives_state

        objectives: dict[str, GameObjective] = dict()
        for objective in objectives_state:
            name = objective.get("name", "")
            hints = objective.get("hints", [])
            requirements = objective.get("requires", [])
            interactions = objective.get("interactions", [])
            new_objective = GameObjective(
                name=name,
                hints=hints,
                requirements=requirements,
                interactions=interactions,
            )
            objectives[name] = new_objective
        self.objectives = objectives

    def find_related_objectives(
        self: "ObjectiveManager", item: Item, action: str
    ) -> list[GameObjective]:
        """Find the objectives related to the given item and action."""
        related_objectives: list[GameObjective] = []
        for objective in self.objectives.values():
            interactions = objective.interactions
            for interaction in interactions:
                if (
                    interaction.get("item") == item.name
                    and interaction.get("interaction_type") == action
                ):
                    related_objectives.append(objective)
        return related_objectives

    def get_objective_by_name(
        self: "ObjectiveManager", name: str
    ) -> GameObjective | None:
        """Find the objective with the given name."""
        return self.objectives.get(name)

    def all_objectives_complete(self: "ObjectiveManager", player: Player) -> bool:
        """Return True if all objectives are complete."""
        for objective in self.objectives.values():
            if not objective.is_complete(player):
                return False
        return True
