from typing import Dict, List, Optional, Tuple
import requests


class RecipeFetcher:
    """
    Fetches recipes from the web
    """

    def __init__(self) -> None:
        """
        Initialize instance variables
        """
        self.url_base: str = (
            "http://www.recipepuppy.com/api/"
            # ALTERNATIVE: www.recipe-free.com
        )
        self.url_prefix_meal: str = "q"
        self.url_prefix_ingredients: str = "i"
        self.url_prefix_page: str = "p"
        self.url_page_number: int = 1
        self.whitelist_targets: List[str] = ["recipeezaar"]
        self.meal: Optional[str] = None
        self.ingredients: Optional[List[str]] = None
        self.recipe_found: bool = False

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

        try:
            while not self.recipe_found:
                api_response = self._recipe_api_get_request()
                self.recipe_found = self._check_valid_target_in_api_response()
        except ConnectionRefusedError:
            return {"error": "HTTP request error. Please try again"}

    def _recipe_api_get_request(self) -> Dict[str, str]:
        """
        Request recipe from API provider

        Returns:
            - Dictionary json response of API
        """
        payload = self._get_payload()
        res = requests.get(self.url_base, params=payload)
        self._check_http_response_status(res)
        return self._convert_http_response_to_json(res)

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

    def _check_http_response_status(self, res: requests.Response) -> None:
        """
        Check response of http GET request

        Raises:
            - ConnectionRefuserError if request's status is invalid
        """
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ConnectionRefusedError

    def _convert_http_response_to_json(
        self, res: requests.Response
    ) -> Dict[str, str]:
        """
        Convert response of HTTP GET request to json

        Raises:
            - ConnectionRefuserError if response cannot be converted from json
        """
        try:
            api_response = res.json()
        except ValueError:
            raise ConnectionRefusedError
        else:
            return api_response

    def _is_whitelisted_target_in_api_response(self) -> Tuple[bool, int]:
        """
        Check if the api response has a whitelisted target in its content

        Returns:
            - bool flag to indicate if accepted recipe was found
            - page number in which recipe was found
        """
        return (False, 1)
