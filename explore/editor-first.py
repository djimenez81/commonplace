"""
Simple Note-Taking App with PySide6
Demonstrates: file browser, markdown editing, LaTeX/MathJax rendering, plugin architecture
"""

from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter,
                               QTreeWidget, QTreeWidgetItem, QTextEdit,
                               QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
                               QFileDialog, QMessageBox)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QDir
import sys
import os
import markdown

class PluginManager:
    """Simple plugin system - plugins are Python modules with a 'register' function"""
    def __init__(self):
        self.plugins = []

    def load_plugin(self, plugin_path):
        """Load a plugin from a Python file"""
        # In a real app, use importlib to dynamically load modules
        pass

    def register_plugin(self, plugin):
        """Register a plugin object"""
        self.plugins.append(plugin)
        return True

class MarkdownEditor(QTextEdit):
    """Enhanced text editor for markdown"""
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Start writing your note here...\n\n"
                               "You can use Markdown syntax.\n"
                               "For math, use: $inline$ or $$block$$")
        # Set a monospace font for better markdown editing
        font = self.font()
        font.setFamily("Courier New")
        font.setPointSize(11)
        self.setFont(font)

class MarkdownPreview(QWebEngineView):
    """Web view to render markdown with MathJax support"""
    def __init__(self):
        super().__init__()
        self.html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']]
            }}
        }};
    </script>
</head>
<body>
{content}
</body>
</html>
"""

    def update_content(self, markdown_text):
        """Convert markdown to HTML and render with MathJax"""
        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables'])
        # Insert into template
        full_html = self.html_template.format(content=html_content)
        self.setHtml(full_html)

class FileTree(QTreeWidget):
    """File browser for notes"""
    def __init__(self, root_path=None):
        super().__init__()
        self.setHeaderLabel("Notes")
        self.root_path = root_path or os.path.expanduser("~/Documents/Notes")

        # Create notes directory if it doesn't exist
        os.makedirs(self.root_path, exist_ok=True)

        self.populate_tree()

    def populate_tree(self):
        """Populate tree with files from notes directory"""
        self.clear()
        root_item = QTreeWidgetItem(self, [os.path.basename(self.root_path)])
        self.add_directory_items(root_item, self.root_path)
        self.expandAll()

    def add_directory_items(self, parent_item, path):
        """Recursively add items to tree"""
        try:
            for item_name in sorted(os.listdir(path)):
                item_path = os.path.join(path, item_name)
                child_item = QTreeWidgetItem(parent_item, [item_name])
                child_item.setData(0, Qt.UserRole, item_path)

                if os.path.isdir(item_path):
                    self.add_directory_items(child_item, item_path)
        except PermissionError:
            pass

class NotesApp(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyNotes - Lightweight Note-Taking")
        self.setGeometry(100, 100, 1200, 800)

        self.current_file = None
        self.plugin_manager = PluginManager()

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Toolbar
        toolbar = QHBoxLayout()

        new_btn = QPushButton("New Note")
        new_btn.clicked.connect(self.new_note)
        toolbar.addWidget(new_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_note)
        toolbar.addWidget(save_btn)

        open_btn = QPushButton("Open Folder")
        open_btn.clicked.connect(self.open_folder)
        toolbar.addWidget(open_btn)

        toolbar.addStretch()

        toggle_preview_btn = QPushButton("Toggle Preview")
        toggle_preview_btn.clicked.connect(self.toggle_preview)
        toolbar.addWidget(toggle_preview_btn)

        main_layout.addLayout(toolbar)

        # Main splitter (3 panes)
        splitter = QSplitter(Qt.Horizontal)

        # Left pane: File tree
        self.file_tree = FileTree()
        self.file_tree.itemClicked.connect(self.on_file_selected)
        splitter.addWidget(self.file_tree)

        # Middle pane: Editor
        self.editor = MarkdownEditor()
        self.editor.textChanged.connect(self.on_text_changed)
        splitter.addWidget(self.editor)

        # Right pane: Preview
        self.preview = MarkdownPreview()
        splitter.addWidget(self.preview)

        # Set initial sizes (20% file tree, 40% editor, 40% preview)
        splitter.setSizes([240, 480, 480])

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar().showMessage("Ready")

    def new_note(self):
        """Create a new note"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "New Note", self.file_tree.root_path, "Markdown Files (*.md)"
        )
        if filename:
            if not filename.endswith('.md'):
                filename += '.md'
            with open(filename, 'w') as f:
                f.write("# New Note\n\n")
            self.current_file = filename
            self.file_tree.populate_tree()
            self.editor.clear()
            self.statusBar().showMessage(f"Created: {filename}")

    def save_note(self):
        """Save current note"""
        if not self.current_file:
            self.new_note()
            return

        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.statusBar().showMessage(f"Saved: {self.current_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def open_folder(self):
        """Open a different notes folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Notes Folder")
        if folder:
            self.file_tree.root_path = folder
            self.file_tree.populate_tree()
            self.statusBar().showMessage(f"Opened folder: {folder}")

    def on_file_selected(self, item):
        """Load selected file into editor"""
        file_path = item.data(0, Qt.UserRole)
        if file_path and os.path.isfile(file_path) and file_path.endswith('.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.current_file = file_path
                self.statusBar().showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def on_text_changed(self):
        """Update preview when text changes"""
        markdown_text = self.editor.toPlainText()
        self.preview.update_content(markdown_text)

    def toggle_preview(self):
        """Show/hide preview pane"""
        self.preview.setVisible(not self.preview.isVisible())

def main():
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
