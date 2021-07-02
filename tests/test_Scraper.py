from unittest.mock import patch
from typing import List, Dict

import pytest
import requests

from recipys.Scraper import HtmlSearchTarget, Scraper, ScraperSearchTerms
from recipys.types import FetchingError


HTML_PAGE: str = """\
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>"""


def test_Scraper_construction():
    target = HtmlSearchTarget("Title of document", "class", "title")
    terms = [ScraperSearchTerms(target)]
    scraper = Scraper("https://www.somewebsite.com", terms)
    assert scraper.url == "https://www.somewebsite.com"
    assert isinstance(terms, List)


def test_check_http_response_status():
    target = HtmlSearchTarget("Title of document", "class", "title")
    terms = [ScraperSearchTerms(target)]
    scraper = Scraper("https://www.somewebsite.com", terms)

    with patch("requests.models.Request") as patched_Request:
        instance = patched_Request.return_value
        instance.raise_for_status.return_value = "valid"

        # assert no exception
        scraper._http_response = instance
        scraper._check_http_response_status()

        def exception_raiser():
            raise requests.exceptions.HTTPError

        instance.raise_for_status = exception_raiser
        with pytest.raises(ConnectionRefusedError):
            scraper._check_http_response_status()


def parse_scraper_from_target(
    *args, return_multiple=False
) -> Dict[str, List[str]]:
    """Helper function to parse directly"""
    terms: List[ScraperSearchTerms] = []
    for target in args:
        terms.append(ScraperSearchTerms(target, return_multiple))
    scraper = Scraper("https://www.somewebsite.com", terms)
    scraper._html = HTML_PAGE
    return scraper._parse()


def test_parse_simple():
    target = HtmlSearchTarget(name="Title of document", tag="title")
    result = parse_scraper_from_target(target)
    assert result == {"Title of document": ["The Dormouse's story"]}

    target = HtmlSearchTarget(
        name="Title of document", att_name="class", att_value="title"
    )
    result = parse_scraper_from_target(target)
    assert result == {"Title of document": ["The Dormouse's story"]}

    target = HtmlSearchTarget(
        name="Story", tag="p", att_name="class", att_value="story"
    )
    result = parse_scraper_from_target(target)
    assert "Once upon a time" in result["Story"][0]


def test_parse_multiple():
    target = HtmlSearchTarget(
        name="Sisters", tag="a", att_name="class", att_value="sister"
    )
    result = parse_scraper_from_target(target, return_multiple=True)
    assert result == {"Sisters": ["Elsie", "Lacie", "Tillie"]}

    target = HtmlSearchTarget(
        name="Sisters",
        att_name="class",
        att_value="sister",
        target_element="id",
    )
    result = parse_scraper_from_target(target, return_multiple=True)
    assert result == {"Sisters": ["link1", "link2", "link3"]}

    target_stories = HtmlSearchTarget(
        name="Stories", tag="p", att_name="class", att_value="story"
    )
    target_urls = HtmlSearchTarget(name="URLs", tag="a", target_element="href")
    result = parse_scraper_from_target(
        target_stories, target_urls, return_multiple=True
    )
    assert len(result) > 1
    assert len(result["Stories"]) == 2
    assert "Once upon a time" in result["Stories"][0]
    assert result["Stories"][1] == "..."
    assert len(result["URLs"]) == 3
    assert result["URLs"][0] == "http://example.com/elsie"
    assert result["URLs"][1] == "http://example.com/lacie"
    assert result["URLs"][2] == "http://example.com/tillie"


def test_parse_no_hits():
    target = HtmlSearchTarget(name="Divs", tag="div")
    result = parse_scraper_from_target(target, return_multiple=True)
    assert result == {"Divs": []}

    target = HtmlSearchTarget(
        name="Styles",
        tag="a",
        att_name="class",
        att_value="sister",
        target_element="style",
    )
    result = parse_scraper_from_target(target, return_multiple=True)
    assert result == {"Styles": []}


def test_get():
    scraper = Scraper(
        url="https://www.google.com",
        search_terms=[
            ScraperSearchTerms(
                target=HtmlSearchTarget(
                    name="First link", tag="a", target_element="href"
                )
            )
        ],
    )
    result = scraper.get()
    assert len(result["First link"]) == 1
    assert "https://" in result["First link"][0]


def test_get_with_error():
    scraper = Scraper(
        url="https://www.google.com/not_a_valid_route",
        search_terms=[
            ScraperSearchTerms(
                target=HtmlSearchTarget(
                    name="First link", tag="a", target_element="href"
                )
            )
        ],
    )

    with pytest.raises(FetchingError):
        result = scraper.get()
