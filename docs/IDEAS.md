# Crazy ideas I have for this project

This is a collection of not completely organized or well thought out ideas I
have for the implementation of this project. This file will be updated regularly
for a time while I brainstorm about the project, but eventually it might
disappear once the ideas are "_better cooked_".


## Implementation

### File Structure

Most _Note Taking_ applications use one of two different philosophies on this
regard:

1. _One-note-per-file_: Each note is contained in a single file, usually using
   _MarkDown_, but other plain text markup languages are also used.
2. _Monolitic_: All notes are contained in a single file, most commonly within
   a _SQLite BD_ file, though, some applications use other formats (_i.e.:_,
   _CherryTree_ originally used exclusively a _XML_ like file, though, now users
   have the option of this format or a _SQLite DB_ file).

Each option has pros and cons that affect different users differently. Also,
there is a third option that I have not seen yet used (though, maybe I have just
not come across it but it is out there), a _hybrid_ model, where some defined
criteria are used to group notes that are all stored on a single file by each
criteria.

I am of the opinion that a user should have the option in the way that makes the
most sense for them, and maybe, if used a hybrid model, more than one of this
strategies could be used. Maybe it makes sense that your tasks are in a _SQLite
DB_ file (not human readable outside the application, but incredibly fast and
efficient), your journal entries would be better stored in a human readable
format in a single file, but your _Zettelkasten_ might benefit of a
one-file-per-note model.


### Structuring of the Data

- **Notes:** Just as with other popular Note-Taking applications, it makes a lot
  of sense for notes to be the main entities, the main data containers. But not
  all notes are equal. The data and metadata of your tasks is different than
  that of the permanent notes in your Zettelkasten, or the recipes in your meal
  plan. Also, it makes sense for a note to be divided into two parts:
  - **Front Matter:** metadata, information about the note, but not about the
    specific information contained in it. Probably using _YAML_ is the best way
    to go about it.
  - **Body of the Note:** The actual content of the note, whether the text it
    contains is _Plain Text_, _MarkDown_, _LaTeX_, or some other format that
    makes sense as long as it can be codified in UTF-8.
- **Containers:** This is a list all the notes of the same type within a
  _Collection_. For example, your Zettelkasten might have permanent (or
  _evergreen_) notes, fleeting notes, literature notes, insertion notes, etc.
  Each of these categories might have its own container.
- **Collection:** This could be seen as _a container of containers_. For
  example, as in the previous example, your Zettelkasten could be a collection.
  Maybe you are writing your next best-seller novel, and that is within a
  collection, with different containers for your research notes, your character
  description, your scenes, etc.
- **Configuration Files:** As there are different structures, these have to be
  specified and configured somewhere. This can be done using _YAML_.

## Features

More to come.

- **Version Control:** Some times we might think that a previous version of a
note makes more sense than the last one we had, and we might go back to it. Or
maybe, we suffered of data corruption. Having Version Control is a very good
idea.

## Potentially useful stuff

### Format specifications

- [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/)
- [CommonMark 0.5](https://spec.commonmark.org/0.5/)

### Potential Tools

- [Mermaid Diagramming](https://mermaid.js.org/)
	- [Git Repository](https://github.com/mermaid-js/mermaid)
	- [Licence](https://github.com/mermaid-js/mermaid/blob/develop/LICENSE)
