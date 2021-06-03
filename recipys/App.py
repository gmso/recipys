import sys
from recipys.ArgParser import ArgParser


def main(args=None):
    """
    Main entry point of app.

    Args:
        args : list of arguments as from the command line.
    """

    # ToDo: Process user input arguments
    parser = ArgParser(sys.argv)
    command = parser.parse()
    
    # ToDo: Pass arguments to scraper, which returns search results

    # ToDo: Pass search results to printer using rich


if __name__ == "__main__":
    main()