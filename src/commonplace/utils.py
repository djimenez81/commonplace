"""This module contains some aditional utilities for the project commonplace.

We will see what we need to include in this module as we develop the package.
"""


__author__  = "David Jiménez"
__email__   = "djimenez81@gmail.com"
__status__  = "Initial implementation"
__version__ = "0.1.0"


# Strandard library imports


# Third party imports
import yaml

# Local imports




def return_yaml_list(file_path):
    yaml_list = list()
    with open(file_path, 'r') as file:
        data = yaml.safe_load_all(file)
        for doc in data:
            yaml_list.append(doc)
    return yaml_list
