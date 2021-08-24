import sys

from recipys.ArgParser import ArgParser
from recipys.ConsolePrinter import ConsolePrinter
from recipys.ProgressBar import ProgressBar
from recipys.RecipeFetcher import RecipeFetcher
from recipys.request_wait import wait_for_green_light
from recipys.types import PrintInterrupt, RecipeConstraints


def main():
    """Main entry point of app"""

    # Create progress bar
    with ProgressBar(total_steps=4) as bar:

        wait_for_green_light()

        try:
            bar.advance()
            recipe_constraints = ArgParser(sys.argv).parse()
        except PrintInterrupt as e:
            bar.advance()
            recipe_constraints = RecipeConstraints(None, None)
            recipe = e.printable
        else:
            bar.advance()
            recipe = RecipeFetcher(recipe_constraints).fetch()
        finally:
            bar.advance()
            ConsolePrinter(recipe, recipe_constraints).print_recipe()


if __name__ == "__main__":
    main()  # pragma: no cover
