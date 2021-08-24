from dataclasses import dataclass
import re
from typing import Optional

from rich import print
from rich.panel import Panel
from rich.console import RenderGroup

from recipys.types import Printable, RecipeConstraints
from recipys.constants import (
    COLOR_RECIPE_MAIN,
    COLOR_RECIPE_SECONDARY,
    COLOR_ERROR,
    COLOR_WARNING,
    COLOR_INFORMATION,
    COLOR_HIGHLIGHT_SEARCHED_MEAL,
    COLOR_HIGHLIGHT_SEARCHED_INGREDIENT,
)


@dataclass
class ConsolePrinter:
    """Prints recipe information to console"""

    recipe: Printable
    recipe_constraints: RecipeConstraints

    def print_recipe(self) -> None:
        """Print recipe or error message"""
        if self.recipe.error_message:
            self._print_error()
        elif self.recipe.warning_message:
            self._print_warning()
        elif self.recipe.info_message:
            self._print_information()
        else:
            self._print_recipe_info()

    def _print_message(
        self,
        title: str,
        message: str,
        color: str = "white",
        subtitle: Optional[str] = None,
        render_group: Optional[RenderGroup] = None,
    ) -> None:
        """Generic print message"""
        if not render_group:
            render_group = RenderGroup(
                f"[{color}]{subtitle}",
                message,
            )
        panel = Panel.fit(
            render_group,
            title=f"[bold {color}]" + f"  {title}  ",
            border_style=f"bold {color}",
            padding=(1, 1),
            title_align="left",
        )
        print("\n")
        print(panel)
        print("\n")

    def _make_inner_panel(self, text: str, title: str) -> Panel:
        """Create interior panel for printed recipes"""
        return Panel(
            text,
            title=f"[bold {COLOR_RECIPE_SECONDARY}]" + title,
            padding=(1, 1),
            border_style=f"bold {COLOR_RECIPE_SECONDARY}",
            title_align="left",
        )

    def _print_recipe_info(self) -> None:
        """Print recipe info"""
        self._add_color_to_searched_terms()

        render_group = RenderGroup(
            self._make_inner_panel(self.recipe.ingredients, "Ingredients"),
            self._make_inner_panel(self.recipe.preparation, "Preparation"),
        )

        return self._print_message(
            title=self.recipe.title,
            message=self.recipe.warning_message,
            color=COLOR_RECIPE_MAIN,
            render_group=render_group,
        )

    def _print_error(self) -> None:
        """Print error message"""
        return self._print_message(
            title="ERROR",
            subtitle="The following error ocurred:",
            message=self.recipe.error_message,
            color=COLOR_ERROR,
        )

    def _print_warning(self):
        """Print warning message"""
        return self._print_message(
            title="Warning",
            subtitle="Heads up!",
            message=self.recipe.warning_message,
            color=COLOR_WARNING,
        )

    def _print_information(self):
        """Print information message"""
        return self._print_message(
            title=self.recipe.title,
            subtitle="Your requested info:",
            message=self.recipe.info_message,
            color=COLOR_INFORMATION,
        )

    def _add_color_to_searched_terms(self):
        """
        Add highlight color of searched terms (meal and ingredients)
        to printable recipe's ingredients and preparation
        """
        if self.recipe_constraints.meal:
            self.recipe.ingredients = self._add_color_tag(
                text=self.recipe.ingredients,
                word=self.recipe_constraints.meal,
                color=COLOR_HIGHLIGHT_SEARCHED_MEAL,
            )
            self.recipe.preparation = self._add_color_tag(
                text=self.recipe.preparation,
                word=self.recipe_constraints.meal,
                color=COLOR_HIGHLIGHT_SEARCHED_MEAL,
            )

        if self.recipe_constraints.ingredients:
            for ingredient in self.recipe_constraints.ingredients:
                self.recipe.ingredients = self._add_color_tag(
                    text=self.recipe.ingredients,
                    word=ingredient,
                    color=COLOR_HIGHLIGHT_SEARCHED_INGREDIENT,
                )
                self.recipe.preparation = self._add_color_tag(
                    text=self.recipe.preparation,
                    word=ingredient,
                    color=COLOR_HIGHLIGHT_SEARCHED_INGREDIENT,
                )

    def _add_color_tag(self, text: str, word: str, color: str) -> str:
        """Add color to word matches inside text

        Args:
            - text: text where word is contained
            - word: string which should recieve the color tags
            - color: color code to be added

        Returns:
            - text with added color tags around the words
        """
        text_with_colors = re.sub(
            pattern=fr"({word})",
            repl=fr"[{color}]\1[/{color}]",
            string=text,
            flags=re.IGNORECASE,
        )

        return text_with_colors
