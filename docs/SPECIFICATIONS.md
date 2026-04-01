# Specifications

|      Project: |  Commonplace  |
| ------------: | :-----------: |
|       Author: | David Jiménez |
| File Version: |    `0.1.0`    |

This file contains the specification of different parts of the project.

## General Structure

**Commonplace** is a _Note Taking App_, this means, the main entity within this
environment is the _note_.  In this case, a note is a piece of data in text
format. Nevertheless, for most users, the notes they take are not all equal, not
only on the nature of their content, but also on the function they serve and the
workflows they follow.

To address this situation, Commonplace organizes notes into _collections_, that
can be viewed as a set of notes that have a related nature and followed a
similar or correlated workflow.

As both notes and collections may contain information (both data and metadata)
of different nature and may follow different workflows, they need to start with
a previously stated configuration that describe how such data is structured and
how it should be treated. This is achieved  through _configuration files_.

All notes live on a shared environment, called a _workspace_. Every note on a
workspace can link to each other, but the user can, if they so desire, create
separate _worspaces_.

Not only the way the data is handle by the application, but also how it is
stored within the user's device matter. Commonplace's pledge is to never seize
control of your data, and it will never use a closed proprietary format. On the
contrary, Commonplace will always industry standard open file formats.
Nevertheless, every format has strengths and weaknesses, that affect different
users differently. Because of this, Commonplace strives to provide a variety of
options.

## The Notes

For **Commonplace**, a _note_ is a portion of text containing two main sections:

- **Metadata:** Specifications about the note itself and about the data it
  contains. This will always be stored at the beginning of the note body in
  _YAML_ format.
- **Body:** The actual contents of the note, that can be anything that is
  encoded in text format. This may be plain text (including code in a
  programming language) or any markup language (initially _MarkDown_ and
  _LaTeX_)

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

The note itself starts with a _YAML_ header, and the four entries on it are
mandatory for every note inside a **Commonplace**.

- `uuid`: Every note needs an internal ID, for identification, linking, indexing
  and structure purposes. It is generated using the UUID version 4 standard.
  This information should be protected and the user should not be able to change
  it. Editions with external text editors are the responsibility of the user.
- `note_type`: As a note has a nature that can be different to another note, a
  type is specified. The built-in basic note types are specified below. This
  field should be protected, and changes should only be made from a type to
  another that extend it, and these changes should be rare and carefully
  managed.
- `body_format`: This field indicates what is the format of the contents of the
   note. This is relevant, as it tells **Commonplace** how to render such
   content.
- `collection`: Every note is inside of a collection, and this one should be
   specified. A note might change collections, but this has to be handled
   carefully.


### Note Types

The _type_ of a _note_ specifies to **Commonplace** some basic characteristics
about the nature of the metadata and the body contents of the note. The user has
the capability to create their own types, usually by extending a previously
existing type. The following are the basic types:

1. `basic_note`: This is the notes as has been described, a metadata header and
    a body in some plain text or markup language format.
2. `basic_metadata`: Some notes do not require a body for the task, and requires
    only the information stored in the metadata to achieve their purpose. Thus,
    there is a type that specifies this.
3. `basic_structure`: In some cases, the information contained in the note
   follows a predictable pattern that creates a structure. This type allows to
   define this within a note and simplifies the treatment or these notes within
   the application.

#### Basic Notes

The first note we showed is an example of a basic note. The following is a more
complex example:


```
---
uuid: "d8b65327-1505-4b2c-aeda-fd40d478a91c"
note_type: "basic_note"
body_format: "latex"
collection: "Math DB"
type: "problem"
courses:
  - "MA2210: Applied Differential Equations"
  - "MA1005: Differential Equations"
main_topic: "Differental Ecuations"
topics:
  - Abel's Formula
  - Variation of Parameters
...
Consider the following differential equation:

$$tx''(t)+2x'(t)+tx(t)=1.$$

Knowing that $x_1(t)=\dfrac{\sen(t)}{t}$ is a particualr solution of the
associated homogeneous equation, determine the general solution of the given
equation.
```

In this case, it is specified that the format of the body is in latex, inside a
collection called "Math DB", and there are a few of `uda` (User Defined
Attributes), including the field `type`. The selection of `note_type` instead of
simply `type` is intentional, as this second might be used by the user to imply
the nature of the note within their own workflow.

#### Basic Metadata

When a note does not need a body, this might be indicated to the application,
and used as such. For example, within a task manager you might need to add as a
task _Renew car registration_. This could be done as followed.

```yaml
---
uuid: "05d5cf5a-0bfe-4590-a642-36bded0b322e"
note_type: basic_metadata
body_format: none
collection: Task Manager
type: task
place: DMV on Whitehall
area: personal
description: Renew car registration
status: pending
due: "2026-07-01"
scheduled: "2026-06-15"
priority: high
...
```


#### Basic Structure

As previously said, there are notes that follow a given pattern. For example, a
recipe have for the most part, four sections: General information (portions,
time of cooking, etc), list of ingredients, preparations and notes. For this we
introduce a new marker, `:::` (three consecutive colons) that allows to include
commands into the body of the note.

```
---
uuid: "9f571078-ecd9-48d5-a9d1-282fd3fe698e"
note_type: basic_structure
body_format: markdown
collection: Recipe Book
title: Chicken Cesar Tacos
...
::: section: General Information :::

|  Servings: |    6    |
| ---------: | :-----: |
| Prep Time: | 10 mins |
| Cook Time: | 10 mins |

::: section: Ingredients :::

- 1 pound ground chicken
- 6 (6 inches) flour tortillas
- 2 teaspoons Greek seasoning
- 1/4 teaspoon salt
- 1/4 teaspoon ground black pepper
- 1 package Cesar Salad Mix
- 1 tablespoon olive oil

::: section: Preparation :::

Spread ground chicken evenly in a very thin layer over each tortilla, spreading
the meat all the way to the edges. Sprinkle with Greek seasoning, salt, and
pepper.

Chop lettuce (if pieces are large) into smaller pieces. Toss with included
packets of dressing and cheese. Slightly crush croutons included in salad mix
and set aside. 

Heat a griddle or large nonstick skillet on medium-high heat. Spread half of the
olive oil over the hot surface.  Working in 2 batches, place prepared tortillas,
meat side down on griddle and cook, undisturbed, until meat is browned and
cooked through, about 3 minutes. Flip, and cook 1 minute more. Repeat with
remaining tacos. 

Top tacos evenly with Caesar salad and sprinkle with crushed croutons. Fold in
half and serve immediately.

```


### Multiple notes on a file

For some uses, it might be a good idea to store multiple notes within a same
file, whether it is within a sub-collection, a collection or an entire
workspace. For this cases we introduce a new marker, `::::` (four consecutive
colons). This indicates the limits between notes or other pieces of text. For
example, we could have something like:


```
:::: begin: note ::::

---
uuid: "2eaaaa54-ba12-476a-8ceb-66037ecf00b5"
note_type: basic_note
body_format: latex
collection: Problems
tags:
  - algebra
---

\begin{problem}
Solve x^2 - 1 = 0
\end{problem}

:::: end: note ::::

:::: begin: note ::::

---
uuid: "6a51fb3e-802c-4dce-8f3a-c3810968b1b6"
note_type: basic_note
body_format: markdown
collection: General Notes
---
This is another note.

:::: end: note ::::

```


## The Collections

A collection unites different notes within a single container. How a type of
collection can be defined will be explored under _configuration files_, but a
collection, when done within a text file system, it will have the following
form:

```yaml
---
uuid: "5ea12a50-ded0-4750-b261-eee216dedbc8"
collection_type: cherrytree
collection_name: First Collection
subcollections:
  - "d2bb7de0-ba35-4f29-b797-28329ed5516d"
  - "fa706245-c97b-44b2-8098-52da651feadc"
collected_notes:
  - "b0828249-0029-41e1-b6b4-47a0349a8b82"
  - "bb1af2ae-f31e-4d97-b523-7f14a8e37eec"
  - "1447a469-3dd0-4f8a-81e0-6c61e1cff9af"
  - "0730e91a-b775-4a5f-a15b-1ae446c02e50"
...
```

The previous is equivalent to:

```yaml
---
uuid: "5ea12a50-ded0-4750-b261-eee216dedbc8"
collection_type: cherrytree
collection_name: First Collection
subcollections:
  - uuid: "d2bb7de0-ba35-4f29-b797-28329ed5516d"
    alias: Personal Notes
  - uuid: "fa706245-c97b-44b2-8098-52da651feadc"
    alias: Work Notes
collected_notes:
  - "b0828249-0029-41e1-b6b4-47a0349a8b82"
  - "bb1af2ae-f31e-4d97-b523-7f14a8e37eec"
  - "1447a469-3dd0-4f8a-81e0-6c61e1cff9af"
  - "0730e91a-b775-4a5f-a15b-1ae446c02e50"
...
```

The `uuid` field is the internal identifier. As a collection may contain other
collections as well as other notes, this are internally referenced by this
field. Nevertheless, every collection is required to have a name, and a is
allowed to have one too. Both are allowed to have multiple aliases if necessary.
As they can be referenced too by these additional identifiers, they can be
included in the definition, and this increases the readability.


## The Configuration Files

The configuration files are _YAML_ files where the configuration of new elements
(new types of notes or collections) are specified.  Throughout this section we
will explore:

- Keys on definitions
- Internal typing
- How to define new field types
- How to define new note types
- How to define new collection types.


### Keys on definitions

- `new_field_type`: Specifies a new field  type is to be defined.
	- `field_name`: Specifies the field name, or the key of the field. Its type
    is `word`. It is required.
	-  `field_type`: Specifies what the content of the field is allowed to be. It
     is required. Its type is `single_line` and follows.
	- `required`: Specifies whether or not the field is of mandatory presence in
    the metadata. It is an optional key. Its type is `boolean` and its default
    value (assumed if absent) is `false`.
	- `system_assigned`: Specifies whether the system assigns automatically this
    value. It is an optional key. Its type is `boolean` and its default value
    (assumed if absent) is `false`.
	- `overwrite`: Specifies whether or not the field can be modified, whether by
    the system or the user. It is an optional key. Its type is `boolean` and its
    default value (assumed if absent) is `true`.
	- `reassign`: Specifies whether or not the field's attributes (type, whether
    it is required, system assigned or can be overwritten) can be modified
    through extension.
	- `default`: Assign a default value to a particular field.
- `new_note_type`: Specifies a new note type is to be defined.
	- `note_type`: The name of the new note type, how it is referenced by the
    system. It is required and its type is `word`.
	- `metadata_fields`: Definitions of the standard fields. Its type is `list of
    word or field_definition`. It is optional, but if in a definition both
    `metadata_fields` and `body_specification` are absent, the definition will
    be ignored.
	- `body_specification`: Specifies what the format of the body. This is
    optional, but if in a definition both `metadata_fields` and
    `body_specification` are absent, the definition will be ignored.
	- `uda_allowed`: UDA stands for User Defined Attributes. This field is a
    `boolean` than when `false` prevents the user from adding new fields, and
    allows it when `true`, that is the default value.
	- `extends`: This fields references another `note_type`, and tells the system
    that the new note type takes all the specifications of the given type unless
    explicitly overwritten (if permitted), and/or adds to it. Its type is
    `word`, and it is optional, and a note type can extend only one previously
    defined type of note. If not specified, the system assumes the new type
    extends `minimal_note`.
- `new_collection_type`: Specifies a new collection type is to be defined.
	- `collection_type`: The name of the new collection type, how it is referenced
    by the system. It is required and its type is `word`.
	- `metadata_fields`:  Definitions of the standard fields. Its type is `list of
     word or field_definition`. It is optional, but if in a definition all three
     of `metadata_fields`, and `subcollections_included`, and
     `note_types_included` are absent, the definition will be ignored.
	- `subcollections_included`: It specifies what types of sub-collections are
    allowed/mandatory, and whether they are unique or multiple of this type of
    sub-collections are allowed. Its type is `word` or `inclusion_attributes`,
    that is, it is either the name of the type of the sub-collection, or a
    dictionary containing the fields specified below:
		- `inclusion_type`: The type of the sub-collection, required, and should be
      the identifier of a `collection_type` defined.
		- `required`: Specified if the sub-collection is required or not. It is an
      optional attribute. Its type is `boolean` and its default is `false`.
		- `unique`: Specifies if the sub-collection is unique or several of them can
      be created. Its type is `boolean` and its default is `false`.
	- `notes_types_allowed`: This specifies the types of notes that can be
    included inside a collection. It can be either `word` (the name of the note
    type) or an `inclusion_attributes` object (as previously specified).
	- `extends`: As with notes, a collection may extend one single collection.
    This is optional, and if not included, it is assumed that the collection is
    extending `empty_collection`.


#### Suggestions for best practices:

- Whenever possible, define new attributes independently and reserve definitions
  inside the `metadata_fields` only when a particular field is being redefined
  in some way. External definitions of fields with a same name is not allowed.
  Fields modified internally will be inherited by extensions.
- Although not forbidden by the system, it is recommended that new collections
  either have sub-collections or notes, but not both at the same time.


### Typing

The following are the types to be specified:

- `uuid`: It is a Universal Unique Identifier, generated through the UUID
  version 4 algorithm. This is, a string of 36 characters containing 32
  hexadecimal digits and 4 dashes in a format 8-4-4-4-12.
- `word`: A string, at least one character long, without spaces or special
  characters. This means `[A~Z,a~z,0~9,_,-]`.
- `single_line`: A single line string, that is, any string that does not have a
  new line character.
- `time_stamp`: Any ISO-8601 compliant string to represent a time stamp at least
  to the precision of a minute.
- `date`: Any ISO-8601 compliant string to represent a time stamp to the
  precision of a day.
- `text`: Any string or list of strings that comprise a piece of text.
- `boolean`: Any _YAML_ compliant expression of a boolean. That is `true` (or
  `yes` or `on`) and `false` (or `no` or `off`).
- `any`: Indicates that, within the allowable values for the field, it can take
  any.  
- `list`: indicates that the key value should be a list.
- `field_definition`: A dictionary containing at least the keys `field_name` and
  `field_type` with compliant values.
- `inclusion_attributes`: A dictionary containing the key `inclusion_type` and
  at least one of the keys `required` and `unique`, with compliant values.
- `referencer`: A dictionary containing the keys `uuid` and `alias` with
  compliant values.
- `internal_link`: A string starting with `[[` and ending with `]]` with a name
  or alias for an existing note.

Note that a definition like:

```yaml
field_type: list
```

is equivalent to

```yaml
field_type: list of any
```

and it is discourage.  It is preferred something like

```yaml
field_type: list of word or integer or referencer
```

where the field would be composed of a list and the elements can be of any of
these formats.


### Field Type Definitons

Based on the previous discussion, the following is the definition of the
obligatory fields.

```yaml
# These are the fields that are inheritted either by every note.
---
new_field_type:
  field_name: uuid
  field_type: uuid
  required: true
  assigned: system
  overwrite: false
  reassign: false
...


---
new_field_type:
  field_name: time_created
  field_type: time_stamp
  required: true
  assigned: system
  overwrite: false
  reassign: false
...


---
new_field_type:
  field_name: time_modified
  field_type: time_stamp
  required: true
  assigned: system
  reassign: false
...


---
new_field_type:
  field_name: note_type
  field_type: word
  required: true
  assigned: system
  reassign: false
...


---
new_field_type:
  field_name: body_format
  field_type: word
  assigned: system
  reassign: false
...


---
new_field_type:
  field_name: collection
  field_type: single_line
  required: true
  assigned: system
  reassign: false
...

# These are the fields that are inheritted either by every collection.
---
new_field_type:
  field_name: collection_type
  field_type: word
  required: true
  assigned: system
  reassign: false
...


---
new_field_type:
  field_name: collection_name
  field_type: single_line
  required: true
  reassign: false
...

```

Note that although the first two field types has six attributes, the others have
five, as `uuid` and `time_created`  should never be changed. As all these fields
are assigned by the system, the user has no direct editing access to them
though, they might be modified through the system.

The fact that

**NOTE:** If scripting or plugin capabilities are implemented, a decision has to
be made if modification of fields assigned by the system is allowed by these
external tools.

Other fields that can be useful for most notes to have could be

```yaml
---
new_field_type:
  field_name: tags
  field_type: list of words
...


---
new_field_type:
  field_name: title
  field_type: single_line
...


---
new_field_type:
  field_name: aliases
  field_type: list of single_line
...


---
new_field_type:
  field_name: internal_links
  field_type: list of uuid or referencer
...


---
new_field_type:
  field_name: description
  field_type: list of single_line
...


---
new_field_type:
  field_name: notes
  field_type: list of single_line
...


---
new_field_type:
  field_name: subcollections
  field_type: list of uuid or referencer
...


---
new_field_type:
  field_name: collected_notes
  field_type: list of uuid or referencer
...


```

It is important to note that the following two definitions are equivalent, as
the missing attributes in the first present in the second are the default
values.

```yaml
---
new_field_type:
  field_name: tags
  field_type: list of words
...


---
new_field_type:
  field_name: tags
  field_type: list of words
  required: false
  assigned: user
  overwrite: true
  reassign: true
...
```


### Note Type Definition

Let's start with the definition for a `minimal_note` as an example. This note is
not intended as one to be used by the user, but as a minimal place to extend.

```yaml
new_note_type:
  note_type: minimal_note
  metadata_fields:
    - uuid
    - time_created
    - time_modified
    - note_type
    - body_format
```

This is a minimal structure. Also, note that as the definition of the field
`body_format` is not mandatory, it allows for notes without a body, like
`basic_metadata`.

Now, the definition of `basic_note`:

```yaml
new_note_type:
  note_type: basic_note
  extends: minimal_note # Not required as it is the default value
  metadata_fields:
    - tags
    - title
    - aliases
    - internal_links
    - field_name: body_format
      required: true
  body_specification:
    body_content: text
    body_format:
      format: any
      required: true
```


In this case, the `body_specification` mean that there is a body is present, and
it is of the type `text`. Observe that in this case, the last field is a
`field_definition`, and is defining `body_format` as it was not required in
`minimal_note`, but `basic_note` does require to specify a format.

The definition of `basic_metadata`:

```yaml
new_note_type:
  note_type: basic_metadata
  matadata_fields:
    - tags
    - internal_links
    - description
    - notes
```

The definition for ``

### Collection Type Definition

As with `minimal_note`, there is a default inheritance collection that is not
expected to be used by the user, and we call it `empty_collection`. This is its
definition:

```yaml
new_note_type:
  note_type: minimal_note
  metadata_fields:
    - uuid
    - time_created
    - time_modified
    - collection_type
    - collection_name
```

**NOTE:** I need to expand this.

## The File Management

The writing of this section is postponed for a later time.

## The User Interface

The writing of this section is postponed for a later time.

## The Queries

The writing of this section is postponed for a later time.
