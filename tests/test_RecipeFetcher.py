from typing import List
from unittest.mock import patch, PropertyMock
import pytest
import requests
from recipys.RecipeFetcher import RecipeFetcher


def test_RecipeFetcher_construction():
    fetcher = RecipeFetcher()
    assert "http://" in fetcher.url_base
    assert len(fetcher.url_prefix_meal) == 1
    assert len(fetcher.url_prefix_ingredients) == 1
    assert len(fetcher.url_prefix_page) == 1
    assert fetcher.url_page_number == 1
    assert fetcher.whitelist_targets


def test_get_payload():
    fetcher = RecipeFetcher()
    payload = fetcher._get_payload()
    assert payload == {"p": 1}

    fetcher.meal = "breakfast"
    payload = fetcher._get_payload()
    assert payload == {f"{fetcher.url_prefix_meal}": "breakfast", "p": 1}

    fetcher.ingredients = ["eggs"]
    payload = fetcher._get_payload()
    assert payload == {
        f"{fetcher.url_prefix_meal}": "breakfast",
        f"{fetcher.url_prefix_ingredients}": "eggs",
        "p": 1,
    }

    fetcher.meal = "dessert"
    fetcher.ingredients = ["cream", "chocolate"]
    fetcher.url_page_number = 5
    payload = fetcher._get_payload()
    assert payload == {
        f"{fetcher.url_prefix_meal}": "dessert",
        f"{fetcher.url_prefix_ingredients}": "cream,chocolate",
        "p": 5,
    }


def test__recipe_api_get_request():
    # Tested using jsonplaceholder.typicode.com
    fetcher = RecipeFetcher()
    fetcher.url_base = "https://jsonplaceholder.typicode.com/comments"
    fetcher.url_prefix_page = "postId"
    fetcher.url_page_number = 1

    api_response = fetcher._recipe_api_get_request()
    assert len(api_response) > 1
    first_entry = api_response[0]
    assert first_entry.get("postId") == 1
    assert first_entry.get("id") == 1
    assert not first_entry.get("name") == ""
    assert "@" in first_entry.get("email")


def test_check_http_response_status():
    fetcher = RecipeFetcher()

    with patch("requests.models.Request") as patched_Request:
        instance = patched_Request.return_value
        instance.raise_for_status.return_value = "valid"

        # assert no exception
        fetcher._check_http_response_status(instance)

        def exception_raiser():
            raise requests.exceptions.HTTPError

        instance.raise_for_status = exception_raiser
        with pytest.raises(ConnectionRefusedError):
            fetcher._check_http_response_status(instance)


def test_convert_http_response_to_json():
    fetcher = RecipeFetcher()

    with patch("requests.models.Request") as patched_Request:
        instance = patched_Request.return_value
        instance.json.return_value = "valid"

        # assert no exception
        fetcher._convert_http_response_to_json(instance)

        def exception_raiser():
            raise ValueError

        instance.json = exception_raiser
        with pytest.raises(ConnectionRefusedError):
            fetcher._convert_http_response_to_json(instance)
