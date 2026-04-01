"""This module contains code that is being played around

This file is temporary and only contains code I am trying to understand how
third party libraries behave, or just dumb stuff I am trying, that if it works,
it will be relocated elsewhere.

Don't be surprised if this file disappear later on.

"""

import yaml

def returnYAML(file_path):
    documents = list()
    with open(file_path, 'r') as file:
        data = yaml.safe_load_all(file)
        for doc in data:
            documents.append(doc)
    return documents


path = '../../config/definitions.yaml'
path2 = '/home/'
