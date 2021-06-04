# import sys
# from recipys.ArgParser import ArgParser
# from recipys.RecipeFetcher import RecipeFetcher
from recipys.request_wait import wait_for_green_light


def main():
    """
    Main entry point of app.
    """

    wait_for_green_light()

    # parser = ArgParser(sys.argv)
    # command = parser.parse()

    # ToDo: Pass arguments to scraper, which returns search results

    # ToDo: Pass search results to printer using rich


if __name__ == "__main__":
    main()
