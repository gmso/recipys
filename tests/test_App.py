import sys

from utility_fixtures import config_file_cleanup

from recipys.App import main
from recipys.constants import MESSAGE_INVALID_ARGS


def test_App_valid_search(config_file_cleanup, capsys):
    sys.argv = ["recipys", "breakfast", "with", "egg", "cheese"]

    main()

    captured = capsys.readouterr()

    assert "Savory breakfast dish" in captured.out
    assert "See below ingredients and instructions" in captured.out
    assert "1 1/2 c LIGHT CREAM" in captured.out


def test_App_invalid_arguments(config_file_cleanup, capsys):
    sys.argv = ["recipys", "brickfast"]

    main()

    captured = capsys.readouterr()

    assert MESSAGE_INVALID_ARGS[:20] in captured.out
