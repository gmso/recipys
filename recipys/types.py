from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RecipeConstraints:
    meal: Optional[str] = None
    ingredients: Optional[List[str]] = None


@dataclass
class Printable:
    title: str = ""
    ingredients: str = ""
    preparation: str = ""
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    info_message: Optional[str] = None


@dataclass
class FetchingError(Exception):
    message: str = "An error ocurred"


@dataclass
class PrintInterrupt(Exception):
    printable: Printable
