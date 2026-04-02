"""This module contains the dataclasses needed for commonplace.

Here you will find an important number of classes that are necessary for the
Commonplace. This are small containers with little to no logic.
"""


__author__  = "David Jiménez"
__email__   = "djimenez81@gmail.com"
__status__  = "Initial implementation"
__version__ = "0.1.0"


# Strandard library imports
from dataclasses import dataclass, field
from typing import Any


# Third party imports


# Local imports
import constants


@dataclass(frozen=True, kw_only=True)
class FieldTypeDefinition:
    """A field type read from initial description.

    The field type definition, when read in an initial description from a YAML
    file that have not yet been initialized inside the system. Some of the
    attributes have default values.

    Attributes:
      - field_name: Name of the Field Type
      - field_type: Type of the data contained in the field.
      - required: Is the field required in the metadata?
      - assigned: Is the field to be assigned by system only or also by user.
      - overwrite: Can the field be overwritten?
      - reassing: Can the field be redefine by extended note or collection?
      - definition_origin: Is the field define individually or reassigned
                           within the definition of a note or a collection?
    """
    field_name: str
    field_type: str
    required: bool | None = None
    assigned: str | None = None
    overwrite: bool | None = None
    reassign: bool | None = None
    definition_origin: str | None = None




@dataclass(frozen=True, kw_only=True)
class NoteTypeDefinition:
    """A note type definition read from initial description.

    The note type definition, when read in an initial description from a YAML
    file that have not yet been initialized inside the system. Some of the
    attributes have default values.

    Attributes:
      - note_type: Name of the note type.
      - extends: Name of the note type that it is extending
      - metadata_fields: list of fields that are allowed.
      - additional_metadata: Is the user allowed to add additional fields?
      - body_specification: Specifies the data and format of the body of the
                            note.
    """
    note_type: str
    extends: str|None = None
    metadata_fields: list[str | dict]
    additional_metadata: bool = True
    body_specification: dict | None = None


@dataclass(frozen=True, kw_only=True)
class CollectionTypeDefinition:
    """A collection type definition read from initial description.

    The collection type definition, when read in an initial description from a
    YAML file that have not yet been initialized inside the system. Some of the
    attributes have default values.

    Attributes:
      - collection_type: Name of the note type.
      - extends: Name of the note type that it is extending
      - metadata_fields: list of fields that are allowed.
      - additional_metadata: Is the user allowed to add additional fields?
      - subcollections_included: List of the subcollections that can be
                                 included.
      - note_types_allowed
    """
    collection_type: str
    extends: str|None = None
    metadata_fields: list[str | dict]
    additional_metadata: bool = True
    subcollections_included: list[str | dict] | None = None
    note_types_allowed: list[str | dict] | None = None


@dataclass(frozen=True, kw_only=True)
class FieldType:
    """A field type in the system.

    Represents a field type that has been already checked and validated within
    the system and it is ready for use.
    """
    pass


@dataclass(frozen=True, kw_only=True)
class NoteType:
    """A note type in the system.

    Represents a note type that has already been checked and validated within
    the system and it is ready for use.
    """
    pass


@dataclass(frozen=True, kw_only=True)
class CollectionType:
    """A collection type in the system.

    ARepresents a collection type that has already been checked and validated
    within the system and it is ready for use.
    """
    pass
