#!/usr/bin/python
# module basic_utils.py

# This module contains some basic functionality.

# IMPORTS
from random import randint


# CONSTANTS

ID_LEN = 4 # This is too small for production, but it is a good for testing.
ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C',
            'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'Q',
            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ALP_LEN = len(ALPHABET)



# FUNCTIONS
def _generate_id(prefix: str) -> str:
    id_string = prefix
    id_string += '-'
    for _ in range(ID_LEN):
        id_string += ALPHABET[randint(0,ALP_LEN-1)]
    return id_string
