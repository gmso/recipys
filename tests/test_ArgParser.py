from recipys.ArgParser import ArgParser
from utility_randoms import random_string


def test_ArgParser_construction():
    cla = ["recipys"]
    parser = ArgParser(cla)
    assert parser.accepted_meals == {
            "breakfast", "lunch", "dinner", "dessert"}
    assert parser.args


def test_no_arguments():
    cla = ["recipys"]
    parser = ArgParser(cla)
    assert parser.parse() == (None, None)


def test_meals_valid():
    cla = ["recipys", "breakfast"]
    parser = ArgParser(cla)
    assert parser.parse() == ("breakfast", None)

    cla = ["recipys", "lunch"]
    parser = ArgParser(cla)
    assert parser.parse() == ("lunch", None)

    cla = ["recipys", "dinner"]
    parser = ArgParser(cla)
    assert parser.parse() == ("dinner", None)

    cla = ["recipys", "dessert"]
    parser = ArgParser(cla)
    assert parser.parse() == ("dessert", None)


def test_meals_invalid():
    cla = ["recipys", "desssert"]
    parser = ArgParser(cla)
    assert parser.parse() == (None, None)

    cla = ["recipys", ","]
    parser = ArgParser(cla)
    assert parser.parse() == (None, None)

    for w in range(10):
        cla = ["recipys", random_string()]
        parser = ArgParser(cla)
        assert parser.parse() == (None, None)
