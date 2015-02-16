
# App by tabs

## <a name="storyboard-tab"/>'Storyboard' tab

## <a name="summary"/>Summary

* [Screenshot](#screenshot)
* [Introduction](#introduction)
* [Usage](#usage)
    * [Scene browser and preview](#scene_nav)
    * [Shot list](#shot_list)
        * [Adding a shot](#shot_add)
        * [Deleting a shot](#shot_del)
        * [List purge](#shot_purge)
    * [Shot editor](#shot_editor)
        * [Shot number](#shot_number)
        * [Shot title](#shot_title)
        * [Shot text](#shot_text)
    * [Character history logs](#char_info)
* [Finally](#finally)
* [Quick nav](#quick-nav)


## <a name="screenshot"/>Screenshot

![image](../../images/screenshots/screenshot-010.png)

Return to [summary](#summary).


## <a name="introduction"/>Introduction

This app tab is intended to help writing shot details of scenario
(storyboard).

It is composed of:

1. a navigation pane, on left side;
1. a storyboard pane, at center;
1. a character history log pane, on right side.

All section panes are **resizable**: put mouse pointer between each
pane, then click and drag sash to get desired size.

Return to [summary](#summary).


## <a name="usage"/>Usage

### <a name="scene_nav"/>Scene browser and preview

Scene browser fills out automatically while scripting new scenes into
[scenario's](en_tab_scenario.html) text editor.

Click on a list item to get its scene preview.

Return to [summary](#summary).

### <a name="shot_list"/>Shot list

Shot list content depends on [scene browser's](#scene_nav) current
selected item.

#### <a name="shot_add"/>Adding a shot

Select first the desired scene into the scene browser, then click on
`+` button to add a new shot item for this scene.

Return to [summary](#summary).

#### <a name="shot_del"/>Deleting a shot

Select first the desired scene into the scene browser, select the
concerned shot item in its shot list and then click on `-` button to
delete this shot item for this scene.

A confirmation dialog will popup before deleting definitely.

Please, note empty shot items will delete without confirmation dialog.

Return to [summary](#summary).

#### <a name="shot_purge"/>List purge

To purge shot list from empty shot items, select first the desired
scene into the scene browser, then click on `Purge` button.

A confirmation dialog will popup before deleting definitely.

Return to [summary](#summary).

### <a name="shot_editor"/>Shot editor

The shot editing form is composed of a shot number label, a shot title
entry and a text editor.

#### <a name="shot_number"/>Shot number

Shot number is formatted along `#{scene_index}.{shot_index}` template
string.

Numbering is automatic and may sometimes be subject to discontinuity,
but [exporting](en_app_topmenu.html#project_export_pdf) storyboard to
PDF&reg; will renumber shots correctly in output document.

Return to [summary](#summary).

#### <a name="shot_title"/>Shot title

Click into the white text entry to fill out shot's title.

Return to [summary](#summary).

#### <a name="shot_text"/>Shot text

Click onto the white text zone to fill out shot text contents.

The big white zone is called a **plain text editor**.

This text editor especially supports character names
[detection](en_tab_scenario.html#detection).

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

Return to [summary](#summary).

### <a name="char_info"/>Character history logs

Select a character name into upper name list and get character's
history log underneath.

Return to [summary](#summary).


## <a name="finally"/>Finally

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
