from unittest.mock import patch
from time import sleep

import pytest

from recipys.RecipeFetcher import RecipeFetcher
from recipys.types import RecipeConstraints, FetchingError


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
    assert fetcher._get_url_recipe() == (
        "https://www.recipe-free.com/recipe/breakfast-egg-cheese/1/search"
    )

    fetcher = RecipeFetcher(CONSTRAINTS_MEAL)
    assert fetcher._get_url_recipe() == (
        "https://www.recipe-free.com/recipe/lunch/1/search"
    )

    fetcher = RecipeFetcher(CONSTRAINTS_INGS)
    assert fetcher._get_url_recipe() == (
        "https://www.recipe-free.com/recipe/peas/1/search"
    )

    fetcher = RecipeFetcher(CONSTRAINTS_NONE)
    assert fetcher._get_url_recipe() == (
        "https://www.recipe-free.com/best-recipes/1"
    )


def test_scrape_recipe_url():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    url = fetcher._scrape_recipe_url()
    assert url == (
        "https://www.recipe-free.com/recipes/"
        "savory-breakfast-dish-bacon-eggs-cheese/83514"
    )

    with patch("recipys.Scraper.Scraper.get") as _get:
        _get.return_value = {"Recipe": []}
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
    assert recipe.ingredients == (
        "See below ingredients and instructions of the recipe"
    )
    assert "1 1/2 c LIGHT CREAM" in recipe.preparation

    with patch("recipys.Scraper.Scraper.get") as _get:
        _get.return_value = {"Recipe": []}
        with pytest.raises(FetchingError):
            fetcher._scrape_recipe()


def test_fetch_recipe():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(CONSTRAINTS_ALL)
    recipe = fetcher.fetch()
    assert recipe.title == "Savory breakfast dish~ bacon~ eggs cheese"
    assert recipe.ingredients == (
        "See below ingredients and instructions of the recipe"
    )
    assert "1 1/2 c LIGHT CREAM" in recipe.preparation


def test_fetch_recipe_with_error():
    with patch("recipys.RecipeFetcher.RecipeFetcher._scrape_recipe_url") as p:
        fetcher = RecipeFetcher(CONSTRAINTS_ALL)

        # Cause function to raise Exception
        def exception_raiser():
            raise FetchingError

        p.return_value = "https://www.google.com/not_a_valid_route"
        recipe = fetcher.fetch()

        assert recipe.error_message


def test_scrape_recipe_url_case_1():
    sleep(1)  # wait to avoid fetching data too quickly (ethical scraping)
    fetcher = RecipeFetcher(RecipeConstraints("dinner", ["broccoli"]))

    with pytest.raises(FetchingError):
        fetcher._scrape_recipe_url()
