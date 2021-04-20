import string
import random


def random_password():
    characters = string.ascii_letters + string.digits
    return "".join([random.choice(characters) for i in range(12)])
