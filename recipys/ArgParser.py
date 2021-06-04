import re
from typing import List, Tuple, AbstractSet, Optional


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

    def parse(self) -> Tuple[Optional[str], Optional[List[str]]]:
        """
        Parses command line arguments

        Returns:
            Tuple with:
                - str: meal name (default: None)
                - List[str]: list of ingredients (default: List[None])
        """

        self.meal: str = self._get_meal()
        self.ingredients: List[str] = self._get_ingredients()
        return (self.meal, self.ingredients)

    def _get_meal(self) -> Optional[str]:
        """
        Gets meal type from command line argument

        Returns:
            - str: meal name (default: None)
        """
        if len(self.args) > 1:
            for accepted_meal in self.accepted_meals:
                if self.args[1].lower() == accepted_meal:
                    return accepted_meal
        return None

    def _get_ingredients(self) -> Optional[List[str]]:
        """
        Gets meal type from command line argument

        Returns:
            - List[str]: list of valid ingredients (default: None)
        """
        args = [a.lower() for a in self.args]
        if "with" not in args:
            return None

        start: int = 2 if self.meal else 1

        if "with" != args[start]:
            return None

        ingredients: List[str] = []
        for _, arg in enumerate(args[start+1::]):
            m = re.findall(r"[a-zA-Z]", arg)
            word = "".join(m)
            if word:
                ingredients.append(word)

        if not ingredients:
            return None

        return ingredients
