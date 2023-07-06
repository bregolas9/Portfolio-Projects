"""The adventure game module."""

import argparse
import sys
from typing import Any

from common.controller_type import ControllerType
from common.game_message import GameMessage
from common.request_status import RequestStatus
from common.service_type import ServiceType
from controllers.game_controller import GameController
from controllers.interaction_controller import InteractionController
from controllers.inventory_controller import InventoryController
from controllers.movement_controller import MovementController
from game_repository.file_manager import FileManager
from game_repository.game_repository import GameRepository
from language.text_parser import TextParser
from router.router import Router
from services.game_service import GameService
from services.interaction_service import InteractionService
from services.inventory_service import InventoryService
from services.movement_service import MovementService


class AdventureGame:
    """A class that represents the adventure game setup and configuration."""

    def __init__(self: "AdventureGame") -> None:
        """Initialize the adventure game."""
        pass

    def initialize_text_parser(
        self: "AdventureGame", router: Router, repository: GameRepository
    ) -> TextParser:
        """Initialize the text parser."""
        return TextParser(router, repository)

    def initialize_router(
        self: "AdventureGame", controllers: dict[ControllerType, Any]
    ) -> Router:
        """Initialize the router."""
        return Router(controllers)

    def initialize_controllers(
        self: "AdventureGame", services: dict[ServiceType, Any]
    ) -> dict[ControllerType, Any]:
        """Initialize the controllers."""
        return {
            ControllerType.MOVEMENT: MovementController(services),
            ControllerType.GAME: GameController(services),
            ControllerType.INVENTORY: InventoryController(services),
            ControllerType.INTERACTION: InteractionController(services),
        }

    def initialize_services(
        self: "AdventureGame", game_repository: GameRepository
    ) -> dict[ServiceType, Any]:
        """Initialize the services."""
        return {
            ServiceType.MOVEMENT: MovementService(game_repository),
            ServiceType.GAME: GameService(game_repository),
            ServiceType.INVENTORY: InventoryService(game_repository),
            ServiceType.INTERACTION: InteractionService(game_repository),
        }

    def initialize_game_repository(
        self: "AdventureGame", is_dev: bool
    ) -> GameRepository:
        """Initialize the game repository."""
        repo = GameRepository(is_dev)
        repo.load_default_state()
        return repo

    def initialize_game(self: "AdventureGame", is_dev: bool) -> "AdventureGame":
        """Initialize the game."""
        self.game_repository = self.initialize_game_repository(is_dev)
        self.services = self.initialize_services(self.game_repository)
        self.controllers = self.initialize_controllers(self.services)
        self.router = self.initialize_router(self.controllers)
        self.text_parser = self.initialize_text_parser(
            self.router, self.game_repository
        )
        return self

    def handle_save_request(self: "AdventureGame") -> None:
        """Handle the save request."""
        self.text_parser.handle_game_input("savegame", False)

    def user_confirmed(self: "AdventureGame", response: str) -> bool:
        """Return True if the user confirmed the request."""
        return self.game_repository.language.is_confirmed(response)

    def print_exit_message(self: "AdventureGame") -> None:
        """Return a formatted message for exiting the game."""
        messages = [
            GameMessage.blank_line(),
            GameMessage.paragraph(
                "You have chosen to exit the game. Thanks for playing!"
            ),
            GameMessage.blank_line(),
            GameMessage.single_line("Press enter to continue..."),
        ]
        self.text_parser.print_list_of_messages(messages, False)
        input()

    def exit_game(self: "AdventureGame") -> None:
        """Exit the game."""
        self.print_exit_message()
        sys.exit()

    def try_handle_load_request(self: "AdventureGame") -> RequestStatus:
        """Ask the user if they want to load a game or start a new one."""
        # Check to see if there is a saved game
        has_saved_game = FileManager.has_saved_game()
        # If not, load a new game without asking
        if not has_saved_game:
            return self.text_parser.handle_game_input("newgame", False)

        # If so, ask the user if they want to load a game or start a new one
        message = "Would you like to load a saved game? (y/n)"
        messages = [
            GameMessage.blank_line(),
            GameMessage.paragraph(message),
        ]
        self.text_parser.print_list_of_messages(messages, False)
        response = input("    ")
        action = ""
        confirmed = self.user_confirmed(response)
        if confirmed and has_saved_game:
            action = "loadgame"
        else:
            action = "newgame"
        return self.text_parser.handle_game_input(action, False)

    def check_for_game_over(self: "AdventureGame") -> None:
        """Check to see if all the objectives are complete to win the game."""
        if self.game_repository.objectives.all_objectives_complete(
            self.game_repository.player
        ):
            self.game_repository.player.won = True

    def print_title(self: "AdventureGame") -> None:
        """Print the title of the game."""
        self.text_parser.handle_game_input("wax lyrical title", True)

    def print_introduction(self: "AdventureGame") -> None:
        """Print the introduction to the game."""
        self.text_parser.handle_game_input("wax lyrical introduction", True)

    def print_ending(self: "AdventureGame") -> None:
        """Print the ending to the game."""
        self.text_parser.handle_game_input("wax lyrical ending", True)

    def roll_end_credits(self: "AdventureGame") -> None:
        """Roll the end credits."""
        previous_delay = self.game_repository.scroll_delay
        self.game_repository.scroll_delay = GameRepository.slow_scroll_delay
        self.print_ending()
        self.game_repository.scroll_delay = previous_delay
        self.game_repository.player.watched_end_credits = True

    def draw_title_art(self: "AdventureGame") -> None:
        """Draws the title art."""
        print("\n")
        self.text_parser.handle_game_input("draw intro_art", True)
        print()

    def run(self: "AdventureGame") -> None:  # pragma: no cover
        """Run the adventure game."""
        self.draw_title_art()
        self.print_title()
        self.print_introduction()

        # Prompt the user to load or start a new game.
        status = self.try_handle_load_request()
        while status == RequestStatus.FAILURE:
            status = self.try_handle_load_request()  # pragma: no cover

        # Tell the user where they are currently standing when the game starts up.
        self.text_parser.display_look_request_on_startup()

        while self.game_repository.game_active:
            self.text_parser.handle_user_input()  # pragma: no cover
            self.check_for_game_over()  # pragma: no cover
            if (
                self.game_repository.player.won
                and not self.game_repository.player.watched_end_credits
            ):
                self.roll_end_credits()  # pragma: no cover

        if self.game_repository.state_dirty:
            messages = [
                GameMessage.blank_line(),
                GameMessage.paragraph(
                    "It looks like there are unsaved changes. Would you like to save the game?"
                ),
            ]
            self.text_parser.print_list_of_messages(messages, False)
            response = input("    ")
            if self.user_confirmed(response):
                self.handle_save_request()
            else:
                messages = [
                    GameMessage.blank_line(),
                    GameMessage.single_line("Your game has not been saved."),
                ]
                self.text_parser.print_list_of_messages(messages, False)
        self.exit_game()

    @staticmethod
    def is_dev() -> bool:
        """Parse command line arguments to check for development mode."""
        parser = argparse.ArgumentParser()  # pragma: no cover
        parser.add_argument(
            "-d",
            "--development",
            help="Run the game in development mode.",
            action="store_true",
        )  # pragma: no cover
        args = parser.parse_args()  # pragma: no cover
        return args.development  # pragma: no cover


if __name__ == "__main__":
    AdventureGame().initialize_game(AdventureGame.is_dev()).run()  # pragma: no cover
