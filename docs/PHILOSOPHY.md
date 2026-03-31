# Philosophy

There are plenty of note taking apps out there. The developers for each of them
have to take decisions with respect to the way they handle data, the way they
link or label notes, and the way they build the knowledge structure. At the end
of the day, this imposses a particular workflow to the user, often with a steep
learning curve.

Of course, the behavior of many of these applications can be endlessly extended
and reconfigured, thus, at least theoretically, the user can more or less addapt
their favorite application to their preferred workflow. Nevertheless, this
requires some technical expertice and time, therefore, some often observed
situations are:

1. The user abandon the application.
2. The user ends up addopting habits substandard for their workflow.
3. The user spends a lot of time playing around with options, plugins, etc.

**Commonplace** wants to be a note taking application that is intuitive to use
and _structure agnostic_. With this we mean that the app can easily be
configured to addopt different workflows, including simultaneously.

We pretend to accomplish this by separating the implementation and configuration
of three different parts of the process:

1. **The notes:** the containers of the data.
2. **The logic:** how is this data proccessed.
3. **The interface:** How is this data displayed to the user.

Also, different applications tend to implement different strategies of file
management. The most common of them (and probably both of the extremes of the
spectrum of possibilities) are, on one side, the _one-note-per-file_, where, as
the name implies, each note is stored in a different file, usually plain text
using some markup (e.g.: _MarkDown_) or data serialization language (e.g.:
_JSON_). On the other side would be the _monolitic_ strategy, where all the
notes are stored in a single file, more often using _SQLite DB_, though some
applications also implement the use of _XML_ or _JSON_ files. Each of these
combinations have implications on one side or another for future proofing, human
readability, speed, performance and ease of sync. More often than not, the
decision is made by the developers, even when different users could benefit more
of using another, or a combination of these. We intend to offer this
flexibility.

## The Notes

In a _Note Taking App_, unsurprisingly, the **notes** are the central entities.
This are the containers of the information collected, the reason for the app to
exist.

More often than not, notes have a _body_ (the actual information contained in
them), usually in a mark up language or in rich text format, and _metadata_.
For a while now, the most popular note taking apps enconde metadata in _YAML_ at
the beginning of the file, and then the contents in _MarkDown_. Others include
it as fields in a database table.

With respect to the body, the fact that _MarkDown_ is the only option is a
limitating factor. It is a very versatile format, and as it is rendered to
_HTML_, it can be extended, even used to write math through _LaTeX_ commands.
But _MarkDown_ is not _LaTeX_, and cannot be directly exported to a _LaTeX_
document, as the way some commands are written in one format are incompatible
with the other. As long as it is plain text (even code) or a markup language,
the content could be stored, even if rendering is a problem to solve.

Regarding the metadata, it is usually used for searching and linking. More than
this usually requires either quite a bit of tweeking around. Nevertheless, this
metadata can also be used to add structure.

## The Logic

Whether the notes are part of a _Zettelkasten_ where there is the need for a
knowledge structure, or a task in a _Productivity System_ that needs to be
pulled into the _daily page_ on the correct day, it is the logic that interprets
the relations between these data points.

Nevertheless, there is a lot more structure that can be obtained in this manner.
For example, if a user is writing a novel, there are research notes, character
profiles, plots, timelines, synopsis, scenes, chapters. Some applications
require the user to create a _Mao of Content_ (_MoC_, also sometimes named
_Maps of Concept_ when related to a _Zettelkasten_), and updated in a regular
basis.

Nevertheless, based on the metadata, this type of relations can be build
automatically, depending on context.

## The Interface

Most _Note Taking Applications_ have a particular look that can be changed only
regarding _Themes_, or slightly depending on complex plugins. Nevertheless,
much of the way the data is shown to the user can be configured using much less
technical tools. 
