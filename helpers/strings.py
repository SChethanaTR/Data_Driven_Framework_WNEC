from random import choice
import string


def random(length: int, uppercase: bool = False) -> str:
    """Generates a random string

    Args:
        length (int): The size of the string
        uppercase (bool, optional): If the string should be all uppercase. Defaults to False.

    Returns:
        str: random string
    """
    letters = string.ascii_uppercase if uppercase else string.ascii_lowercase

    return "".join(choice(letters) for _ in range(length))


def random_digit(length: int) -> str:
    """Generates a random string with digit only

    Args:
        length (int): The size of the string

    Returns:
        str: random string with digit only
    """

    return "".join(choice(string.digits) for _ in range(length))


def id_string(param):
    if isinstance(param, dict):
        return str(param).split("message", maxsplit=1)[0]
    return repr(param)
