from dataclasses import dataclass
import re

from recipys.types import RecipeConstraints, RecipeInformation, FetchingError
from recipys.Scraper import (
    Scraper,
    ScraperSearchTerms,
    HtmlSearchTarget,
)


@dataclass
class RecipeFetcher:
    """Fetches recipes from the web"""

    recipe_constraints: RecipeConstraints

    def fetch_recipe(self) -> RecipeInformation:
        """Fetches recipe according to user input"""
        self.recipe_url = self._scrape_recipe_url()
        return self._scrape_recipe()

    def _get_url_recipe(self) -> str:
        """Get URL for HTTP GET request"""
        url_base: str = "https://www.recipe-free.com/recipe/"
        url_suffix: str = "/1/search"
        ings = (
            self.recipe_constraints.ingredients
            if self.recipe_constraints.ingredients
            else [None]
        )
        query = [self.recipe_constraints.meal] + ings
        clean_query = [e for e in query if e]

        if clean_query:
            return url_base + "-".join(clean_query) + url_suffix
        else:
            return "https://www.recipe-free.com/best-recipes/1"

    def _scrape_recipe_url(self) -> str:
        """Scrape url of recipe according to search constraints"""
        scraper = Scraper(
            url=self._get_url_recipe(),
            search_terms=[
                ScraperSearchTerms(
                    target=HtmlSearchTarget(
                        name="Recipe",
                        tag="a",
                        att_name="class",
                        att_value="day",
                        target_element="href",
                    )
                )
            ],
        )

        recipe_url = scraper.get().get("Recipe")[0]
        if not recipe_url:
            raise FetchingError(
                "No recipe found with your criteria. "
                "Maybe try removing or changing your filters to broaden your search?"
            )

        return recipe_url

    def _scrape_recipe(self) -> RecipeInformation:
        """Scrape recipe information from its URL"""
        scraper = self._setup_scraper_recipe()
        results = scraper.get()

        try:
            recipe_title = self._beautify(results["Title"][0])
            recipe_ingredients = self._beautify(
                results["Ingredients & Preparation"][0]
            )
            recipe_preparation = self._beautify(
                results["Ingredients & Preparation"][1]
            )
        except KeyError or IndexError:
            raise FetchingError("Recipe format incorrect. Please try again")
        else:
            return RecipeInformation(
                title=recipe_title,
                ingredients=recipe_ingredients,
                preparation=recipe_preparation,
            )

    def _setup_scraper_recipe(self) -> Scraper:
        """Setup Scraper object to be used scraping recipe from its page"""
        target_title = HtmlSearchTarget(
            name="Title",
            tag="h1",
            att_name="class",
            att_value="red",
        )
        target_ings_and_prep = HtmlSearchTarget(
            name="Ingredients & Preparation",
            tag="p",
            att_name="style",
            att_value="padding-left: 30px",
        )

        search_terms_title = ScraperSearchTerms(target=target_title)
        search_terms_ings_and_prep = ScraperSearchTerms(
            target=target_ings_and_prep, return_multiple=True
        )

        scraper = Scraper(
            url=self.recipe_url,
            search_terms=[
                search_terms_title,
                search_terms_ings_and_prep,
            ],
        )

        return scraper

    def _beautify(self, text: str):
        """Return beautified text from parsed html"""

        # Remove multiple spaces and leading and trailing spaces
        return re.sub(" +", " ", text).strip()
