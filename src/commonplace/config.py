"""This module contains the configuration manager class for Commonplace.
"""
from __future__ import annotations

__author__  = "David Jiménez"
__email__   = "djimenez81@gmail.com"
__status__  = "Initial implementation"
__version__ = "0.1.0"


# Strandard library imports


# Third party imports


# Local imports
import constants
import models
import utils


class TypeConfigurationManager:
    """Manages the configuration of types for Commonplace.

    This class handles system and user define types of fields, notes and
    collections for use inside the system.
    """

    field_type_definitions: dict[str, list[models.FieldTypeDefinition]]
    note_type_definitions: dict[str, list[models.NoteTypeDefinition]]
    collection_type_definitions: dict[str, list[models.CollectionTypeDefinition]]

    def __init__(self):
        """Initializes the Type Configuration Manager.
        """
        self.field_type_definitions = {}
        self.note_type_definitions = {}
        self.collection_type_definitions = {}

    def load_definitions(self, definitions: list[dict]) -> None:
        """Loads the definitions from a list of dictionaries.
        """
        # NOTE: The errors raised need to be improved.

        for definition in definitions:

            if not isinstance(definition, dict):
                raise TypeError(f"Definition has to be passed as a dictionary")

            if len(definition) != 1:
                raise ValueError("Malformed definition.")

            def_key = list(definition.keys())[0]

            if not isinstance(definition[def_key], dict):
                raise ValueError("Malformed definition.")

            if def_key == constants.NEW_FIELD_TYPE:
                self.add_field_def(definition[def_key])
            elif def_key == constants.NEW_NOTE_TYPE:
                self.add_note_def(definition[def_key])
            elif def_key == constants.NEW_COLLECTION_TYPE:
                self.add_collection_def(definition[def_key])
            else:
                raise ValueError("Malformed definition.")


    def add_field_def(self, definition: dict) -> None:
        """Validate and add a field definition.

        Args:
            definition: Dictionary containing field definition data.

        Raises:
            KeyError: If required keys are missing.
        """
        # Required fields
        try:
            field_name = definition[constants.FIELD_NAME]
            field_type = definition[constants.FIELD_TYPE]
        except KeyError as exc:
            raise KeyError(f"Missing required key: {exc.args[0]}") from exc

        # Optional fields.
        required = definition.get(constants.REQUIRED)
        assigned = definition.get(constants.ASSIGNED)
        overwrite = definition.get(constants.OVERWRITE)
        reassign = definition.get(constants.REASSIGN)
        def_origin = definition.get(constants.DEF_ORIGIN)

        # Ensure container exists
        if field_name not in self.field_type_definitions:
            self.field_type_definitions[field_name] = []

        # Create definition object
        new_type_def = models.FieldTypeDefinition(
            field_name=field_name,
            field_type=field_type,
            required=required,
            assigned=assigned,
            overwrite=overwrite,
            reassign=reassign,
            definition_origin=def_origin,
        )

        self.field_type_definitions[field_name].append(new_type_def)

    def add_note_def(self, definition: dict) -> None:
        """Validates and adds a note definition to the list.

        Args:
            definition: Dictionary containing field definition data.

        Raises:
            KeyError: If required keys are missing.
        """
        try:
            note_type = definition.get(constants.NOTE_TYPE)
        except KeyError as exc:
            raise KeyError(f"Missing required key: {exc.args[0]}") from exc

        # Optional fields
        extends = definition.get(constants.EXTENDS)
        metadata_fields = definition.get(constants.META_FIELDS)
        additional_metadata = definition.get(constants.META_FIELDS)
        body_specification = definition.get(constants.BODY_SPEC)

        # Ensure container exists
        if note_type not in self.note_type_definitions:
            self.note_type_definitions[note_type] = []

        # Create definition object
        new_note_def = models.NoteTypeDefinition(
            note_type=note_type,
            extends=extends,
            metadata_fields=metadata_fields,
            additional_metadata=additional_metadata,
            body_specification=body_specification,
        )

        self.note_type_definitions[note_type].append(new_note_def)

    def add_fcollection_def(self, definition: dict) -> None:
        """Validates and adds a collection definition to the list.
        """
        pass



"""
Thinking ahead, for resolution of attributes, I might want to do something like:

def resolve_field_attr(self, field_name: str, attr: str):
    field = self.get_field(field_name)

    value = getattr(field, attr)
    if value is not None:
        return value

    if self.parent:
        return self.parent.resolve_field_attr(field_name, attr)

    return DEFAULTS[attr]
"""
