"""Test during development.

This file simply contains snippets of code that I run manually while
developing other parts of the code. Not proper tests, but mini-tests to
ensure that I am understanding myself what I am writing.

Also, it might contain pieces of code to understand standard or third
party libraries that I am using for the first time.

This file might be deleted at the end.
"""

# Testing that loading new definitions works.
import utils
import config

file_path = "../../config/definitions.yaml"
definitions = utils.return_yaml_list(file_path)
con_man = config.TypeConfigurationManager()
con_man.load_definitions(definitions)

# So far seems to be doing what I want it to do.
