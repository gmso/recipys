import sys
from recipys.ArgParser import ArgParser
from recipys.ConsolePrinter import ConsolePrinter
from recipys.RecipeFetcher import RecipeFetcher
from recipys.request_wait import wait_for_green_light
from recipys.types import PrintInterrupt


def main():
    """Main entry point of app"""

    wait_for_green_light()

    try:
        recipe_constraints = ArgParser(sys.argv).parse()
    except PrintInterrupt as e:
        recipe = e.printable
    else:
        recipe = RecipeFetcher(recipe_constraints).fetch()
    finally:
        ConsolePrinter(recipe).print_recipe()


if __name__ == "__main__":
    main()  # pragma: no cover
