# Collected, not in modules

## Suggestion for folder structure

```
pynotes/
├── pynotes/                    # Main package directory
│   ├── __init__.py
│   ├── main.py                 # Entry point (the app code)
│   ├── ui/                     # UI components
│   │   ├── __init__.py
│   │   ├── editor.py           # MarkdownEditor class
│   │   ├── preview.py          # MarkdownPreview class
│   │   ├── file_tree.py        # FileTree class
│   │   └── main_window.py      # NotesApp main window
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── plugin_manager.py   # Plugin system
│   │   ├── file_manager.py     # File operations
│   │   └── search.py           # Search functionality (future)
│   ├── plugins/                # Built-in and user plugins
│   │   ├── __init__.py
│   │   └── example_plugin.py
│   ├── resources/              # Icons, styles, etc.
│   │   ├── icons/
│   │   └── styles/
│   │       └── default.qss     # Qt stylesheet
│   └── utils/                  # Helper functions
│       ├── __init__.py
│       └── markdown_utils.py
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_core.py
├── docs/                       # Documentation
│   └── plugin_guide.md
├── requirements.txt            # Dependencies
├── setup.py                    # Installation script
├── README.md
└── .gitignore
```

### Minimal Start (if the above feels like overkill):
```
pynotes/
├── main.py                     # Your app (the code I gave you)
├── plugins/                    # Plugin folder
│   └── __init__.py
├── requirements.txt
└── README.md
```

### Key Benefits:

1. **Separation of concerns**: UI, core logic, and plugins are separate
2. **Easy imports**: `from pynotes.core import PluginManager`
3. **Plugin discoverability**: Plugins live in a known location
4. **Scalability**: Easy to add new modules without cluttering
5. **Testing**: Clear place for tests separate from code

### The `requirements.txt` should contain:
```
PySide6>=6.6.0
markdown>=3.5.0
```


## Suggestion for data bases

```
notes.db
├── notes table (id, content, metadata, module_id, created, modified)
├── modules table (id, name, type, config)
├── links table (source_note_id, target_note_id, link_type)
├── tags table (note_id, tag)
└── properties table (note_id, key, value)
```


## YAML configuration file example

```yaml
# modules/task-manager.yaml
module:
  name: "Task Manager"
  type: "task-system"
  storage: "notes.db"  # or separate task.db

views:
  - name: "Today"
    query: "tasks WHERE due_date = today()"
    template: "daily_tasks_view"

  - name: "Master List"
    query: "tasks ORDER BY priority"
    template: "task_list_view"

properties:
  - name: "due_date"
    type: "date"
  - name: "priority"
    type: "integer"
  - name: "status"
    type: "enum"
    values: ["todo", "in-progress", "done"]

links_to:
  - "zettelkasten"
  - "projects"
```


## Suggestion of properties for dtabase schema

```python
# Flexible schema to support different module types
class Note:
    id: int
    module_id: int
    title: str
    content: str  # Markdown content
    properties: dict  # JSON field for flexible metadata
    created: datetime
    modified: datetime

class Module:
    id: int
    name: str
    type: str  # 'tasks', 'zettelkasten', 'writing', 'teaching', etc.
    config: dict  # Module-specific configuration

class Link:
    source_note_id: int
    target_note_id: int
    link_type: str  # 'reference', 'related', 'parent', etc.
```


## Suggested tech stack

```python
# Core
PySide6              # UI framework
SQLite3              # Database (built into Python)
SQLAlchemy          # ORM for database operations

# Text processing
markdown            # Markdown rendering
pymdown-extensions  # Extended markdown features
PyYAML              # Module configuration

# LaTeX
subprocess          # Call pdflatex
Pygments           # Syntax highlighting

# Code execution
jupyter-client     # For code execution
IPython            # Interactive Python

# Export
pandoc             # Universal document converter (call as subprocess)
```


## Suggested modular architecture pattern

```python
# Base module class
class Module:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.db = Database()  # Shared database connection

    def get_views(self) -> List[View]:
        """Return views defined in module config"""
        pass

    def get_schema(self) -> dict:
        """Return properties schema for this module"""
        pass

    def query(self, query_string: str) -> List[Note]:
        """Execute module-specific query"""
        pass

# Example: Task module
class TaskModule(Module):
    def get_today_tasks(self):
        return self.query("status != 'done' AND due_date <= today()")

    def create_daily_note(self):
        """Generate daily note with task aggregation"""
        pass
```

### 7. **File Structure for This Approach**

```
pynotes/
├── pynotes/
│   ├── core/
│   │   ├── database.py          # SQLite operations
│   │   ├── module_manager.py    # Load/manage modules
│   │   ├── note.py              # Note model
│   │   ├── link_graph.py        # Track relationships
│   │   └── search_engine.py     # Full-text search
│   ├── modules/
│   │   ├── base_module.py       # Base Module class
│   │   ├── task_module.py       # Task-specific logic
│   │   ├── zettelkasten_module.py
│   │   ├── writing_module.py
│   │   └── teaching_module.py
│   ├── ui/
│   │   ├── module_view.py       # Generic module display
│   │   ├── editor.py            # Enhanced editor
│   │   ├── latex_editor.py      # LaTeX editing pane
│   │   ├── code_runner.py       # Code execution widget
│   │   └── graph_view.py        # Visualize links
│   └── exporters/
│       ├── markdown_exporter.py
│       └── latex_exporter.py
├── modules/                      # User module definitions
│   ├── tasks.yaml
│   ├── zettelkasten.yaml
│   └── writing.yaml
├── data/
│   └── notes.db                 # Your data
└── templates/                    # View templates
    └── daily_tasks.html
```

## YAML-Driven Configuration

```yaml
# custom_modules/research_papers.yaml
module:
  name: "Research Papers"
  type: "database"
  icon: "📄"

properties:
  - name: "authors"
    type: "text"
    required: true
  - name: "year"
    type: "integer"
  - name: "journal"
    type: "text"
  - name: "doi"
    type: "text"
  - name: "read_status"
    type: "enum"
    values: ["to-read", "reading", "completed"]
  - name: "rating"
    type: "integer"
    min: 1
    max: 5

views:
  - name: "By Author"
    group_by: "authors"
  - name: "To Read"
    filter: "read_status = 'to-read'"
    sort: "year DESC"

templates:
  note: |
    # {title}
    **Authors:** {authors}
    **Year:** {year}
    **Journal:** {journal}

    ## Summary

    ## Key Points

    ## Related
```


## About some formats


Welcome back! Great question - the choice of storage format is really important for a knowledge management system. Let me break down each option:

## JSON (JavaScript Object Notation)

**What it looks like:**
```json
{
  "id": "20241103-001",
  "title": "My First Note",
  "module": "zettelkasten",
  "created": "2024-11-03T10:30:00",
  "tags": ["philosophy", "epistemology"],
  "properties": {
    "status": "draft",
    "certainty": 8
  },
  "content": "# My First Note\n\nThis is the content...",
  "links": [
    {"to": "20241102-005", "type": "references"},
    {"to": "20241101-012", "type": "related"}
  ]
}
```

**Advantages:**
- ✅ **Ubiquitous**: Every language has excellent JSON support
- ✅ **Fast parsing**: Very efficient
- ✅ **Structured**: Clear hierarchy
- ✅ **Git-friendly**: Diffs work reasonably well
- ✅ **Validation**: JSON Schema exists for validation

**Disadvantages:**
- ❌ **Not very human-readable** for large content blocks
- ❌ **No comments**: Can't annotate the structure
- ❌ **Verbose**: Lots of quotes and braces
- ❌ **Multiline strings**: Awkward with `\n` escapes

**Best for:** Configuration files, structured data exports, API interchange

## YAML (YAML Ain't Markup Language)

**What it looks like:**
```yaml
id: 20241103-001
title: My First Note
module: zettelkasten
created: 2024-11-03T10:30:00
tags:
  - philosophy
  - epistemology
properties:
  status: draft
  certainty: 8
content: |
  # My First Note

  This is the content with proper
  multiline support and no escaping.

links:
  - to: 20241102-005
    type: references
  - to: 20241101-012
    type: related
```

**Advantages:**
- ✅ **Very human-readable**: Clean, minimal syntax
- ✅ **Multiline strings**: Natural with `|` or `>` operators
- ✅ **Comments**: Can add `# comments` anywhere
- ✅ **Less verbose**: No quotes needed for most strings
- ✅ **Anchors & references**: Can avoid duplication with `&` and `*`

**Disadvantages:**
- ❌ **Indentation-sensitive**: Whitespace matters (like Python)
- ❌ **Parsing complexity**: More complex than JSON
- ❌ **Security concerns**: Can execute code if not careful (use safe loaders!)
- ❌ **Ambiguity**: `no` vs `"no"`, dates, etc. can be confusing

**Best for:** Configuration files, module definitions, human-edited metadata

## XML (eXtensible Markup Language)

**What it looks like:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<note>
  <id>20241103-001</id>
  <title>My First Note</title>
  <module>zettelkasten</module>
  <created>2024-11-03T10:30:00</created>
  <tags>
    <tag>philosophy</tag>
    <tag>epistemology</tag>
  </tags>
  <properties>
    <property name="status">draft</property>
    <property name="certainty">8</property>
  </properties>
  <content><![CDATA[
# My First Note

This is the content...
  ]]></content>
  <links>
    <link to="20241102-005" type="references"/>
    <link to="20241101-012" type="related"/>
  </links>
</note>
```

**Advantages:**
- ✅ **Industry standard**: Used in many enterprise systems
- ✅ **Rich tooling**: XPath, XSLT, XML Schema
- ✅ **Mixed content**: Can intermix text and structure easily
- ✅ **Namespaces**: Prevent naming conflicts
- ✅ **Validation**: XSD schemas are powerful

**Disadvantages:**
- ❌ **Very verbose**: Lots of opening/closing tags
- ❌ **Hard to read**: Visual noise
- ❌ **Overkill**: Usually too heavy for simple use cases
- ❌ **Large file sizes**: More bytes than other formats

**Best for:** Enterprise integrations, complex documents with mixed content, when you need advanced validation


## Summary Table

| Format | Readability | Parsing Speed | Standard Support | Best Use Case |
|--------|-------------|---------------|------------------|---------------|
| **Markdown + YAML** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Notes/content** |
| JSON | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Structured data |
| YAML | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Config files |
| XML | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Enterprise |


## Watchdog example

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class NoteFileHandler(FileSystemEventHandler):
    """Handle file system events for note files"""

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            print(f"Note modified: {event.src_path}")
            # Here you would re-index the note
            # manager.reindex_note(event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"New note created: {event.src_path}")
            # manager.index_new_note(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"Note deleted: {event.src_path}")
            # manager.remove_from_index(event.src_path)

# Set up the observer
observer = Observer()
event_handler = NoteFileHandler()
observer.schedule(event_handler, path="./my_notes", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

## Example in this app context

```python
class NoteManager:
    def __init__(self, notes_dir: str, db_path: str = None):
        self.notes_dir = Path(notes_dir)
        self.db = NoteDatabase(db_path)

        # Set up file watcher
        self.observer = Observer()
        self.event_handler = NoteWatchHandler(self)
        self.observer.schedule(
            self.event_handler,
            path=str(self.notes_dir),
            recursive=True
        )
        self.observer.start()

    def on_file_changed(self, file_path: str):
        """Called by watchdog when a file changes"""
        note = MarkdownParser.parse(file_path)
        self.db.index_note(note)
        print(f"Auto-indexed: {note.id}")
```
