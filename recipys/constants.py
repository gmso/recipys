"""
Global constants of application
"""

# Real time delay between two executions of application (ethical scraping)
MIN_SECONDS_REQUEST: float = 10.0


# Seconds to wait between requests to same endpoint (ethical scraping)
WAIT_BETWEEN_PINGS: int = 1


# Rich colors for printed messages
COLOR_RECIPE_MAIN: str = "steel_blue"
COLOR_RECIPE_SECONDARY: str = "light_slate_grey"
COLOR_ERROR: str = "orange_red1"
COLOR_WARNING: str = "gold1"
COLOR_INFORMATION: str = "deep_sky_blue1"


# Standard messages
MESSAGE_INVALID_ARGS: str = """\
It seems the input arguments are invalid (⌣́_⌣̀)

You can only use [bold]one[/not bold] of the accepted meals :
'breakfast', 'lunch', 'dinner' or 'desert'

Or if you are specifying ingredients, be sure to use the keyword 'with' \
before the ingredients list
(like in 'recipys with potato beans')
"""

MESSAGE_INVALID_INGREDIENT: str = """\
It seems the input arguments are invalid (⌣́_⌣̀)

Please make sure to specify valid ingredients after the 'with' keyword
(valid ingredients have at least one letter, not only symbols)
"""
