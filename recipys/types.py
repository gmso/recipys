from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RecipeConstraints:
    meal: Optional[str] = None
    ingredients: Optional[List[str]] = None