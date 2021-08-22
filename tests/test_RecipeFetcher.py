from unittest.mock import patch
from time import sleep

import pytest

from recipys.RecipeFetcher import RecipeFetcher
from recipys.types import RecipeConstraints, FetchingError
from recipys.constants import (
    KEY_STRINGS_CUT_FROM_RECIPE,
    KEY_STRINGS_INGREDIENTS_MISSING,
)


CONSTRAINTS_ALL = RecipeConstraints("breakfast", ["egg", "cheese"])
CONSTRAINTS_MEAL = RecipeConstraints("lunch", None)
CONSTRAINTS_INGS = RecipeConstraints(None, ["peas"])
CONSTRAINTS_NONE = RecipeConstraints(None, None)

HTML_EMTPY: str = """\
<div class="someclass">
    Basically nothing
</div>
"""
HTML_RECIPE_LIST: str = """\
<div class="recipe_row">
    <div class="tile">
        <a class="day" title="Savory breakfast dish~ bacon~ eggs  cheese" \
            href="https://www.recipe-free.com/recipes/savory-breakfast-dish\
                -bacon-eggs-cheese/83514">
            Savory breakfast dish~ bacon~ eggs  cheese
        </a>
    </div>
</div>
"""


def test_RecipeFetcher_construction():
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    assert fetcher.recipe_constraints.meal == "breakfast"
    assert fetcher.recipe_constraints.ingredients == ["egg", "cheese"]

    fetcher = RecipeFetcher(CONSTRAINTS_MEAL)
    assert fetcher.recipe_constraints.meal == "lunch"
    assert fetcher.recipe_constraints.ingredients is None

    fetcher = RecipeFetcher(CONSTRAINTS_INGS)
    assert fetcher.recipe_constraints.meal is None
    assert fetcher.recipe_constraints.ingredients == ["peas"]

    fetcher = RecipeFetcher(CONSTRAINTS_NONE)
    assert fetcher.recipe_constraints.meal is None
    assert fetcher.recipe_constraints.ingredients is None


def test_get_url_recipe():
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    assert fetcher._create_url_recipe_search() == (
        "https://www.recipe-free.com/recipe/breakfast-egg-cheese/1/search"
    )

    fetcher = RecipeFetcher(CONSTRAINTS_MEAL)
    assert fetcher._create_url_recipe_search() == (
        "https://www.recipe-free.com/recipe/lunch/1/search"
    )

    fetcher = RecipeFetcher(CONSTRAINTS_INGS)
    assert fetcher._create_url_recipe_search() == (
        "https://www.recipe-free.com/recipe/peas/1/search"
    )

    fetcher = RecipeFetcher(CONSTRAINTS_NONE)
    assert fetcher._create_url_recipe_search() == (
        "https://www.recipe-free.com/recipe/best/1"
    )


def test_scrape_recipe_url():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    url = fetcher._scrape_recipe_url()
    assert "savory-breakfast-dish-bacon" in url

    with patch("recipys.Scraper.Scraper.get") as _get:
        _get.return_value = {"Recipe": [], "Pages": []}
        with pytest.raises(FetchingError):
            url = fetcher._scrape_recipe_url()


def test_scrape_recipe():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    fetcher.recipe_url = (
        "https://www.recipe-free.com/recipes/"
        "savory-breakfast-dish-bacon-eggs-cheese/83514"
    )
    recipe = fetcher._scrape_recipe()
    assert recipe.title == "Savory breakfast dish~ bacon~ eggs cheese"
    assert recipe.ingredients != (
        "See below ingredients and instructions of the recipe"
    )
    assert "COMBINE CHEESE, EGGS, BACON" in recipe.preparation

    with patch("recipys.Scraper.Scraper.get") as _get:
        _get.return_value = {"Recipe": []}
        with pytest.raises(FetchingError):
            fetcher._scrape_recipe()


def test_fetch_recipe():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    recipe = fetcher.fetch()
    assert recipe.title
    assert recipe.ingredients
    assert recipe.preparation


def test_fetch_recipe_with_error():
    with patch("recipys.RecipeFetcher.RecipeFetcher._scrape_recipe_url") as p:
        fetcher = RecipeFetcher(CONSTRAINTS_ALL)

        # Cause function to raise Exception
        def exception_raiser():
            raise FetchingError

        p.return_value = "https://www.google.com/not_a_valid_route"
        recipe = fetcher.fetch()

        assert recipe.error_message


def test_scrape_recipe_url_no_recipes_found():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(RecipeConstraints("dinner", ["broccoli"]))

    with pytest.raises(FetchingError):
        fetcher._scrape_recipe_url()


def test_scrape_recipe_url_load_new_page():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(CONSTRAINTS_NONE)
    assert not hasattr(fetcher, "._determined_target_page")
    assert not hasattr(fetcher, "._target_page_recipe_list")

    with patch("random.randint") as p_randit:
        patched_target_page = 39
        p_randit.return_value = patched_target_page
        fetcher._scrape_recipe_url()
        assert str(patched_target_page) in fetcher._url_recipe_list
        assert fetcher._determined_target_page
        assert fetcher._target_page_recipe_list == str(patched_target_page)


def test_beautify_recipe():
    fetcher = RecipeFetcher(CONSTRAINTS_NONE)
    base_text: str = "  This   recipe is prepared ...\n and finished!    "
    expected_text: str = "This recipe is prepared ...\nand finished!"
    text_after_match: str = "this should be cut from the recipe"

    for string in KEY_STRINGS_CUT_FROM_RECIPE:
        beautified_text = fetcher._beautify(
            base_text + string + text_after_match
        )
        assert beautified_text == expected_text

    # Now with several keys: the first one determines the cut
    beautified_text = fetcher._beautify(
        base_text
        + KEY_STRINGS_CUT_FROM_RECIPE[1].upper()  # should be case insensitive
        + "text being cut"
        + KEY_STRINGS_CUT_FROM_RECIPE[0]
        + text_after_match
    )

    assert beautified_text == expected_text


def test_beautify_real_recipe():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(RecipeConstraints("breakfast", ["salad"]))
    recipe = fetcher.fetch()
    assert recipe.title
    assert recipe.ingredients
    assert recipe.preparation
    assert "recipe by: " not in recipe.preparation.lower()


def test_extract_ingredients_from_preparation():
    fetcher = RecipeFetcher(CONSTRAINTS_NONE)

    # Case: ingredients empty and dividing string present
    initial_preparation: str = (
        "1.Ingredient\n2.Ingredient\n3.Ingredient"
        "\n\nPreparation\nPreparation\n"
    )
    for inital_ingredients in KEY_STRINGS_INGREDIENTS_MISSING:
        (
            ingredients,
            preparation,
        ) = fetcher._extract_ingredients_from_preparation(
            inital_ingredients,
            initial_preparation,
        )
        # Ingredients and preparation changed
        assert ingredients == "1.Ingredient\n2.Ingredient\n3.Ingredient"
        assert preparation == "Preparation\nPreparation"

    # Case: ingredients empty/invalid but no dividing string present
    initial_preparation: str = (
        "1.Ingredient\n2.Ingredient\n3.Ingredient"
        "\nPreparation\nPreparation\n"
    )
    inital_ingredients: str = KEY_STRINGS_INGREDIENTS_MISSING[0]
    (
        ingredients,
        preparation,
    ) = fetcher._extract_ingredients_from_preparation(
        inital_ingredients,
        initial_preparation,
    )
    # Ingredients and preparation DID NOT change
    assert ingredients == inital_ingredients
    assert preparation == initial_preparation

    # Case: ingredients valid
    initial_preparation: str = (
        "1.Ingredient\n2.Ingredient\n3.Ingredient"
        "\n\nPreparation\nPreparation\n"
    )
    inital_ingredients: str = "1. Lettuce\n2. Tomatoes"
    (
        ingredients,
        preparation,
    ) = fetcher._extract_ingredients_from_preparation(
        inital_ingredients,
        initial_preparation,
    )
    # Ingredients and preparation DID NOT change
    assert ingredients == inital_ingredients
    assert preparation == initial_preparation


def test_extract_ingredients_from_preparation_real_recipe():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(RecipeConstraints("breakfast", ["salad"]))
    recipe = fetcher.fetch()
    assert recipe.title
    assert "See below ingredients" not in recipe.ingredients
    assert "Cucumbers" in recipe.ingredients
    assert "Cucumbers" not in recipe.preparation
    assert "Vegetables" in recipe.preparation
