from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Type

from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    BarColumn,
)


@dataclass
class ProgressBar:
    """Manage progress bar displayed while waiting for recipe"""

    total_steps: int

    def __post_init__(self):
        """Initialize members after __init__"""
        self._message = "Fetching recipe"
        self._color = "green"
        self._progress: Progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=True,
        )
        self._task: TaskID = self._progress.add_task(
            f"[{self._color}]{self._message}", total=self.total_steps
        )

    def __enter__(self) -> "Progress":
        """Enter function for context manager"""
        print("\n")
        self._progress.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit function for context manager"""
        self._progress.stop()

    def advance(self):
        """Advance progress bar to next step"""
        self._progress.update(self._task, advance=1)
