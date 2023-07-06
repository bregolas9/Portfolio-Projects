"""The service that handles item and player interactions."""

from typing import Any

from common.game_message import GameMessage
from common.game_request import GameRequest
from common.game_response import GameResponse
from common.item import Item
from game_repository.game_repository import GameRepository


class InteractionService:
    """The service that handles item and player interactions."""

    def __init__(self: "InteractionService", game_repository: GameRepository) -> None:
        """Initialize the interaction service."""
        self.repository = game_repository

    def use(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Use an item in the player's inventory or in the current room."""
        if len(request.targets) == 0:
            return self.try_naming_the_item_response
        if len(request.targets) == 1:
            item = self.repository.items.get_item_by_name(request.targets[0])
            return self.handle_single_interaction(item, "use")
        items = [
            self.repository.items.get_item_by_name(target) for target in request.targets
        ]
        return self.handle_multiple_interaction(items, "use_with")

    def handle_multiple_interaction(
        self: "InteractionService", items: list[Item | None], action: str
    ) -> GameResponse:
        """Handle the case where there are multiple items."""
        if any(item is None for item in items):
            return self.try_naming_the_item_response
        filtered_items = [item for item in items if item is not None]
        trimmed_action = action.replace("_with", "")
        for item in items:
            if not self.is_nearby(item) or item is None:
                return self.item_not_found_response
            if not self.is_discovered(item):
                return self.try_picking_it_up_response(item, trimmed_action)
                # Determine if the item can be used.
        if not self.can_interact_multiple_items(items, action):
            return self.item_default_multiple_interaction_response(
                filtered_items, trimmed_action
            )
        return self.interact_multiple_items(filtered_items, action)

    def handle_single_interaction(
        self: "InteractionService", item: Item | None, action: str
    ) -> GameResponse:
        """Handle the case where there is only one item."""
        if not self.is_nearby(item) or item is None:
            return self.item_not_found_response

        if not self.is_discovered(item):
            return self.try_picking_it_up_response(item, action)

        # Determine if the item can be used.
        if not self.can_interact_single_item(item, action):
            return self.item_default_single_interaction_response(item, action)

        return self.interact_single_item(item, action)

    def is_nearby(self: "InteractionService", item: Item | None) -> bool:
        """Return true if the item is nearby."""
        return item is not None and (
            item in self.repository.player.inventory
            or item in self.repository.current_location.inventory
        )

    def can_interact_multiple_items(
        self: "InteractionService", items: list[Item | None], action: str
    ) -> bool:
        """Return true if the items can be used."""
        for item in items:
            if item is None or not self.is_nearby(item):
                return False
            use_interaction = item.interactions.get(action)
            if use_interaction is None:
                return False
            requirements = self.get_interaction_requirements(item, action)
            if item.is_collectible and item not in self.repository.player.inventory:
                return False
            if self.has_missing_items(requirements) and self.is_discovered(item):
                return False
        return True

    def can_interact_single_item(
        self: "InteractionService", item: Item | None, action: str
    ) -> bool:
        """Return true if the item can be used."""
        if item is None or not self.is_nearby(item):
            return False
        use_interaction = item.interactions.get(action)
        if use_interaction is None:
            return False
        requirements = self.get_interaction_requirements(item, action)
        if item.is_collectible and item not in self.repository.player.inventory:
            return False
        return not self.has_missing_items(requirements) and (
            (self.is_discovered(item) and item.is_collectible)
            or not item.is_collectible
        )

    def handle_interaction_transformations(
        self: "InteractionService", item: Item, action: str
    ) -> None:
        """Transform an existing item into another one after use."""
        transformations = self.get_transformations(item, action)
        for transformation in transformations:
            self.transform_item(transformation["from"], transformation["to"])

    def transform_item(
        self: "InteractionService", from_item_name: str | None, to_item_name: str | None
    ) -> None:
        """Transform an item into another item."""
        from_item = self.repository.items.get_item_by_name(from_item_name)
        to_item = self.repository.items.get_item_by_name(to_item_name)

        # if both are None, then nothing happens.
        if from_item is None and to_item is None:
            return

        # if from_item is None, then we add a new item to the player's inventory.
        elif from_item is None and to_item is not None:
            self.repository.player.inventory.append(to_item)
            to_item.discovered = True
            self.repository.state_dirty = True

        # if to_item is None, then the item is removed from the player's
        # inventory or the room.
        elif from_item is not None and to_item is None:
            if from_item in self.repository.player.inventory:
                self.repository.player.inventory.remove(from_item)
            elif from_item in self.repository.current_location.inventory:
                self.repository.current_location.inventory.remove(from_item)
            self.repository.state_dirty = True

        # if both are not None, then the item is transformed into another item.
        elif from_item is not None and to_item is not None:
            if from_item in self.repository.player.inventory:
                self.repository.player.inventory.remove(from_item)
            elif from_item in self.repository.current_location.inventory:
                self.repository.current_location.inventory.remove(from_item)
            self.repository.player.inventory.append(to_item)
            to_item.discovered = True
            self.repository.state_dirty = True

    def get_transformations(
        self: "InteractionService", item: Item, action: str
    ) -> list[dict[str, str]]:
        """Return the transformations that occur after using the item."""
        use_interaction = item.interactions.get(action)
        if use_interaction is None:
            return []
        transformations = use_interaction.get("transforms")
        return [] if transformations is None else transformations

    def get_interaction_requirements(
        self: "InteractionService", item: Item, action: str
    ) -> list[Item | None]:
        """Return the requirements for the given item."""
        interaction = item.interactions.get(action)
        if interaction is None:
            return []
        requirements = interaction.get("requires")
        if requirements is None:
            return []
        return [
            self.repository.items.get_item_by_name(item_name)
            for item_name in requirements
        ]

    def is_discovered(self: "InteractionService", item: Item | None) -> bool:
        """Return true if the item has been discovered."""
        if item is None:
            return False
        if item.is_collectible:
            return item.discovered
        # This is probably okay because these items are not collectible and are
        # always in the descriptions.
        return True

    def has_missing_items(self: "InteractionService", items: list[Item | None]) -> bool:
        """Return true if any of the items are missing."""
        return (
            any(item is None for item in items)
            or not all(self.is_nearby(item) for item in items)
            or not all(self.is_discovered(item) for item in items)
        )

    def chew(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Chew on an item in the player's inventory or in the current room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "chew")

    def sit(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Sit on an item in the player's inventory or in the current room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "sit")

    def pull(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Pull on an item in the player's inventory or in the current room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "pull")

    def clean(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Clean up some items in a room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "clean")

    def drink(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Clean up some items in a room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "drink")

    def climb(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Climb an item in the room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "climb")

    def turn_on(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Turn on an item in the room."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "turn on")

    def open(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Open an item in the room or inventory."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "open")

    def play(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Play an item in the room or inventory."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "play")

    def flush(self: "InteractionService", request: GameRequest) -> GameResponse:
        """Play an item in the room or inventory."""
        if len(request.targets) == 0:
            return self.item_not_found_response
        item = self.repository.items.get_item_by_name(request.targets[0])
        return self.handle_single_interaction(item, "flush")

    def interact_single_item(
        self: "InteractionService", item: Item, action: str
    ) -> GameResponse:
        """Use this item on another item, or use it by itself."""
        interaction = item.interactions.get(action)
        if interaction is None:
            return self.item_default_single_interaction_response(item, action)
        else:
            self.update_interaction_description(item, action)
            self.update_interaction_objectives(item, action)
            self.unhide_items(item, action)
            self.unlock_items(item, action)
            self.discover_items(item, action)
            response = self.get_interaction_message_response(item, action)
            self.handle_interaction_transformations(item, action)
            return response

    def discover_items(self: "InteractionService", item: Item, action: str) -> None:
        """Discover an item after an interaction."""
        interaction = item.interactions.get(action)
        if interaction is None:
            return
        discovers = interaction.get("discovers")
        if discovers is None:
            return
        for item_name in discovers:
            possible_item = self.repository.items.get_item_by_name(item_name)
            if possible_item is not None:
                possible_item.discovered = True

    def unhide_items(self: "InteractionService", item: Item, action: str) -> None:
        """Unhide an item after it has been interacted with."""
        # figure out if the interaction defines unhides
        interaction = item.interactions.get(action)
        if interaction is None:
            return
        unhides = interaction.get("unhides")
        if unhides is None:
            return
        for item_name in unhides:
            possible_item = self.repository.items.get_item_by_name(item_name)
            if possible_item is not None:
                possible_item.hidden = False

    def unlock_items(self: "InteractionService", item: Item, action: str) -> None:
        """Unlock an item after it has been interacted with."""
        interaction = item.interactions.get(action)
        if interaction is None:
            return
        unlocks = interaction.get("unlocks")
        if unlocks is None:
            return
        for item_name in unlocks:
            possible_item = self.repository.items.get_item_by_name(item_name)
            if possible_item is not None:
                possible_item.locked = False

    def update_interaction_objectives(
        self: "InteractionService", item: Item, action: str
    ) -> None:
        """Update the objectives of an item after it has been interacted with."""
        objectives = self.repository.objectives.find_related_objectives(item, action)
        for objective in objectives:
            objective.complete_interaction_objective(item.name, action)

    def interact_multiple_items(
        self: "InteractionService", items: list[Item], action: str
    ) -> GameResponse:
        """Use multiple items on another item, or use them by themselves."""
        interaction = items[0].interactions.get(action)
        if interaction is None:
            return self.item_default_multiple_interaction_response(items, action)
        else:
            self.update_interaction_description(items[0], action)
            self.update_interaction_description(items[1], action)
            self.update_interaction_objectives(items[0], action)
            self.update_interaction_objectives(items[1], action)
            self.unhide_items(items[0], action)
            self.unlock_items(items[0], action)
            self.unhide_items(items[1], action)
            self.unlock_items(items[1], action)
            self.discover_items(items[0], action)
            self.discover_items(items[1], action)
            response = self.get_interaction_message_response(items[0], action)
            self.handle_interaction_transformations(items[0], action)

            return response

    def update_interaction_description(
        self: "InteractionService", item: Item, action: str
    ) -> None:
        """Update the description of an item after it has been used."""
        interaction = item.interactions.get(action)
        if interaction is None:
            return
        new_description = interaction.get("new_description")
        if new_description is not None:
            item.description = new_description

    def get_interaction_message_response(
        self: "InteractionService", item: Item, action: str
    ) -> GameResponse:
        """Return a response for using an item."""
        interaction = item.interactions.get(action)
        if interaction is None:
            return self.item_default_single_interaction_response(item, action)
        message = interaction.get("message")
        messages = [
            GameMessage.blank_line(),
            GameMessage.paragraph(message),
        ]
        return GameResponse.success_with_messages(messages)

    @property
    def item_not_found_response(self: "InteractionService") -> GameResponse:
        """Return a response for when an item is not found."""
        return GameResponse.failure("Hmm, you can't seem to find that.")

    def item_default_single_interaction_response(
        self: "InteractionService", item: Item, action: str
    ) -> GameResponse:
        """Return a response for when an item has no use defined."""
        return GameResponse.failure(
            f"You try to {action + ' on' if action == 'sit' else action} the {item.name} but nothing interesting happens."
        )

    def item_default_multiple_interaction_response(
        self: "InteractionService", items: list[Item], action: str
    ) -> GameResponse:
        """Return a response for when an item has no use defined."""
        if len(items) == 1:
            return self.item_default_single_interaction_response(items[0], action)

        item1, item2 = items[:2]
        return GameResponse.failure(
            f"You try to {action + ' on' if action == 'sit' else action} the {item1.name} with the {item2.name} "
            + "but nothing interesting happens."
        )

    def try_picking_it_up_response(
        self: "InteractionService", item: Item, action: str
    ) -> GameResponse:
        """Return a response for when an item has not been discovered yet."""
        return GameResponse.failure(
            f"You try to {action + ' on' if action == 'sit' else action} the {item.name} but it's too far away. "
            + "Try picking it up first."
        )

    @property
    def try_naming_the_item_response(self: "InteractionService") -> GameResponse:
        """Return a response for when an item name is not resolved."""
        return GameResponse.failure("You aren't sure what to do, try naming the item.")
