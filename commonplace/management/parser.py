#!/usr/bin/python
# module parser

# This module contains the basic logic for the management of notes and modules
# or note collections.


# Own imports
from ..core.core import BasicNote, NoteCollection, NoteModule

# Standard imports
from dataclasses import dataclass


# @dataclass
class Parser:
    # This class contains the logic to read from drive or save to it a
    # collection of notes.

    @classmethod
    def parse(cls, file_path: str, mode: str):
        # This is the function that reads a file and parse it. As there are
        # different types of files and it can be either parsed to a note, a
        # collection or a module, this is going to be fun.
        #
        # The "file" might be a database, an xml, a YAML+MD collection or a
        # YAML+MD single note, YAML+LaTeX or YAML+Code.
        pass

    @classmethod
    def serialize(cls, note: BasicNote) -> str:
        # This function takes a note and serialize it into a string
        pass

    @classmethod
    def save_note(cls, note: BasicNote):
        pass

    @classmethod
    def save_collection(cls, collection: NoteCollection):
        pass

    @classmethod
    def save_module(cls, module: NoteModule):
        pass




class NoteDatabase:
    # This contains the SQLite logic for indexing

    def __init__(self,db_path: str):
        # Initializator of the instance.
        pass

    def _create_tables(self):
        # Create Database Schema.
        pass

    def index_note(self, note: BasicNote):
        # Add or update note in the database
        pass

    def get_note(self,note_id: str):
        # Retrieves a note by ID.
        pass

    def search(self,query: str, module: str = None):
        # Full-text search across notes
        pass

    def get_notes_by_module(self, module: str):
        pass

    def get_notes_by_tag(self, tag:str):
        pass

    def get_linked_notes(self, note_id: str):
        pass

    def get_backlinks(self, note_id: str):
        pass
