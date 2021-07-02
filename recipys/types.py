from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RecipeConstraints:
    meal: Optional[str] = None
    ingredients: Optional[List[str]] = None


@dataclass
class RecipeInformation:
    title: str
    ingredients: str
    preparation: str


@dataclass
class FetchingError(Exception):
    message: str = "An error ocurred"
