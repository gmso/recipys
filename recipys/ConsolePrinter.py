from dataclasses import dataclass

from rich import print
from rich.panel import Panel
from rich.console import RenderGroup

from recipys.types import RecipeInformation


@dataclass
class ConsolePrinter:
    """Prints recipe information to console"""

    recipe: RecipeInformation

    def print_recipe(self) -> None:
        """Print recipe or error message"""
        if self.recipe.error_message:
            self._print_recipe_error()
        else:
            self._print_recipe_info()

    def _print_recipe_info(self) -> None:
        """Print recipe info"""
        panel_recipe = Panel.fit(
            RenderGroup(
                self._make_inner_panel(self.recipe.ingredients, "Ingredients"),
                self._make_inner_panel(self.recipe.preparation, "Preparation"),
            ),
            title="[bold green1]" + self.recipe.title,
            border_style="bold green1",
            padding=(1, 1),
        )

        print("\n")
        print(panel_recipe)
        print("\n")

    def _print_recipe_error(self):
        panel_error = Panel.fit(
            RenderGroup(
                "[dark_orange3]The following error ocurred: ",
                self.recipe.error_message,
            ),
            title="[bold dark_orange3]" + "   ERROR   ",
            border_style="bold dark_orange3",
            padding=(1, 1),
        )

        print("\n")
        print(panel_error)
        print("\n")

    def _make_inner_panel(self, text: str, title: str) -> Panel:
        return Panel(
            text,
            title="[bold cyan1]" + title,
            padding=(1, 1),
            border_style="bold cyan1",
        )
