#!/usr/bin/python
# module core

# This module contains the basic logic for the management of notes and modules
# or note collections.

from typing import Any

@dataclass
class BasicNote:
    # This class contains the most basic unit of this project: the note.
    id: str
    module: str
    created: str
    modified: str
    content: str
    title: str = None
    tags: list[str] = None
    links: list[str] = None
    properties: dict[str, Any] = None
    aliases: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.properties is None:
            self.properties = {}
        if self.links is None:
            self.links = []
        if aliases is None:
            self.aliases = []


class NoteCollection:
    # This class contains the structure and logic for collections of notes.
    pass

class NoteModule:
    # This class contains the structure and logic for note modules. A note
    # module may contain more than one note collection

    def __init__(self):
        pass

    def create_note(self, note: BasicNote):
        pass

    def update_note(self, note: BasicNote):
        pass

    def get_note(self, note_id: str):
        # Get a specific note on this module by its id.
        pass

    def delete_note(self, note_id: str):
        pass

    def rebuild_index(self):
        # Rebuild the entire database indes from files
        pass

    def search(self, query: str):
        # Searches all the notes in this module.
        pass
