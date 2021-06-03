import re
from recipys.ArgParser import ArgParser
from utility_randoms import random_string


def test_ArgParser_construction():
    parser = ArgParser(["recipys"])
    assert parser.accepted_meals == {
            "breakfast", "lunch", "dinner", "dessert"}
    assert parser.args


def test_no_arguments():
    parser = ArgParser(["recipys"])
    assert parser.parse() == (None, None)


def test_meals_valid():
    parser = ArgParser(["recipys", "breakfast"])
    assert parser.parse() == ("breakfast", None)

    parser = ArgParser(["recipys", "lunch"])
    assert parser.parse() == ("lunch", None)

    parser = ArgParser(["recipys", "dinner"])
    assert parser.parse() == ("dinner", None)

    parser = ArgParser(["recipys", "dessert"])
    assert parser.parse() == ("dessert", None)


def test_meals_invalid():
    parser = ArgParser(["recipys", "desssert"])
    assert parser.parse() == (None, None)

    parser = ArgParser(["recipys", "a", "lunch"])
    assert parser.parse() == (None, None)

    for w in range(10):
        parser = ArgParser(["recipys", random_string()])
        assert parser.parse() == (None, None)


def test_ingredients_valid():
    parser = ArgParser(["recipys", "with", "banana"])
    assert parser.parse() == (None, ["banana"])

    parser = ArgParser(["recipys", "with", "garlic", "onion"])
    assert parser.parse() == (None, ["garlic", "onion"])
    
    parser = ArgParser(["recipys", "with", "'*'#potato+´?."])
    assert parser.parse() == (None, ["potato"])

    for w in range(10):
        rand_string = random_string()
        parser = ArgParser(["recipys", "with", rand_string])
        word  = "".join(re.findall(r"\w",rand_string))
        if word:
            assert parser.parse() == (None, [word])
        else:
            assert parser.parse() == (None, None)


def test_ingredients_invalid():
    parser = ArgParser(["recipys", "banana"]) # "with" missing
    assert parser.parse() == (None, None)
    
    parser = ArgParser(["recipys", "chocolate", "with"]) # "with" misplaced
    assert parser.parse() == (None, None)
    
    parser = ArgParser(["recipys", "with", "..."]) # invalid ingredient
    assert parser.parse() == (None, None)

    # one valid ingredient, invalid ingredients ignored
    parser = ArgParser(["recipys", "with", "...", "???", "apple"])
    assert parser.parse() == (None, ["apple"])
