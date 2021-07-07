from recipys.types import Printable
from recipys.ConsolePrinter import ConsolePrinter


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

    ConsolePrinter(recipe).print_recipe()

    captured = capsys.readouterr()
    assert recipe.title in captured.out
    assert "Yerba mate" in captured.out
    assert "Wash mate with water" in captured.out


def test_ConsolePrinter_with_error(capsys):
    recipe = Printable(error_message="An error ocurred!")

    ConsolePrinter(recipe).print_recipe()

    captured = capsys.readouterr()
    assert recipe.error_message in captured.out
