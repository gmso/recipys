import time
from unittest.mock import patch
from recipys.ConfigFile import ConfigFile
from recipys.request_wait import wait_for_green_light
from recipys.constants import MIN_SECONDS_REQUEST as min_seconds
from utility_fixtures import config_file_cleanup


def test_wait_below_min_seconds(config_file_cleanup):
    patch_seconds_passed = min_seconds - 0.1

    with patch.object(
        ConfigFile, "get_delta_last_request",
            return_value=patch_seconds_passed):

        timestamp_start = time.time()
        assert timestamp_start > 0

        wait_for_green_light()

        assert (time.time() - timestamp_start) > 0.1


def test_wait_above_min_seconds(config_file_cleanup):
    patch_seconds_passed = min_seconds + 0.1

    with patch.object(
        ConfigFile, "get_delta_last_request",
            return_value=patch_seconds_passed):

        timestamp_start = time.time()
        assert timestamp_start > 0

        wait_for_green_light()

        assert (time.time() - timestamp_start) < 0.1
