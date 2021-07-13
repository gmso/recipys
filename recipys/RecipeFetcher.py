from dataclasses import dataclass
import re
from time import sleep
import random

from recipys.types import RecipeConstraints, Printable, FetchingError
from recipys.Scraper import (
    Scraper,
    ScraperSearchTerms,
    HtmlSearchTarget,
)
from recipys.constants import WAIT_BETWEEN_PINGS, KEY_STRINGS_CUT_FROM_RECIPE


@dataclass
class RecipeFetcher:
    """Fetches recipes from the web"""

    recipe_constraints: RecipeConstraints

    def fetch(self) -> Printable:
        """Fetches recipe according to user input"""
        try:
            self.recipe_url = self._scrape_recipe_url()
            sleep(WAIT_BETWEEN_PINGS)
            recipe = self._scrape_recipe()
            return recipe
        except FetchingError as e:
            return Printable(error_message=e.message)

    def _create_url_recipe_search(self) -> str:
        """Get URL for HTTP GET request"""
        url_base: str = "https://www.recipe-free.com/recipe/"

        if not hasattr(self, "_target_page_recipe_list"):
            self._target_page_recipe_list: str = "1"
        url_suffix: str = f"/{self._target_page_recipe_list}/search"

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
            return (
                "https://www.recipe-free.com/recipe/best/"
                f"{self._target_page_recipe_list}"
            )

    def _create_search_terms_recipe_search(self) -> None:
        """Creates search terms used to search for recipe url"""
        if not hasattr(self, "terms_recipe_list"):
            self.terms_recipe_list = ScraperSearchTerms(
                target=HtmlSearchTarget(
                    name="Recipe",
                    tag="a",
                    att_name="class",
                    att_value="day",
                    target_element="href",
                ),
                return_multiple=True,
            )
        if not hasattr(self, "terms_pages_with_recipes"):
            self.terms_pages_with_recipes = ScraperSearchTerms(
                target=HtmlSearchTarget(
                    name="Pages",
                    tag="span",
                    att_name="class",
                    att_value="f12 f12",
                )
            )

    def _scrape_recipe_url(self) -> str:
        """Scrape url of recipe according to search constraints"""
        self._create_search_terms_recipe_search()
        self._url_recipe_list = self._create_url_recipe_search()

        scraper = Scraper(
            url=self._url_recipe_list,
            search_terms=[
                self.terms_recipe_list,
                self.terms_pages_with_recipes,
            ],
        )
        scraped_data = scraper.get()

        try:
            pages_text = scraped_data.get("Pages")[0]
            if not self._is_current_recipe_page_the_right_one(pages_text):
                sleep(WAIT_BETWEEN_PINGS)
                return self._scrape_recipe_url()

            recipes_urls = scraped_data.get("Recipe")
            return random.choice(recipes_urls)

        except IndexError:
            raise FetchingError(
                "No recipe found with your criteria. "
                "Maybe try removing or changing your filters "
                "to broaden your search? Using only ingredients could help!"
            )

    def _scrape_recipe(self) -> Printable:
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
            return Printable(
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

    def _beautify(self, text: str) -> str:
        """Return beautified text from parsed html

        Args:
            - text: text to be beautified
        """

        # Remove metadata if key string found
        pos_to_cut: int = 0
        text_lowercase = text.lower()
        for key in KEY_STRINGS_CUT_FROM_RECIPE:
            substring_position = text_lowercase.find(key)
            if substring_position != -1:
                # Substring found
                if pos_to_cut == 0:
                    pos_to_cut = substring_position
                else:
                    pos_to_cut = min(pos_to_cut, substring_position)
        text_without_metadata = text[:pos_to_cut] if pos_to_cut else text

        # Remove multiple spaces and leading and trailing spaces
        return re.sub(" +", " ", text_without_metadata).strip()

    def _is_current_recipe_page_the_right_one(self, text: str) -> bool:
        """Determine if we are in the right page of recipe listing

        Args:
            - text: Inner HTML text of total pages information
        """
        if hasattr(self, "_determined_target_page"):
            return True

        regex = re.compile(r"Results (\d).+?\(de (.*?)\) recipes")
        m = regex.match(text)

        recipes_per_page: int = 10

        current_page = (int(m.group(1)) // recipes_per_page) + 1

        recipes_total = int(m.group(2).replace(",", ""))
        pages_total: int = (recipes_total // recipes_per_page) + 1

        target_page: int = random.randint(1, pages_total)
        self._target_page_recipe_list = str(target_page)

        self._determined_target_page: bool = True

        return target_page == current_page
