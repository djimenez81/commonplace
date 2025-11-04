"""
Option A: Multiple Notes Per File (Grouped by Month and Module)

This implementation stores multiple notes in single files, grouped by:
- Module (zettelkasten, tasks, writing, etc.)
- Time period (monthly)

Example structure:
    my_notes/
    ├── zettelkasten/
    │   ├── 2024-11.md
    │   └── 2024-10.md
    ├── tasks/
    │   └── 2024-11.md
    └── .index/
        └── notes.db
"""

import os
import re
import yaml
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Note delimiter for separating multiple notes in one file
NOTE_START_DELIMITER = "<!-- NOTE_START: {id} -->"
NOTE_END_DELIMITER = "<!-- NOTE_END: {id} -->"

@dataclass
class Note:
    """Represents a note with metadata and content"""
    id: str
    module: str
    title: str
    content: str
    created: str
    modified: str
    tags: List[str] = None
    properties: Dict[str, Any] = None
    links: List[Dict[str, str]] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.properties is None:
            self.properties = {}
        if self.links is None:
            self.links = []

class GroupedFileParser:
    """Parse files containing multiple notes"""

    @classmethod
    def parse_file(cls, file_path: str) -> List[Note]:
        """Parse a file and return all notes in it"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        notes = []

        # Find all note sections
        # Pattern: <!-- NOTE_START: id --> ... <!-- NOTE_END: id -->
        pattern = r'<!-- NOTE_START: (.+?) -->\s*\n---\s*\n(.*?)\n---\s*\n(.*?)\n<!-- NOTE_END: \1 -->'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            note_id = match.group(1)
            front_matter = match.group(2)
            note_content = match.group(3).strip()

            try:
                metadata = yaml.safe_load(front_matter)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML for note {note_id}: {e}")
                continue

            note = Note(
                id=metadata.get('id', note_id),
                module=metadata.get('module', 'default'),
                title=metadata.get('title', 'Untitled'),
                content=note_content,
                created=metadata.get('created', datetime.now().isoformat()),
                modified=metadata.get('modified', datetime.now().isoformat()),
                tags=metadata.get('tags', []),
                properties=metadata.get('properties', {}),
                links=metadata.get('links', [])
            )
            notes.append(note)

        return notes

    @classmethod
    def serialize_notes(cls, notes: List[Note]) -> str:
        """Convert multiple notes into a single file content"""
        file_content_parts = []

        # Add file header
        file_content_parts.append(f"# Notes File")
        file_content_parts.append(f"# Generated: {datetime.now().isoformat()}")
        file_content_parts.append(f"# Contains {len(notes)} notes\n")

        for note in notes:
            # Start delimiter
            file_content_parts.append(NOTE_START_DELIMITER.format(id=note.id))

            # Front matter
            metadata = {
                'id': note.id,
                'module': note.module,
                'title': note.title,
                'created': note.created,
                'modified': note.modified,
            }

            if note.tags:
                metadata['tags'] = note.tags
            if note.properties:
                metadata['properties'] = note.properties
            if note.links:
                metadata['links'] = note.links

            yaml_text = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
            file_content_parts.append("---")
            file_content_parts.append(yaml_text.rstrip())
            file_content_parts.append("---")

            # Content
            file_content_parts.append(note.content)

            # End delimiter
            file_content_parts.append(NOTE_END_DELIMITER.format(id=note.id))
            file_content_parts.append("")  # Empty line between notes

        return "\n".join(file_content_parts)

    @classmethod
    def update_note_in_file(cls, file_path: str, updated_note: Note) -> bool:
        """Update a specific note within a file"""
        notes = cls.parse_file(file_path)

        # Find and replace the note
        found = False
        for i, note in enumerate(notes):
            if note.id == updated_note.id:
                notes[i] = updated_note
                found = True
                break

        if not found:
            # Note not in this file, add it
            notes.append(updated_note)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cls.serialize_notes(notes))

        return True

    @classmethod
    def delete_note_from_file(cls, file_path: str, note_id: str) -> bool:
        """Remove a specific note from a file"""
        notes = cls.parse_file(file_path)
        notes = [n for n in notes if n.id != note_id]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cls.serialize_notes(notes))

        return True

class NoteDatabase:
    """SQLite database for indexing notes (same as before)"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        # Main notes table - now includes file_path to track which file contains the note
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                module TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created TEXT,
                modified TEXT,
                file_path TEXT NOT NULL,
                properties TEXT,
                UNIQUE(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                note_id TEXT,
                tag TEXT,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                PRIMARY KEY (note_id, tag)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                source_id TEXT,
                target_id TEXT,
                link_type TEXT,
                context TEXT,
                FOREIGN KEY (source_id) REFERENCES notes(id) ON DELETE CASCADE,
                PRIMARY KEY (source_id, target_id, link_type)
            )
        """)

        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                id UNINDEXED,
                title,
                content,
                tags
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_module ON notes(module)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_modified ON notes(modified)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_path ON notes(file_path)")

        self.conn.commit()

    def index_note(self, note: Note, file_path: str):
        """Add or update a note in the database"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO notes
            (id, module, title, content, created, modified, file_path, properties)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            note.id,
            note.module,
            note.title,
            note.content,
            note.created,
            note.modified,
            file_path,
            json.dumps(note.properties)
        ))

        # Delete old tags and links
        cursor.execute("DELETE FROM tags WHERE note_id = ?", (note.id,))
        cursor.execute("DELETE FROM links WHERE source_id = ?", (note.id,))

        # Insert tags
        for tag in note.tags:
            cursor.execute(
                "INSERT INTO tags (note_id, tag) VALUES (?, ?)",
                (note.id, tag)
            )

        # Insert links
        for link in note.links:
            cursor.execute("""
                INSERT INTO links (source_id, target_id, link_type, context)
                VALUES (?, ?, ?, ?)
            """, (
                note.id,
                link.get('target'),
                link.get('type', 'reference'),
                link.get('context', '')
            ))

        # Update FTS index
        cursor.execute("DELETE FROM notes_fts WHERE id = ?", (note.id,))
        cursor.execute("""
            INSERT INTO notes_fts (id, title, content, tags)
            VALUES (?, ?, ?, ?)
        """, (
            note.id,
            note.title,
            note.content,
            ' '.join(note.tags)
        ))

        self.conn.commit()

    def get_note(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()

        if not row:
            return None

        # Get tags
        cursor.execute("SELECT tag FROM tags WHERE note_id = ?", (note_id,))
        tags = [r['tag'] for r in cursor.fetchall()]

        # Get links
        cursor.execute("""
            SELECT target_id, link_type, context
            FROM links WHERE source_id = ?
        """, (note_id,))
        links = [
            {'target': r['target_id'], 'type': r['link_type'], 'context': r['context']}
            for r in cursor.fetchall()
        ]

        return Note(
            id=row['id'],
            module=row['module'],
            title=row['title'],
            content=row['content'],
            created=row['created'],
            modified=row['modified'],
            tags=tags,
            properties=json.loads(row['properties']),
            links=links
        )

    def get_file_path(self, note_id: str) -> Optional[str]:
        """Get the file path where a note is stored"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT file_path FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        return row['file_path'] if row else None

    def search(self, query: str, module: str = None) -> List[Note]:
        """Full-text search"""
        cursor = self.conn.cursor()

        if module:
            cursor.execute("""
                SELECT n.id FROM notes n
                JOIN notes_fts fts ON n.id = fts.id
                WHERE fts MATCH ? AND n.module = ?
                ORDER BY rank
            """, (query, module))
        else:
            cursor.execute("""
                SELECT n.id FROM notes_fts fts
                JOIN notes n ON fts.id = n.id
                WHERE fts MATCH ?
                ORDER BY rank
            """, (query,))

        note_ids = [row['id'] for row in cursor.fetchall()]
        return [self.get_note(nid) for nid in note_ids]

    def get_notes_by_module(self, module: str) -> List[Note]:
        """Get all notes in a module"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM notes WHERE module = ? ORDER BY modified DESC", (module,))
        note_ids = [row['id'] for row in cursor.fetchall()]
        return [self.get_note(nid) for nid in note_ids]

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a tag"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT note_id FROM tags WHERE tag = ?", (tag,))
        note_ids = [row['note_id'] for row in cursor.fetchall()]
        return [self.get_note(nid) for nid in note_ids]

    def delete_note(self, note_id: str):
        """Delete a note from the index"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

class GroupedNoteManager:
    """Manages notes stored in grouped files"""

    def __init__(self, notes_dir: str, db_path: str = None):
        self.notes_dir = Path(notes_dir)
        self.notes_dir.mkdir(parents=True, exist_ok=True)

        if db_path is None:
            db_path = self.notes_dir / ".index" / "notes.db"

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = NoteDatabase(str(db_path))

    def _get_file_path(self, note: Note) -> Path:
        """Determine which file a note should be stored in"""
        # Group by module and month
        created_date = datetime.fromisoformat(note.created)
        year_month = created_date.strftime("%Y-%m")

        module_dir = self.notes_dir / note.module
        module_dir.mkdir(parents=True, exist_ok=True)

        return module_dir / f"{year_month}.md"

    def create_note(self, note: Note) -> str:
        """Create a new note"""
        # Set timestamps
        now = datetime.now().isoformat()
        if not note.created:
            note.created = now
        note.modified = now

        # Determine file path
        file_path = self._get_file_path(note)

        # Load existing notes from file
        if file_path.exists():
            notes = GroupedFileParser.parse_file(str(file_path))
        else:
            notes = []

        # Add new note
        notes.append(note)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(GroupedFileParser.serialize_notes(notes))

        # Index in database
        self.db.index_note(note, str(file_path))

        return note.id

    def update_note(self, note: Note):
        """Update an existing note"""
        note.modified = datetime.now().isoformat()

        # Get current file path from database
        file_path = self.db.get_file_path(note.id)

        if not file_path:
            # Note doesn't exist, create it
            self.create_note(note)
            return

        # Update in file
        GroupedFileParser.update_note_in_file(file_path, note)

        # Update index
        self.db.index_note(note, file_path)

    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID"""
        return self.db.get_note(note_id)

    def delete_note(self, note_id: str):
        """Delete a note"""
        # Get file path
        file_path = self.db.get_file_path(note_id)

        if file_path:
            # Remove from file
            GroupedFileParser.delete_note_from_file(file_path, note_id)

        # Remove from database
        self.db.delete_note(note_id)

    def rebuild_index(self):
        """Rebuild the entire database index from files"""
        print("Rebuilding index from grouped files...")
        count = 0

        for md_file in self.notes_dir.rglob("*.md"):
            if ".index" in md_file.parts:
                continue

            try:
                notes = GroupedFileParser.parse_file(str(md_file))
                for note in notes:
                    self.db.index_note(note, str(md_file))
                    count += 1
                    print(f"Indexed: {note.id}")
            except Exception as e:
                print(f"Error indexing {md_file}: {e}")

        print(f"Indexed {count} notes from grouped files")

    def search(self, query: str, module: str = None) -> List[Note]:
        """Search notes"""
        return self.db.search(query, module)

    def get_notes_by_module(self, module: str) -> List[Note]:
        """Get all notes in a module"""
        return self.db.get_notes_by_module(module)

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a tag"""
        return self.db.get_notes_by_tag(tag)

    def export_module_to_individual_files(self, module: str, output_dir: str):
        """Export a module's notes to individual files (for backup/portability)"""
        output_path = Path(output_dir) / module
        output_path.mkdir(parents=True, exist_ok=True)

        notes = self.get_notes_by_module(module)

        for note in notes:
            # Create individual file
            file_path = output_path / f"{note.id}.md"

            # Front matter
            metadata = {
                'id': note.id,
                'module': note.module,
                'title': note.title,
                'created': note.created,
                'modified': note.modified,
                'tags': note.tags,
                'properties': note.properties,
                'links': note.links
            }

            yaml_text = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"---\n{yaml_text}---\n\n{note.content}")

        print(f"Exported {len(notes)} notes from '{module}' to {output_path}")

    def close(self):
        """Close database connection"""
        self.db.close()


# Example usage
if __name__ == "__main__":
    # Initialize
    manager = GroupedNoteManager("./my_notes_grouped")

    # Create several notes
    print("Creating notes...")

    note1 = Note(
        id="zk-20241103-001",
        module="zettelkasten",
        title="Epistemology Notes",
        content="""# Epistemology Notes

## Kant's Approach

Kant argued that knowledge requires both empirical input and rational structure.
""",
        created="2024-11-03T10:30:00",
        modified="2024-11-03T10:30:00",
        tags=["philosophy", "epistemology", "kant"],
        properties={"certainty": 7}
    )

    note2 = Note(
        id="zk-20241103-002",
        module="zettelkasten",
        title="Synthetic A Priori",
        content="""# Synthetic A Priori

These judgments are both synthetic (adding new info) and a priori (known independently).
""",
        created="2024-11-03T11:00:00",
        modified="2024-11-03T11:00:00",
        tags=["philosophy", "kant", "mathematics"],
        properties={"certainty": 9}
    )

    note3 = Note(
        id="task-20241103-001",
        module="tasks",
        title="Buy groceries",
        content="""- Milk
- Eggs
- Bread
""",
        created="2024-11-03T09:00:00",
        modified="2024-11-03T09:00:00",
        tags=["shopping", "urgent"],
        properties={"due": "2024-11-05", "priority": "high"}
    )

    # Create notes
    manager.create_note(note1)
    manager.create_note(note2)
    manager.create_note(note3)

    print(f"\n✅ Created 3 notes")
    print(f"   Check: ./my_notes_grouped/zettelkasten/2024-11.md")
    print(f"   Check: ./my_notes_grouped/tasks/2024-11.md")

    # Search
    print("\n--- Searching for 'kant' ---")
    results = manager.search("kant")
    for note in results:
        print(f"  {note.id}: {note.title}")

    # Get by module
    print("\n--- All zettelkasten notes ---")
    zk_notes = manager.get_notes_by_module("zettelkasten")
    for note in zk_notes:
        print(f"  {note.id}: {note.title}")

    # Update a note
    print("\n--- Updating a note ---")
    note = manager.get_note("zk-20241103-001")
    note.content += "\n\n## Additional Thoughts\n\nAdded more content..."
    manager.update_note(note)
    print(f"  Updated: {note.id}")

    # Export to individual files (for backup)
    print("\n--- Exporting to individual files ---")
    manager.export_module_to_individual_files("zettelkasten", "./exports")

    manager.close()

    print("\n✅ Done!")
    print("   Grouped files: ./my_notes_grouped/")
    print("   Individual file exports: ./exports/")
