
# App by tabs

## <a name="characters-tab"/>'Characters' tab

## <a name="summary"/>Summary

* [Screenshot](#screenshot)
* [Introduction](#introduction)
* [Usage](#usage)
    * [Characters' name list](#name_list)
        * [Adding a new character name](#list_add)
        * [Renaming a character name](#list_rename)
        * [Deleting a character name](#list_del)
        * [List purge](#list_purge)
    * [Character's history log](#history_log)
    * [Relationships canvas](#canvas)
        * [Adding a new character name](#canvas_add)
        * [Renaming a character name](#canvas_rename)
        * [Deleting a character name](#canvas_del)
        * [Adding a new relationship](#canvas_add_rel)
        * [Renaming a relationship](#canvas_rename_rel)
        * [Deleting a relationship](#canvas_del_rel)
* [Finally](#finally)
* [Quick nav](#quick-nav)


## <a name="screenshot"/>Screenshot

![image](../../images/screenshots/screenshot-005.png)

Return to [summary](#summary).


## <a name="introduction"/>Introduction

This app tab manages with movie characters, their names, history logs
and relationships.

It is composed of:

1. characters' name list, at top-left side;
1. character's history log, on bottom-left side;
1. characters relationships canvas, right side.

All section panes are **resizable**: put mouse pointer between each
pane, then click and drag sash to get desired size.

Return to [summary](#summary).


## <a name="usage"/>Usage

### <a name="name_list"/>Characters' name list

#### <a name="list_add"/>Adding a new character name

Click on `+` button to add a new character name.

Character names are automatically set to uppercase: this is a script
writing policy.

Character names must be unique.

Return to [summary](#summary).

#### <a name="list_rename"/>Renaming a character name

First, select a character name into the list, then click on `Rename`
button.

Please, note it is *NOT* possible to rename a character name once it is
mentioned into ['Scenario' tab](en_tab_scenario.html)'s text editor
contents.

New character name must be as unique as any other one.

Return to [summary](#summary).

#### <a name="list_del"/>Deleting a character name

First, select a character name into the list, then click on `-` button.

A confirmation dialog will popup before deleting definitely.

Please, note it is *NOT* possible to delete a character name once it is
mentioned into ['Scenario' tab](en_tab_scenario.html)'s text editor
contents.

Return to [summary](#summary).

#### <a name="list_purge"/>List purge

One may need to clean up characters' name list in order to keep only
scenario's mentioned names.

Click on `Purge` button to delete all unmentioned names.

A confirmation dialog will popup before deleting definitely.

Return to [summary](#summary).

### <a name="history_log"/>Character's history log

First, select a character name into the list, then click into
character's history log text zone.

The big white zone is called a **plain text editor**.

This object allows multiple line editing with carriage return,
undo/redo stack and many other features.

Pressing on the carriage return key will insert a new **paragraph**.

Double-clicking on a word will select **this word only**.

Triple-clicking on a word will select **the whole paragraph**.

You may **select all text** by using `Edit > Select all` menu option or
with `<Ctrl-A>` keyboard shortcut.

Any selection band is likely to be replaced by the next keystroke on
the keyboard.

To **undo** last operation, either use `Edit > Undo` menu option or try
`<Ctrl-Z>` keyboard shortcut.

To **redo** last cancelled operation, either use `Edit > Redo` menu
option or try `<Ctrl-Shift-Z>` keyboard shortcut.

Please, note this text editor manages with **automatic backup**
feature: anything you enter into this object will be automatically
saved into software's memory. However, this does not exempt you from
saving your project file regularly.

Return to [summary](#summary).

### <a name="canvas"/>Relationships canvas

#### <a name="canvas_add"/>Adding a new character name

Simply double-click on a canvas empty zone (grey zone).

Character names are automatically set to uppercase: this is a script
writing policy.

Character names must be unique.

Return to [summary](#summary).

#### <a name="canvas_rename"/>Renaming a character name

Double-click onto desired character name label on the canvas.

Please, note it is *NOT* possible to rename a character name once it is
mentioned into ['Scenario' tab](en_tab_scenario.html)'s text editor
contents.

New character name must be as unique as any other one.

Return to [summary](#summary).

#### <a name="canvas_del"/>Deleting a character name

Do a `<Ctrl-Click>` onto desired character name label on the canvas.

This may be obtained by clicking on target while pressing `<Ctrl>` key
down on your keyboard.

A confirmation dialog will popup before deleting definitely.

Please, note it is *NOT* possible to delete a character name once it is
mentioned into ['Scenario' tab](en_tab_scenario.html)'s text editor
contents.

Return to [summary](#summary).

#### <a name="canvas_add_rel"/>Adding a new relationship

Press `<Shift>` key on your keyboard while clicking onto start
character name label on the canvas and dragging link to a destination
character name label. Release then mouse click and `<Shift>` key.

Please, note adding a new relationship must respect the followings:

1. a relationship link *CANNOT* be drawn from a character name label to
itself;
1. a relationship link *CANNOT* be drawn from a character name label to
nowhere;
1. only *ONE* relationship link between two same character name labels,
no duplex links.

A relationship is made of a black drawn line with its associated black
relationship text label.

Return to [summary](#summary).

#### <a name="canvas_rename_rel"/>Renaming a relationship

Double-click onto desired relationship text label on the canvas.

Return to [summary](#summary).

#### <a name="canvas_del_rel"/>Deleting a relationship

Do a `<Ctrl-Click>` onto desired relationship text label on the canvas.

This may be obtained by clicking on target while pressing `<Ctrl>` key
on your keyboard.

A confirmation dialog will popup before deleting definitely.

Return to [summary](#summary).


## <a name="finally"/>Finally

Clicking onto a character name label on the canvas will also select
this name into characters' name list, on top-left side.

Conversely, clicking on a list item will try to show up the name label
on the canvas, especially if it is out of viewport bounds.

Character name labels on the canvas do support `Drag'n'Drop` feature:
click on desired character name label, drag it to another location and
then release mouse click to drop it there.

One may browse easily into relationships canvas by clicking onto an
empty zone (grey zone), moving mouse to the desired direction and then
releasing mouse click when arrived.

**IMPORTANT**: don't forget to **save your project** regularly, either
with `Project > Save` menu option or with `<Ctrl-S>` keyboard shortcut.

Return to [summary](#summary).

---

#### <a name="quick-nav"/>Quick nav

* **App by tabs**
    * ['Title/Data' tab](en_tab_title_data.html)
    * ['Draft/Notes' tab](en_tab_draft_notes.html)
    * ['Pitch/Concept' tab](en_tab_pitch_concept.html)
    * ['Characters' tab](en_tab_characters.html)
    * ['Scenario' tab](en_tab_scenario.html)
    * ['Storyboard' tab](en_tab_storyboard.html)
    * ['Resources' tab](en_tab_resources.html)
* **Extra tools**
    * [Name database](en_tools_name_db.html)
    * [Story/pitch templates](en_tools_pitch_templates.html)
    * [Scenario Elements Editor (SEE)](en_tools_scenario_elements_editor.html)

Return to [homepage](index.html).
