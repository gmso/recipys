from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
import requests

from recipys.types import FetchingError


@dataclass
class HtmlSearchTarget:
    """Search target for HTML elements and their values"""

    name: str
    tag: Optional[str] = None
    att_name: Optional[str] = None
    att_value: Optional[str] = None
    target_element: Optional[str] = None  # If none, inner HTML is returned


@dataclass
class ScraperSearchTerms:
    """Search terms for scraper within HTML page"""

    target: HtmlSearchTarget
    return_multiple: bool = False  # If False, only first match is returned


@dataclass
class Scraper:
    """Scrapes content from website"""

    url: str
    search_terms: List[ScraperSearchTerms]

    def get(self) -> Dict[str, List[str]]:
        """Return found data as requested by search parameters"""
        self._http_response = requests.get(self.url)

        try:
            self._check_http_response_status()
        except ConnectionRefusedError:
            raise FetchingError(
                (
                    "HTTP request error. "
                    "Please check your internet connection and try again"
                )
            )

        self._html = self._http_response.text
        return self._parse()

    def _check_http_response_status(self) -> None:
        """Check response of http GET request
        - Raises: ConnectionRefusedError if request's status is invalid"""
        try:
            self._http_response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ConnectionRefusedError

    def _parse(self) -> Dict[str, List[str]]:
        """Return Dict with findings in HTML file according to search terms"""
        parsed_results: Dict[str, List[str]] = {}

        for search in self.search_terms:
            results: List[str] = []

            attributes = (
                {search.target.att_name: search.target.att_value}
                if (search.target.att_name and search.target.att_name)
                else None
            )

            soup = BeautifulSoup(self._html, "html.parser")
            tags = soup.find_all(
                name=search.target.tag,
                attrs=attributes,
            )

            for tag in tags:
                # Get only exact matches
                if attributes:
                    if not tag.get_attribute_list(
                        f"{search.target.att_name}"
                    ) == [f"{search.target.att_value}"]:
                        continue

                if search.target.target_element:
                    # Specific tag of element is searched
                    att_value = tag.attrs.get(
                        search.target.target_element, None
                    )
                    if att_value:
                        results.append(att_value)
                else:
                    # Inner HTML is searched
                    results.append(tag.text)

                # Break if we only need one result
                if not search.return_multiple:
                    break

            parsed_results.setdefault(search.target.name, results)

        return parsed_results
