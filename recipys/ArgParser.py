from dataclasses import dataclass
import re
from typing import List, Tuple, Optional

from recipys.types import RecipeConstraints


@dataclass
class ArgParser:
    """Command line arguments parser"""

    args: List[str]
    accepted_meals: Tuple[str] = (
        "breakfast",
        "lunch",
        "dinner",
        "dessert",
    )

    def parse(self) -> RecipeConstraints:
        """Parses command line arguments"""
        self.meal = self._get_meal()
        self.ingredients = self._get_ingredients()
        return RecipeConstraints(self.meal, self.ingredients)

    def _get_meal(self) -> Optional[str]:
        """Gets meal type from command line argument"""
        if len(self.args) > 1:
            for accepted_meal in self.accepted_meals:
                if self.args[1].lower() == accepted_meal:
                    return accepted_meal
        return None

    def _get_ingredients(self) -> Optional[List[str]]:
        """Gets meal type from command line argument"""
        args = [a.lower() for a in self.args]
        if "with" not in args:
            return None

        start: int = 2 if self.meal else 1

        if "with" != args[start]:
            return None

        ingredients: List[str] = []
        for _, arg in enumerate(args[start + 1 : :]):
            m = re.findall(r"[a-zA-Z]", arg)
            word = "".join(m)
            if word:
                ingredients.append(word)

        if not ingredients:
            return None

        return ingredients
