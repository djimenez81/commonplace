# Specifications

|      Project: |  Commonplace  |
| ------------: | :-----------: |
|       Author: | David Jiménez |
| File Version: |    `0.1.0`    |

This file contains the specification of different parts of the project.

## General Structure

**Commonplace** is a _Note Taking App_, this means, the main entity within this environment is the _note_.  In this case, a note is a piece of data in text format. Nevertheless, for most users, the notes they take are not all equal, not only on the nature of their content, but also on the function they serve and the workflows they follow.

To address this situation, Commonplace organizes notes into _collections_, that can be viewed as a set of notes that have a related nature and followed a similar or correlated workflow.

As both notes and collections may contain information (both data and metadata) of different nature and may follow different workflows, they need to start with a previously stated configuration that describe how such data is structured and how it should be treated. This is achieved  through _configuration files_.

All notes live on a shared environment, called a _workspace_. Every note on a workspace can link to each other, but the user can, if they so desire, create separate _worspaces_.

Not only the way the data is handle by the application, but also how it is stored within the user's device matter. Commonplace's pledge is to never seize control of your data, and it will never use a closed proprietary format. On the contrary, Commonplace will always industry standard open file formats. Nevertheless, every format has strengths and weaknesses, that affect different users differently. Because of this, Commonplace strives to provide a variety of options.

## The Notes

For **Commonplace**, a _note_ is a portion of text containing two main sections:

- **Metadata:** Specifications about the note itself and about the data it contains. This will always be stored at the beginning of the note body in _YAML_ format.
- **Body:** The actual contents of the note, that can be anything that is encoded in text format. This may be plain text (including code in a programming language) or any markup language (initially _MarkDown_ and _LaTeX_)

This means, a valid note may look like:

```
---
uuid: 'a996f5d4-637b-40f9-a846-59096192efdc'
note_type: basic_note
body_format: plain_text
collection: First Collection
...

The data contained within this note is jut for show.

```

The note itself starts with a _YAML_ header, and the four entries on it are mandatory for every note inside a **Commonplace**.

- `uuid`: Every note needs an internal ID, for identification, linking, indexing and structure purposes. It is generated using the UUID version 4 standard. This information should be protected and the user should not be able to change it. Editions with external text editors are the responsibility of the user.
- `note_type`: As a note has a nature that can be different to another note, a type is specified. The built-in basic note types are specified below. This field should be protected, and changes should only be made from a type to another that extend it, and these changes should be rare and carefully managed.
- `body_format`: This field indicates what is the format of the contents of the note. This is relevant, as it tells **Commonplace** how to render such content.
- `collection`: Every note is inside of a collection, and this one should be specified. A note might change collections, but this has to be handled carefully.


### Note Types

The _type_ of a _note_ specifies to **Commonplace** some basic characteristics about the nature of the metadata and the body contents of the note. The user has the capability to create their own types, usually by extending a previously existing type. The following are the basic types:

1. `basic_note`: This is the notes as has been described, a metadata header and a body in some plain text or markup language format.
2. `basic_metadata`: Some notes do not require a body for the task, and requires only the information stored in the metadata to achieve their purpose. Thus, there is a type that specifies this.
3. `basic_structure`: In some cases, the information contained in the note follows a predictable pattern that creates a structure. This type allows to define this within a note and simplifies the treatment or these notes within the application.

#### Basic Notes

The first note we showed is an example of a basic note. The following is a more complex example:



## The Collections



## The Configuration Files



## The File Management



## The User Interface

This is likely to be undefined for a little while.

## The Queries

This is likely to be undefined for a little while.
