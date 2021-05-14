"""
This module implements password generation for employees
"""
import string
import random


def random_password():
    """
    function generate random password
    :return: 8 both number and digit password
    """
    characters = string.ascii_letters + string.digits
    return "".join([random.choice(characters) for i in range(8)])
