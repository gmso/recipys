from unittest.mock import patch
from typing import List

import pytest
import requests

from recipys.Scraper import HtmlSearchTarget, Scraper, ScraperSearchTerms


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


def test_parse():
    target = HtmlSearchTarget("Title of document", "class", "title")
    terms = [ScraperSearchTerms(target)]
    scraper = Scraper("https://www.somewebsite.com", terms)
    scraper._html = HTML_PAGE
    result = scraper._parse()
    assert result == {"Title of document": ["The Dormouse's story"]}

    target = HtmlSearchTarget("Sisters", "class", "sister")
    terms = [ScraperSearchTerms(target, return_multiple=True)]
    scraper = Scraper("https://www.somewebsite.com", terms)
    scraper._html = HTML_PAGE
    result = scraper._parse()
    assert result == {"Sisters": ["Elsie", "Lacie", "Tillie"]}

    target = HtmlSearchTarget(
        "Sisters", "class", "sister", target_element="id"
    )
    terms = [ScraperSearchTerms(target, return_multiple=True)]
    scraper = Scraper("https://www.somewebsite.com", terms)
    scraper._html = HTML_PAGE
    result = scraper._parse()
    assert result == {"Sisters": ["link1", "link2", "link3"]}
