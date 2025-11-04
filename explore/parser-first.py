"""
Markdown + YAML Front Matter Parser with Hybrid File/Database Storage

This module demonstrates:
1. Parsing Markdown files with YAML front matter
2. Storing notes in both files (human-readable) and SQLite (fast queries)
3. Keeping the two in sync
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
    file_path: str = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.properties is None:
            self.properties = {}
        if self.links is None:
            self.links = []

class MarkdownParser:
    """Parse Markdown files with YAML front matter"""

    # Regex to split front matter from content
    FRONT_MATTER_REGEX = re.compile(
        r'^---\s*\n(.*?)\n---\s*\n(.*)$',
        re.DOTALL
    )

    @classmethod
    def parse(cls, file_path: str) -> Note:
        """Parse a markdown file and return a Note object"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = cls.FRONT_MATTER_REGEX.match(content)

        if not match:
            # No front matter, treat entire file as content
            return Note(
                id=Path(file_path).stem,
                module="default",
                title=Path(file_path).stem,
                content=content,
                created=datetime.now().isoformat(),
                modified=datetime.now().isoformat(),
                file_path=file_path
            )

        # Parse front matter (YAML) and content (Markdown)
        front_matter_text = match.group(1)
        markdown_content = match.group(2).strip()

        try:
            metadata = yaml.safe_load(front_matter_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {file_path}: {e}")

        # Create Note object
        return Note(
            id=metadata.get('id', Path(file_path).stem),
            module=metadata.get('module', 'default'),
            title=metadata.get('title', 'Untitled'),
            content=markdown_content,
            created=metadata.get('created', datetime.now().isoformat()),
            modified=metadata.get('modified', datetime.now().isoformat()),
            tags=metadata.get('tags', []),
            properties=metadata.get('properties', {}),
            links=metadata.get('links', []),
            file_path=file_path
        )

    @classmethod
    def serialize(cls, note: Note) -> str:
        """Convert a Note object back to Markdown with front matter"""
        # Prepare metadata
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

        # Convert to YAML
        yaml_text = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)

        # Combine front matter and content
        return f"---\n{yaml_text}---\n\n{note.content}"

class NoteDatabase:
    """SQLite database for indexing notes"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self._create_tables()

    def _create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        # Main notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                module TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created TEXT,
                modified TEXT,
                file_path TEXT NOT NULL,
                properties TEXT,  -- JSON
                UNIQUE(file_path)
            )
        """)

        # Tags table (many-to-many)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                note_id TEXT,
                tag TEXT,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                PRIMARY KEY (note_id, tag)
            )
        """)

        # Links table
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

        # Full-text search index
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                id UNINDEXED,
                title,
                content,
                tags
            )
        """)

        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_module ON notes(module)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_modified ON notes(modified)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tag ON tags(tag)")

        self.conn.commit()

    def index_note(self, note: Note):
        """Add or update a note in the database"""
        cursor = self.conn.cursor()

        # Insert or replace main note
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
            note.file_path,
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
            links=links,
            file_path=row['file_path']
        )

    def search(self, query: str, module: str = None) -> List[Note]:
        """Full-text search across notes"""
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
        cursor.execute("SELECT id FROM notes WHERE module = ?", (module,))
        note_ids = [row['id'] for row in cursor.fetchall()]
        return [self.get_note(nid) for nid in note_ids]

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a specific tag"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT note_id FROM tags WHERE tag = ?", (tag,))
        note_ids = [row['note_id'] for row in cursor.fetchall()]
        return [self.get_note(nid) for nid in note_ids]

    def get_linked_notes(self, note_id: str) -> List[tuple]:
        """Get all notes linked from this note"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT target_id, link_type FROM links WHERE source_id = ?
        """, (note_id,))
        return [(row['target_id'], row['link_type']) for row in cursor.fetchall()]

    def get_backlinks(self, note_id: str) -> List[str]:
        """Get all notes that link to this note"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT source_id FROM links WHERE target_id = ?
        """, (note_id,))
        return [row['source_id'] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()

class NoteManager:
    """Manages the hybrid file + database system"""

    def __init__(self, notes_dir: str, db_path: str = None):
        self.notes_dir = Path(notes_dir)
        self.notes_dir.mkdir(parents=True, exist_ok=True)

        if db_path is None:
            db_path = self.notes_dir / ".index" / "notes.db"

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = NoteDatabase(str(db_path))

    def create_note(self, note: Note) -> str:
        """Create a new note (save to file and index in database)"""
        # Determine file path
        module_dir = self.notes_dir / note.module
        module_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from ID
        file_path = module_dir / f"{note.id}.md"
        note.file_path = str(file_path)

        # Update timestamps
        now = datetime.now().isoformat()
        if not note.created:
            note.created = now
        note.modified = now

        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(MarkdownParser.serialize(note))

        # Index in database
        self.db.index_note(note)

        return note.id

    def update_note(self, note: Note):
        """Update an existing note"""
        note.modified = datetime.now().isoformat()

        # Update file
        with open(note.file_path, 'w', encoding='utf-8') as f:
            f.write(MarkdownParser.serialize(note))

        # Update index
        self.db.index_note(note)

    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID (from database)"""
        return self.db.get_note(note_id)

    def delete_note(self, note_id: str):
        """Delete a note (from both file and database)"""
        note = self.db.get_note(note_id)
        if note and note.file_path:
            Path(note.file_path).unlink(missing_ok=True)

        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.db.conn.commit()

    def rebuild_index(self):
        """Rebuild the entire database index from files"""
        print("Rebuilding index from files...")
        count = 0

        for md_file in self.notes_dir.rglob("*.md"):
            if ".index" in md_file.parts:
                continue  # Skip index directory

            try:
                note = MarkdownParser.parse(str(md_file))
                self.db.index_note(note)
                count += 1
                print(f"Indexed: {note.id}")
            except Exception as e:
                print(f"Error indexing {md_file}: {e}")

        print(f"Indexed {count} notes")

    def search(self, query: str, module: str = None) -> List[Note]:
        """Search notes"""
        return self.db.search(query, module)

    def get_notes_by_module(self, module: str) -> List[Note]:
        """Get all notes in a module"""
        return self.db.get_notes_by_module(module)

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a tag"""
        return self.db.get_notes_by_tag(tag)

    def close(self):
        """Close database connection"""
        self.db.close()


# Example usage and testing
if __name__ == "__main__":
    # Initialize the system
    manager = NoteManager("./my_notes")

    # Create a sample note
    note1 = Note(
        id="zk-20241103-001",
        module="zettelkasten",
        title="Epistemology Notes",
        content="""# Epistemology Notes

## Kant's Approach

Kant argued that knowledge requires both **empirical input** and **rational structure**.

The categories of understanding are:
- Quantity
- Quality
- Relation
- Modality

## Mathematical Example

$$\\text{Knowledge} = \\text{Intuition} + \\text{Concepts}$$
""",
        created=datetime.now().isoformat(),
        modified=datetime.now().isoformat(),
        tags=["philosophy", "epistemology", "kant"],
        properties={"certainty": 7, "status": "draft"},
        links=[
            {"target": "zk-20241102-005", "type": "references"},
            {"target": "zk-20241101-012", "type": "related"}
        ]
    )

    # Save the note
    print(f"Creating note: {note1.id}")
    manager.create_note(note1)

    # Create another note
    note2 = Note(
        id="zk-20241103-002",
        module="zettelkasten",
        title="Synthetic A Priori",
        content="""# Synthetic A Priori Judgments

These are judgments that are:
- **Synthetic**: Add new information
- **A Priori**: Known independent of experience

Example: "7 + 5 = 12"
""",
        created=datetime.now().isoformat(),
        modified=datetime.now().isoformat(),
        tags=["philosophy", "kant", "mathematics"],
        properties={"certainty": 9}
    )

    manager.create_note(note2)

    # Search for notes
    print("\n--- Searching for 'kant' ---")
    results = manager.search("kant")
    for note in results:
        print(f"Found: {note.id} - {note.title}")

    # Get notes by tag
    print("\n--- Notes with tag 'philosophy' ---")
    philosophy_notes = manager.get_notes_by_tag("philosophy")
    for note in philosophy_notes:
        print(f"{note.id}: {note.title}")

    # Get notes by module
    print("\n--- All zettelkasten notes ---")
    zk_notes = manager.get_notes_by_module("zettelkasten")
    for note in zk_notes:
        print(f"{note.id}: {note.title} (tags: {', '.join(note.tags)})")

    # Retrieve and modify a note
    print("\n--- Updating note ---")
    note = manager.get_note("zk-20241103-001")
    note.content += "\n\n## New Section\n\nAdded some new thoughts..."
    note.tags.append("updated")
    manager.update_note(note)
    print(f"Updated: {note.id}")

    # Close database
    manager.close()

    print("\n✅ Done! Check the ./my_notes directory for your files.")
    print("   The database index is at ./my_notes/.index/notes.db")
