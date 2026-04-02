"""This module contains some aditional utilities for the project commonplace.

We will see what we need to include in this module as we develop the package.
"""


__author__  = "David Jiménez"
__email__   = "djimenez81@gmail.com"
__status__  = "Initial implementation"
__version__ = "0.1.0"


# Strandard library imports
import uuid


# Third party imports
import yaml

# Local imports




def return_yaml_list(file_path: str) -> list[dict]:
    """Returns a list of YAML documents (dictinaries) contained in a file.

    Attributes:
      - file_path: The path of the YAML file.

    Returns:
      - list of dictionaries
    """
    yaml_list = list()
    with open(file_path, 'r') as file:
        data = yaml.safe_load_all(file)
        for doc in data:
            yaml_list.append(doc)
    return yaml_list



def is_valid_uuid(possible_uuid: str) -> bool:
    """Checks if a given string is a UUID or not.

    Attributes:
      - val: String that could be.

    Returns:
      - True if string is a valid UUID, false otherwise.
    """
    try:
        # Attempts to parse the string as a UUID
        uuid.UUID(str(possible_uuid))
        return True
    except ValueError:
        # Raised if the string is not a valid 32-character hex string
        return False
