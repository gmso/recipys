from recipys.ConsolePrinter import ConsolePrinter
from recipys.constants import (
    COLOR_HIGHLIGHT_SEARCHED_MEAL,
    COLOR_HIGHLIGHT_SEARCHED_INGREDIENT,
)

from recipys.types import Printable, RecipeConstraints


def test_ConsolePrinter(capsys):
    recipe = Printable(
        title="Mate",
        ingredients=("Yerba mate\n" "Water"),
        preparation=(
            "Pour Yerba into Mate\n"
            "Wash mate with water a few times\n"
            "Pour warm water into mate\n"
            "Enjoy!"
        ),
    )
    constraints = RecipeConstraints()

    ConsolePrinter(recipe, constraints).print_recipe()

    captured = capsys.readouterr()
    assert recipe.title in captured.out
    assert "Yerba mate" in captured.out
    assert "Wash mate with water" in captured.out


def test_ConsolePrinter_with_error(capsys):
    recipe = Printable(error_message="An error ocurred!")
    constraints = RecipeConstraints()

    ConsolePrinter(recipe, constraints).print_recipe()

    captured = capsys.readouterr()
    assert recipe.error_message in captured.out


def test_ConsolePrinter_with_warning(capsys):
    recipe = Printable(warning_message="Watch out for the following")
    constraints = RecipeConstraints()

    ConsolePrinter(recipe, constraints).print_recipe()

    captured = capsys.readouterr()
    assert recipe.warning_message in captured.out


def test_ConsolePrinter_with_info_message(capsys):
    recipe = Printable(info_message="You may want to know this:")
    constraints = RecipeConstraints()

    ConsolePrinter(recipe, constraints).print_recipe()

    captured = capsys.readouterr()
    assert recipe.info_message in captured.out


def test_ConsolePrinter_highlighted_meal_and_ingredients():
    recipe = Printable(
        title="Summer mate",
        ingredients=("Yerba mate\n" "Juice\n" "Ice"),
        preparation=(
            "Pour yerba into Mate\n"
            "Wash mate with water a few times\n"
            "Add ice cubes to mate\n"
            "Pour your favorite juice into mate\n"
            "Enjoy!"
        ),
    )
    constraints = RecipeConstraints(
        meal="mate", ingredients=["yerba", "juice"]
    )
    highlighted_mate: str = (
        f"[{COLOR_HIGHLIGHT_SEARCHED_MEAL}]"
        "mate"
        f"[/{COLOR_HIGHLIGHT_SEARCHED_MEAL}]"
    )
    highlighted_mate_uppercase: str = (
        f"[{COLOR_HIGHLIGHT_SEARCHED_MEAL}]"
        "Mate"
        f"[/{COLOR_HIGHLIGHT_SEARCHED_MEAL}]"
    )
    highlighted_yerba: str = (
        f"[{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
        "yerba"
        f"[/{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
    )
    highlighted_yerba_uppercase: str = (
        f"[{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
        "Yerba"
        f"[/{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
    )
    highlighted_juice: str = (
        f"[{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
        "juice"
        f"[/{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
    )
    highlighted_juice_uppercase: str = (
        f"[{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
        "Juice"
        f"[/{COLOR_HIGHLIGHT_SEARCHED_INGREDIENT}]"
    )

    printer = ConsolePrinter(recipe, constraints)
    printer.print_recipe()

    assert printer.recipe.ingredients == (
        f"{highlighted_yerba_uppercase} {highlighted_mate}\n"
        f"{highlighted_juice_uppercase}\n"
        "Ice"
    )

    assert printer.recipe.preparation == (
        f"Pour {highlighted_yerba} into {highlighted_mate_uppercase}\n"
        f"Wash {highlighted_mate} with water a few times\n"
        f"Add ice cubes to {highlighted_mate}\n"
        f"Pour your favorite {highlighted_juice} into "
        f"{highlighted_mate}\n"
        "Enjoy!"
    )
