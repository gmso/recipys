from recipys import ConfigFile


def wait_for_green_light() -> None:
    """
    Checks config file and waits a given timeout before exiting.
    This avoids overloading the server with requests in a short
    period of time (ethical scraping & avoiding blocks)
    """

    MIN_WAIT_SECONDS: float = 10.0

    config_file = ConfigFile()
    