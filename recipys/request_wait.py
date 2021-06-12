from time import sleep
from recipys.ConfigFile import ConfigFile
from recipys.constants import MIN_SECONDS_REQUEST as min_seconds


def wait_for_green_light() -> None:
    """
    Checks config file and waits a given timeout before exiting.
    This avoids overloading the server with requests in a short
    period of time (ethical scraping & avoiding blocks)
    """

    seconds_passed = ConfigFile().get_delta_last_request()

    if seconds_passed < min_seconds:
        sleep(min_seconds - seconds_passed)

    ConfigFile().update_time_last_request()
