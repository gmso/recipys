import sys
from typing import List, Tuple, AbstractSet


class ArgParser():
    """
    Command line arguments parser
    """

    def __init__(self, args: List[str]) -> None:
        """
        Initializes the argument parser.

        Args:
            - List[str]: arguments from command line
        """

        self.accepted_meals: AbstractSet[str] = {
            "breakfast", "lunch", "dinner", "dessert"}
        self.args: List[str] = args

    def parse(self) -> Tuple[str, List[str]]:
        """
        Parses command line arguments

        Returns:
            Tuple with:
                - str: meal name (default: None)
                - List[str]: list of ingredients (default: None)
        """

        self.meal: str = self._get_meal()
        self.ingredients: List[str] = self._get_ingredients()
        return (self.meal, self.ingredients)

    def _get_meal(self) -> str:
        """
        Gets meal type from command line argument

        Returns:
            - str: meal name (default: None)
        """
        if len(self.args) > 1:
            for accepted_meal in self.accepted_meals:
                if self.args[1] == accepted_meal:
                    return accepted_meal
        return None

    def _get_ingredients(self) -> List[str]:
        """
        Gets meal type from command line argument

        Returns:
            - str: meal name (default: None)
        """
        pass