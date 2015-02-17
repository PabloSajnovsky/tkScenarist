
# Extra tool: 'Name database'

## <a name="summary"/>Summary

* [Screenshot](#screenshot)
* [Introduction](#introduction)
* [Usage](#usage)
    * ['Search' pane](#search)
    * ['Tools' pane](#tools)
        * [Browsing results](#browse_results)
        * [Importing a CSV file](#file_import)
* [Finally](#finally)
* [Quick nav](#quick-nav)


## <a name="screenshot"/>Screenshot

![image](../../images/screenshots/screenshot-006.png)

Return to [summary](#summary).


## <a name="introduction"/>Introduction

This tool is aimed to ease character name search among thousands of
names coming from all over the world.

It is composed of:

1. a Database view, on left side;
1. a 'Search' pane, on top right side;
1. a 'Tools' pane, on bottom right side.

Extra tool panes are *NOT* resizable.

Return to [summary](#summary).


## <a name="usage"/>Usage

### <a name="search"/>'Search' pane

By default, all data are shown off without any criteria.

To set a DB query, click on one of `contains`, `starts with`, `ends
with` or `matches exactly` choice buttons, fill out the mention entry
text, eventually choose which mention (e.g. name, origin, description)
should be concerned, select which type of name you wish (male, female,
both, none) and then wait for automatic query submission.

Each time you make a change into criteria, the automatic query
submission maechanism fires up after **about half a second**.

Return to [summary](#summary).

### <a name="tools"/>'Tools' pane

#### <a name="browse_results"/>Browsing results

Once you got query results, you can browse each page by clicking on one
of `Show first` (page), `Show previous`, `Show next` buttons in 'Tools'
pane.

Please, note numerous number of result pages is generally symptomatic
of too imprecise DB query. One should refine criteria to get something
more accurate.

Also note each time criteria are changed, the DB query result view is
**reset to first page** of new results.

Return to [summary](#summary).

#### <a name="file_import"/>Importing a CSV file

Click on `Import file (CSV)` button at the bottom end of 'Tools' pane.

An importing dialog tool will then popup to help you in adding new
names.

![image](../../images/screenshots/screenshot-007.png)

In this dialog tool:

Click on `Browse` button to choose the CSV file you want to import.

**CAUTION**: only [RFC 4180](http://tools.ietf.org/html/rfc4180) *de
facto* standard [CSV](http://en.wikipedia.org/wiki/Comma-separated_values) files are
supported by `tkScenarist` software.

On correct file format, take a look at 'Preview' data contents and then
verify automatic 'Fields' redirections.

Fix incorrect 'Fields' redirections, if necessary, then click on
`Import` button.

Importation process is fully automatic.

Doublets (names in double into DB) are filtered to keep database as
small as possible.

Click on dialog's `OK` button once finished.

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
