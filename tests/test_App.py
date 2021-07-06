import sys
from recipys.App import main
from utility_fixtures import config_file_cleanup


def test_App(config_file_cleanup, capsys):
    sys.argv = ["recipys", "breakfast", "with", "egg", "cheese"]

    main()

    captured = capsys.readouterr()

    assert "Savory breakfast dish" in captured.out
    assert "See below ingredients and instructions" in captured.out
    assert "1 1/2 c LIGHT CREAM" in captured.out
