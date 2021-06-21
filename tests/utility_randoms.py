import random
import string


def random_string() -> str:
    """
    Create random string, combination of letters and symbols

    Returns:
        - str: random string between 1 and 15 digits.
    """

    str_length = random.choice(range(1, 16))
    word = []
    for c in range(str_length):
        word.append(random.choice(string.ascii_letters + string.punctuation))
    return "".join(word)
