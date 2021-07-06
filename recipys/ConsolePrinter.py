from dataclasses import dataclass

# from rich import print

from recipys.types import RecipeInformation


@dataclass
class ConsolePrinter:
    """Prints recipe information to console"""

    recipe: RecipeInformation

    def print_recipe(self) -> None:
        """Print recipe"""
        if self.recipe.error_message:
            print(self.recipe.error_message)
        else:
            print(self.recipe.title)
            print(self.recipe.ingredients)
            print(self.recipe.preparation)
