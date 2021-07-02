from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import requests


@dataclass
class RecipeFetcher:
    """
    Fetches recipes from the web
    """
    url_base: str = (
        "https://www.recipe-free.com/recipe"
    )
    url_suffix: str = "search"
    url_page_number: int = 1
    meal: Optional[str] = None
    ingredients: Optional[List[str]] = None
    recipe_found: bool = False

    def fetch_recipe(
        self, meal: Optional[str], ingredients: Optional[List[str]]
    ) -> Dict[str, str]:
        """
        Fetches recipe according to user input

        Args:
            - meal: name of meal type to search (default: None)
            - ingredients: list of ingredients (default: None)

        Returns:
            - Dictionary with meal information (name, ingredients,
                preparation, error)
        """
        (self.meal, self.ingredients) = (meal, ingredients)

    def _get_payload(self) -> str:
        """
        Get payload used as arguments for query of HTTP GET request

        Returns:
            - payload for GET request as string
        """
        payload: Dict[str, str] = {}

        if self.meal:
            payload.setdefault(self.url_prefix_meal, self.meal)

        if self.ingredients:
            payload.setdefault(
                self.url_prefix_ingredients, ",".join(self.ingredients)
            )

        if self.url_page_number != 0:
            payload.setdefault(self.url_prefix_page, self.url_page_number)

        return payload
