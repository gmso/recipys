from time import sleep
from recipys.ConfigFile import ConfigFile


def wait_for_green_light() -> None:
    """
    Checks config file and waits a given timeout before exiting.
    This avoids overloading the server with requests in a short
    period of time (ethical scraping & avoiding blocks)
    """

    MIN_SECONDS_REQUEST: float = 10.0

    seconds_passed = ConfigFile().get_delta_last_request()

    if seconds_passed < MIN_SECONDS_REQUEST:
        sleep(seconds_passed)
