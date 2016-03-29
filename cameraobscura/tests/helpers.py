
# python standard library
import random
import string


def random_string_of_letters(maximum=100, minimum=1):
    """
    Returns a random string of letters of a random size (uses string.letters as the source)

    :param:

     - `maximum`: maximum string length
     - `minimum`: shortest string length (added later so comes after maximum to remain compatible)
    """
    characters = xrange(random.randrange(minimum, maximum))
    return "".join((random.choice(string.letters) for character in characters))
