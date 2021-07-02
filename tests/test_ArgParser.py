import re
from utility_randoms import random_string

from recipys.ArgParser import ArgParser


def test_ArgParser_construction():
    parser = ArgParser(["recipys"])
    assert parser.accepted_meals == ("breakfast", "lunch", "dinner", "dessert")
    assert parser.args


def test_no_arguments():
    constraints = ArgParser(["recipys"]).parse()
    assert not constraints.meal
    assert not constraints.ingredients


def test_meals_valid():
    constraints = ArgParser(["recipys", "breakfast"]).parse()
    assert constraints.meal == "breakfast"
    assert not constraints.ingredients

    constraints = ArgParser(["recipys", "LUNCH"]).parse()
    assert constraints.meal == "lunch"
    assert not constraints.ingredients

    constraints = ArgParser(["recipys", "Dinner"]).parse()
    assert constraints.meal == "dinner"
    assert not constraints.ingredients

    constraints = ArgParser(["recipys", "dEsSeRT"]).parse()
    assert constraints.meal == "dessert"
    assert not constraints.ingredients


def test_meals_invalid():
    constraints = ArgParser(["recipys", "desssert"]).parse()
    assert not constraints.meal
    assert not constraints.ingredients

    constraints = ArgParser(["recipys", "a", "lunch"]).parse()
    assert not constraints.meal
    assert not constraints.ingredients

    for w in range(10):
        constraints = ArgParser(["recipys", random_string()]).parse()
        assert not constraints.meal
        assert not constraints.ingredients


def test_ingredients_valid():
    constraints = ArgParser(["recipys", "with", "banana"]).parse()
    assert not constraints.meal
    assert constraints.ingredients == ["banana"]

    constraints = ArgParser(["recipys", "with", "garlic", "onion"]).parse()
    assert not constraints.meal
    assert constraints.ingredients == ["garlic", "onion"]

    constraints = ArgParser(["recipys", "with", "'*'#potato+´?."]).parse()
    assert not constraints.meal
    assert constraints.ingredients == ["potato"]

    for w in range(10):
        rand_string = random_string()
        constraints = ArgParser(["recipys", "with", rand_string]).parse()
        word = "".join(re.findall(r"[a-zA-Z]", rand_string)).lower()
        if word:
            assert not constraints.meal
            assert constraints.ingredients == [word]
        else:
            assert not constraints.meal
            assert not constraints.ingredients


def test_ingredients_invalid():
    # "with" missing
    constraints = ArgParser(["recipys", "banana"]).parse()
    assert not constraints.meal
    assert not constraints.ingredients

    # "with" misplaced
    constraints = ArgParser(["recipys", "chocolate", "with"]).parse()
    assert not constraints.meal
    assert not constraints.ingredients

    # invalid ingredient
    constraints = ArgParser(["recipys", "with", "..."]).parse()
    assert not constraints.meal
    assert not constraints.ingredients

    # one valid ingredient, invalid ingredients ignored
    constraints = ArgParser(["recipys", "with", "...", "???", "apple"]).parse()
    assert not constraints.meal
    assert constraints.ingredients == ["apple"]


def test_mixed_valid():
    constraints = ArgParser(["recipys", "breakfast", "with", "oats"]).parse()
    assert constraints.meal == "breakfast"
    assert constraints.ingredients == ["oats"]

    constraints = ArgParser(
        ["recipys", "lunch", "WitH", "BEEF", "eGGs"]
    ).parse()
    assert constraints.meal == "lunch"
    assert constraints.ingredients == ["beef", "eggs"]

    constraints = ArgParser(
        ["recipys", "dessert", "with", "*`+#+*pe*´+.a45r"]
    ).parse()
    assert constraints.meal == "dessert"
    assert constraints.ingredients == ["pear"]
