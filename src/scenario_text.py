#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkScenarist - screen writing made simpler

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports
import re
import json
import tkinter as TK
import tkRAD.widgets.rad_widget_base as RW
from tkRAD.core import tools


class ScenarioText (RW.RADWidgetBase, TK.Text):
    """
        Scenario-specific text widget class;
    """

    # class constant defs
    CONFIG = {
        "autoseparators": False,    # do *NOT* change this /!\
        "background": "white",
        "font": "monospace 12",
        "foreground": "black",
        "highlightthickness": 1,
        "undo": False,              # do *NOT* change this /!\
        "wrap": "word",
    }

    DEAD_KEYS = (
        "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L",
        "Alt_R", "Caps_Lock",
    )

    DEFAULT_TAG = "scene"

    # NOTICE: element name == element tag
    ELEMENT_DEFAULTS = {
        "action": {
            "label": _("Action"),
            "config": {
                "spacing1": "5",
                "spacing3": "5",
            },
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "character",
            "ctrl_return": "transition",
            "ctrl_switch": "scene",
        },
        "character": {
            "label": _("Character"),
            "config": {
                "font": "monospace 12 bold",
                "foreground": "grey40",
                "lmargin1": "5c",
                "lmargin2": "5c",
                "rmargin": "1c",
                "spacing1": "5",
            },
            "on_return": "dialogue",
            "on_tab": "parenthetical",
            "tab_switch": "action",
            "ctrl_return": "action",
        },
        "dialogue": {
            "label": _("Dialogue"),
            "config": {
                "foreground": "grey30",
                "lmargin1": "3c",
                "lmargin2": "3c",
                "rmargin": "1c",
                "spacing1": "5",
                "spacing3": "10",
            },
            "on_return": "character",
            "on_tab": "action",
            "tab_switch": "parenthetical",
            "ctrl_return": "scene",
        },
        "parenthetical": {
            "label": _("Parenthetical"),
            "config": {
                "foreground": "grey50",
                "font": "monospace 12 italic",
                "lmargin1": "4c",
                "lmargin2": "4c",
                "rmargin": "1c",
            },
            "on_return": "dialogue",
            "on_tab": "dialogue",
            "tab_switch": "dialogue",
            "ctrl_return": "action",
        },
        "scene": {
            "label": _("Scene"),
            "config": {
                "background": "grey90",
                "spacing1": "5",
                "spacing3": "5",
            },
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "action",
            "ctrl_return": "transition",
        },
        "transition": {
            "label": _("Transition"),
            "config": {
                "justify": "right",
                "rmargin": "10",
            },
            "on_return": "scene",
            "on_tab": "transition",
            "tab_switch": "scene",
            "ctrl_return": "action",
        },
    }

    INS_LINE = (
        "{} linestart".format(TK.INSERT),
        "{} linestart + 1 line".format(TK.INSERT),
    )

    INS_LINE_END = (
        "{} linestart".format(TK.INSERT),
        "{} lineend".format(TK.INSERT),
    )


    def __init__ (self, master=None, **kw):
        # default values
        self.CONFIG = self.CONFIG.copy()
        self.CONFIG.update(kw)
        # super inits
        TK.Text.__init__(self, master)
        self.configure(**self._only_tk(self.CONFIG))
        RW.RADWidgetBase.__init__(self, master, **self.CONFIG)
    # end def


    def _do_reformat_line (self, args, kw):
        """
            reformats insertion cursor's line in order to match element
            tag constraints;
        """
        # inits
        _tag = self.update_current_tag(TK.INSERT)
        _text = self.get(*self.INS_LINE_END)
        _cursor = self.index(TK.INSERT)
        # reformat along with element tag constraints
        _text, _adjust = self.switch_to_method(
            "reformat_line_{}".format(_tag), _text
        )
        # reset text
        self.delete(*self.INS_LINE_END)
        self.insert(self.INS_LINE_END[0], _text, _tag)
        # disable adjustments?
        if kw.get("no_adjust"):
            _adjust = ""
        # end if
        # reset cursor
        self.move_cursor("{} {}".format(_cursor, _adjust))
    # end def


    def _do_update_line (self, args, kw):
        """
            updates line contents in order to keep it correctly
            up-to-date;
        """
        # get tag at insertion cursor
        _tag = self.update_current_tag(TK.INSERT, **kw)
        # got element tag?
        if _tag in self.ELEMENT:
            # remove all line tags
            self.tag_remove(self.tag_names(TK.INSERT), *self.INS_LINE)
            # reset tag all line long
            self.tag_add(_tag, *self.INS_LINE)
            # notify app
            self.events.raise_event(
                "Scenario:Current:Element:Update", element_tag=_tag
            )
        # end if
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Scenario:Switch:Line": self.switch_line,
            }
        )
        # tkinter event bindings
        # CAUTION:
        # self.tag_bind() triggers event only when mouse pointer
        # is *OVER* tag's region - WTF? /!\
        # we have to work with a tag dispatcher
        self.bind("<Key>", self.slot_on_keypress)
        self.bind("<KeyRelease>", self.slot_on_keyrelease)
        self.bind("<ButtonRelease>", self.slot_on_click)
        self.bind("<FocusIn>", self.slot_on_focus_in)
        self.bind("<Return>", self.slot_on_key_return)
        self.bind("<Tab>", self.slot_on_key_tab)
        self.bind("<Control-Return>", self.slot_on_key_ctrl_return)
        self.bind("<Control-a>", self.slot_on_select_all)
        self.bind("<Control-A>", self.slot_on_select_all)
        self.bind("<Delete>", self.slot_on_key_delete)
        self.bind("<Control-Delete>", self.slot_on_key_ctrl_delete)
        self.bind("<BackSpace>", self.slot_on_key_delete)
        self.bind("<Control-BackSpace>", self.slot_on_key_ctrl_backspace)
        self.bind("<KeyRelease-Delete>", self.slot_on_keyup_delete)
        self.bind("<KeyRelease-BackSpace>", self.slot_on_keyup_delete)
    # end def


    def clear_text (self, *args, **kw):
        """
            event handler for clearing up text widget;
        """
        # clear text
        self.delete("1.0", "end")
        self.edit_reset()
    # end def


    def create_element_line (self, element_tag, index=None):
        """
            inserts a new element-formatted line at @index;
            inserts at insertion point if @index omitted;
        """
        # inits
        index = self.index(
            "{} linestart + 1 line".format(index or TK.INSERT)
        )
        # got element tag?
        if element_tag in self.ELEMENT:
            # got some preprocessing?
            self.switch_to_method(
                "manage_line_{}".format(self.get_line_tag())
            )
            # switch to specific method
            return self.switch_to_method(
                "create_element_line_{}".format(element_tag),
                element_tag, index
            )
        # end if
    # end def


    def create_element_line_action (self, tag, index):
        """
            creates a new line of 'action' element type;
        """
        # simply insert new line
        self.insert_new_line(tag, index)
    # end def


    def create_element_line_character (self, tag, index):
        """
            creates a new line of 'character' element type;
        """
        # simply insert new line
        self.insert_new_line(tag, index)
    # end def


    def create_element_line_dialogue (self, tag, index):
        """
            creates a new line of 'dialogue' element type;
        """
        # simply insert new line
        self.insert_new_line(tag, index)
    # end def


    def create_element_line_parenthetical (self, tag, index):
        """
            creates a new line of 'parenthetical' element type;
        """
        # simply insert new line
        self.insert_new_line(tag, index)
        # insert parenthesis
        self.insert(index, "()", (tag,))
        # put cursor
        self.move_cursor("{}+1c".format(index))
    # end def


    def create_element_line_scene (self, tag, index):
        """
            creates a new line of 'scene' element type;
        """
        # simply insert new line
        self.insert_new_line(tag, index)
    # end def


    def create_element_line_transition (self, tag, index):
        """
            creates a new line of 'transition' element type;
        """
        # simply insert new line
        self.insert_new_line(tag, index)
    # end def


    def file_setup (self, fname, archive):
        """
            sets up widget along with all files/contents in @fname and
            @archive;
        """
        # inits
        _get_fc = lambda k: archive.read(fname[k]).decode("UTF-8")
        # reset widget
        self.reset()
        # put text
        self.insert("1.0", _get_fc("text").rstrip())
        # put elements
        self.reset_elements(json.loads(_get_fc("elements")))
        # put tags
        _tags = json.loads(_get_fc("tags"))
        # browse items
        for _index, _tag in enumerate(_tags):
            # reset tag at correct indices
            self.tag_add(
                _tag, float(_index + 1), float(_index + 2)
            )
        # end for
        # move insertion cursor
        self.move_cursor("1.0")
        # update line data
        self.update_line()
    # end def


    def get_all_lines_range (self):
        """
            returns range() object for all lines in widget;
        """
        return range(1, 1 + self.get_nb_of_lines())
    # end def


    def get_column_index (self, index=None):
        """
            retrieves column index as integer for @index location;
        """
        # inits
        index = self.index(index or TK.INSERT)
        # return integer
        return tools.ensure_int(index.split(".")[-1])
    # end def


    def get_element_mappings (self, index=None):
        """
            returns dict() of hotkey/element mappings along with
            inserted chars in @index line;
        """
        # inits
        index = index or TK.INSERT
        _tag = self.get_line_tag(index)
        # got element tag?
        if _tag in self.ELEMENT:
            # inits
            _element = self.ELEMENT[_tag]
            # got inserted chars?
            if self.inserted_chars(index):
                # init values
                _map = {
                    "tag": _tag,
                    "tab": _element.get("on_tab") or "",
                    "tab_switch": "",
                    "return": _element.get("on_return") or "",
                    "ctrl_return": _element.get("ctrl_return") or "",
                    "ctrl_switch": "",
                }
            # virgin line
            else:
                # init values
                _map = {
                    "tag": _tag,
                    "tab": "",
                    "tab_switch": _element.get("tab_switch") or "",
                    "return": "",
                    "ctrl_return": "",
                    "ctrl_switch": _element.get("ctrl_switch") or "",
                }
            # end if
            # return mappings
            return _map
        # end if
    # end def


    def get_fc_tags (self):
        """
            returns file contents for tags in widget;
        """
        # inits
        _tags = list()
        # browse widget lines
        for _line in self.get_all_lines_range():
            # inits
            _tn = self.tag_names(float(_line))
            # got tag names?
            if _tn:
                # add to list
                _tags.append(_tn[0])
            # end if
        # end for
        # return file contents as JSON string dump
        return json.dumps(_tags)
    # end def


    def get_file_contents (self, fname):
        """
            returns file(s) contents;
        """
        # always return a dict
        return {
            fname["text"]: self.get("1.0", TK.END),
            fname["tags"]: self.get_fc_tags(),
            fname["elements"]: json.dumps(self.ELEMENT),
        }
    # end def


    def get_label (self, element_tag):
        """
            returns label text corresponding to @element_tag;
            returns an empty string otherwise;
        """
        # inits
        _element = self.ELEMENT.get(element_tag) or dict()
        # return result
        return _element.get("label") or ""
    # end def


    def get_line_contents (self, index=None):
        """
            retrieves line text contents at @index or insertion cursor,
            if omitted;
        """
        # inits
        index = index or TK.INSERT
        # return contents
        return self.get(
            "{} linestart".format(index), "{} lineend".format(index)
        )
    # end def


    def get_line_number (self, index=None):
        """
            retrieves line number at @index or insertion cursor,
            if omitted;
        """
        # inits
        index = index or TK.INSERT
        # return result
        return tools.ensure_int(
            self.index("{} linestart".format(index))
        )
    # end def


    def get_line_tag (self, index=None, strict=False):
        """
            retrieves @index line tag, if given; retrieves insertion
            cursor line tag, if @index omitted; returns
            self.current_tag if @strict=False and no previous tag
            found; returns None otherwise;
        """
        # get tags at line start
        index = "{} linestart".format(index or TK.INSERT)
        _tags = self.tag_names(index)
        # got element tag?
        if _tags and _tags[0] in self.ELEMENT:
            return _tags[0]
        # end if
        # allow default value?
        if not strict:
            # return current available tag
            return self.current_tag
        # end if
    # end def


    def get_lines (self, element_tag):
        """
            retrieves dict() of line numbers, texts where @element_tag
            resides plus line number of current insertion cursor;
        """
        # inits
        _lines = []
        _texts = []
        _count = 1
        # browse all lines
        for _line in self.get_all_lines_range():
            # init index
            _index = float(_line)
            # get line tag
            _tag = self.get_line_tag(_index, strict=True)
            # line tag matches up?
            if _tag == element_tag:
                # add line number
                _lines.append(_line)
                # add text contents
                _texts.append(
                    "#{} {}"
                    .format(_count, self.get_line_contents(_index))
                )
                # update counter
                _count += 1
            # end if
        # end for
        # return results
        return {
            "current": self.get_line_number(),
            "lines": _lines,
            "texts": _texts,
        }
    # end def


    def get_nb_of_lines (self):
        """
            retrieves total nb of lines in widget;
        """
        return self.get_line_number(TK.END) - 1
    # end def


    def get_word (self, index=None):
        """
            retrieves word located at or around @index, if any.
        """
        # inits
        index = index or TK.INSERT
        _start = "{} linestart".format(index)
        _end = "{} lineend".format(index)
        _word = ""
        # look backward
        _text = self.get(_start, index)
        _pos = _text.rfind(" ")
        # found?
        if _pos >= 0:
            # set first part of word
            _word += _text[_pos + 1:]
            # update start index
            _start = "{}+{}c".format(_start, _pos + 1)
        else:
            # take all
            _word += _text
        # end if
        # look forward
        _text = self.get(index, _end)
        _pos = _text.find(" ")
        # found?
        if _pos >= 0:
            # set last part of word
            _word += _text[:_pos]
            # update end index
            _end = "{}+{}c".format(_start, _pos)
        else:
            # take all
            _word += _text
        # end if
        # return result
        return {
            "word": _word.rstrip(" .:,;?!\"']})"),
            "start_index": _start,
            "end_index": _end,
        }
    # end def


    def init_deferred (self, kw):
        """
            deferred inits;
        """
        # first time init
        self.reset()
        # event bindings
        self.bind_events(**kw)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.current_tag = self.DEFAULT_TAG
        self.reset_elements(self.ELEMENT_DEFAULTS.copy())
    # end def


    def init_styles (self, **kw):
        """
            tag styles inits;
        """
        # browse elements
        for _tag, _element in self.ELEMENT.items():
            # inits
            _config = _element.get("config")
            # got tag configuration?
            if _config:
                # delete tag first
                self.tag_delete(_tag)
                # reset config
                self.tag_configure(_tag, **_config)
            # end if
        # end for
        # configure selection tag
        self.tag_configure(
            TK.SEL, background="grey30", foreground="white"
        )
        # selection tag should always be upon all others
        self.tag_raise(TK.SEL)
    # end def


    def init_widget (self, **kw):
        r"""
            virtual method to be implemented in subclass;
        """
        # deferred inits
        self.after_idle(self.init_deferred, kw)
    # end def


    def insert_new_line (self, new_tag, index):
        """
            inserts a new @tag element-formatted line at @index;
        """
        # insert new line
        self.insert("{} lineend".format(TK.INSERT), "\n")
        # move to index location
        self.move_cursor(index)
        # remove previous tag
        self.tag_remove(self.tag_names(TK.INSERT), *self.INS_LINE)
        # set new tag instead
        self.tag_add(new_tag, *self.INS_LINE)
        # notify app
        self.events.raise_event("Project:Modified")
    # end def


    def inserted_chars (self, index=None):
        """
            returns True if chars have been inserted in @index line;
            returns False otherwise;
        """
        # inits
        index = index or TK.INSERT
        _chars = self.get(
            "{} linestart".format(index),
            "{} linestart + 1 line".format(index)
        ).strip("\n\t")
        _tag = self.get_line_tag(index)
        # special case
        if _tag == "parenthetical":
            # inserted if different than '()'
            return bool(len(_chars) > 2)
        # default case
        else:
            # inserted if not empty
            return bool(_chars)
        # end if
    # end def


    def line_selected (self, index=None):
        """
            returns True if line at @index is currently selected;
        """
        # inits
        _line = self.get_line_number(index)
        # try out
        try:
            _sel = self.get_line_number(TK.SEL_FIRST)
        except:
            return False
        else:
            return bool(_line == _sel)
        # end try
    # end def


    def manage_line (self, create_key, switch_key):
        """
            determines whether to create/switch line at insertion
            cursor index;
        """
        # inits
        _map = self.get_element_mappings()
        # got mappings?
        if _map:
            # show insertion cursor
            self.after_idle(self.see, TK.INSERT)
            # allowed to create line?
            if _map.get(create_key):
                # create new line
                self.create_element_line(_map.get(create_key))
            # switch current line?
            elif _map.get(switch_key):
                # switch new tag
                self.switch_line(new_tag=_map.get(switch_key))
            # end if
        # end if
        # break the tkevent chain
        return "break"
    # end def


    def manage_line_action (self):
        """
            does some preprocessing for the current line element tag
            before creating a new line;
        """
        # nothing for this element tag
        pass
    # end def


    def manage_line_character (self):
        """
            does some preprocessing for the current line element tag
            before creating a new line;
        """
        # inits
        _name = self.get_line_contents()
        # got character name?
        if _name:
            # notify app
            self.events.raise_event(
                "Scenario:Character:Name:Detected",
                name=_name,
            )
        # end if
    # end def


    def manage_line_dialogue (self):
        """
            does some preprocessing for the current line element tag
            before creating a new line;
        """
        # nothing for this element tag
        pass
    # end def


    def manage_line_parenthetical (self):
        """
            does some preprocessing for the current line element tag
            before creating a new line;
        """
        # nothing for this element tag
        pass
    # end def


    def manage_line_scene (self):
        """
            does some preprocessing for the current line element tag
            before creating a new line;
        """
        # nothing for this element tag
        pass
    # end def


    def manage_line_transition (self):
        """
            does some preprocessing for the current line element tag
            before creating a new line;
        """
        # nothing for this element tag
        pass
    # end def


    def move_cursor (self, index):
        """
            moves insertion cursor programmatically;
        """
        # move insertion cursor
        self.mark_set(TK.INSERT, index)
    # end def


    def reformat_line (self, *args, **kw):
        """
            event handler: reformats insertion cursor's line in order
            to match element tag constraints;
        """
        # deferred task (after idle tasks)
        self.after_idle(self._do_reformat_line, args, kw)
    # end def


    def reformat_line_action (self, text):
        """
            reformats current line along with element constraints;
        """
        # reset to standard line of text
        return (text.strip("()"), "")
    # end def


    def reformat_line_character (self, text):
        """
            reformats current line along with element constraints;
        """
        # same as SCENE
        return self.reformat_line_scene(text)
    # end def


    def reformat_line_dialogue (self, text):
        """
            reformats current line along with element constraints;
        """
        # same as ACTION
        return self.reformat_line_action(text)
    # end def


    def reformat_line_parenthetical (self, text):
        """
            reformats current line along with element constraints;
        """
        # ensure parenthetical
        return ("({})".format(text.strip("()")), "+1c")
    # end def


    def reformat_line_scene (self, text):
        """
            reformats current line along with element constraints;
        """
        # ensure upper case
        return (text.strip("()").upper(), "")
    # end def


    def reformat_line_transition (self, text):
        """
            reformats current line along with element constraints;
        """
        # same as SCENE
        return self.reformat_line_scene(text)
    # end def


    def replace_text (self, text, start=None, end=None, smart_delete=False, keep_cursor=False):
        """
            replaces text segment found between @start and @end by
            @text contents;
        """
        # inits
        start = start or TK.INSERT
        end = end or TK.INSERT
        # keep cursor
        _cursor = self.index(TK.INSERT)
        # keep tags
        _tags = tuple(set(self.tag_names(start) + self.tag_names(end)))
        # asked for smart deletion?
        if smart_delete:
            # inits
            _endl = "{} lineend".format(end)
            _text = self.get(end, _endl)
            # search for a non-alphabetical char
            _found = re.search(r"[^\w\-]", _text)
            # found word separator?
            if _found:
                # update end index
                end = "{} +{}c".format(end, _found.start())
            # not found?
            else:
                # expand to line end
                end = _endl
            # end if
        # end if
        # remove old text
        self.delete(start, end)
        # insert new text
        self.insert(start, text, _tags)
        # asked to keep cursor?
        if keep_cursor:
            # reset cursor location
            self.move_cursor(_cursor)
        # end if
        # notify app
        self.events.raise_event("Project:Modified")
    # end def


    def reset (self, *args, **kw):
        """
            resets text to new;
        """
        # clear text
        self.clear_text(**kw)
        # reset members
        self.init_members(**kw)
        # update line infos (deferred)
        self.update_line(**kw)
    # end def


    def reset_elements (self, new_dict):
        """
            resets self.ELEMENT dictionary with @new_dict;
        """
        if tools.is_pdict(new_dict):
            # reset dict
            self.ELEMENT = new_dict
            # reset configs
            self.init_styles()
            # notify app
            self.events.raise_event(
                "Scenario:Elements:Init",
                elements=tuple(sorted(self.ELEMENT))
            )
        # end if
    # end def


    def slot_keypress_action (self, event=None, *args, **kw):
        """
            event handler: on 'action' element key press;
        """
        # notify app
        if event.char and not (event.state & 0x8c):
            # inits
            _ins = TK.INSERT
            # need to capitalize first word of sentence?
            if self.compare(_ins, "==", self.INS_LINE[0]) or \
                    self.get("{}-2c".format(_ins), _ins) in \
                                                    (". ", "! ", "? "):
                # same as SCENE
                return self.slot_keypress_scene(event, *args, **kw)
            # end if
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def slot_keypress_character (self, event=None, *args, **kw):
        """
            event handler: on 'character' element key press;
        """
        # same as SCENE
        return self.slot_keypress_scene(event, *args, **kw)
    # end def


    def slot_keypress_dialogue (self, event=None, *args, **kw):
        """
            event handler: on 'dialogue' element key press;
        """
        # same as ACTION
        return self.slot_keypress_action(event)
    # end def


    def slot_keypress_parenthetical (self, event=None, *args, **kw):
        """
            event handler: on 'parenthetical' element key press;
        """
        # same as ACTION
        return self.slot_keypress_action(event)
    # end def


    def slot_keypress_scene (self, event=None, *args, **kw):
        """
            event handler: on 'scene' element key press;
        """
        # inits
        _char = event.char
        _modifiers = (event.state & 0x8c)
        # letter char?
        if _char and ord(_char) > 31 and not _modifiers:
            try:
                # delete previous selected
                self.delete(TK.SEL_FIRST, TK.SEL_LAST)
            except:
                pass
            # end try
            # set to uppercase
            self.insert(
                TK.INSERT, _char.upper(), self.tag_names(TK.INSERT)
            )
            # notify app
            self.events.raise_event("Project:Modified")
            # break the tkevent chain
            return "break"
        # end if
    # end def


    def slot_keypress_transition (self, event=None, *args, **kw):
        """
            event handler: on 'transition' element key press;
        """
        # same as SCENE
        return self.slot_keypress_scene(event, *args, **kw)
    # end def


    def slot_on_click (self, event=None, *args, **kw):
        """
            event handler: mouse click;
        """
        # update line infos (deferred)
        self.update_line()
        # notify app
        self.events.raise_event("Scenario:Text:Clicked", event=event)
    # end def


    def slot_on_focus_in (self, event=None, *args, **kw):
        """
            event handler: widget got focused;
        """
        # update line infos (deferred)
        self.update_line()
        # notify app
        self.events.raise_event("Scenario:Text:FocusedIn", event=event)
    # end def


    def slot_on_key_ctrl_backspace (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-BackSpace> key press;
        """
        # get contents
        _start = self.index("{} linestart".format(TK.INSERT))
        _text = self.get(_start, TK.INSERT)
        # try to find a white space
        _pos = _text.rfind(" ")
        # got one?
        if _pos >= 0:
            # reset index
            _start = self.index("{}+{}c".format(_start, _pos))
        # end if
        # remove a word at once
        self.delete(_start, TK.INSERT)
        # update line infos (deferred)
        self.update_line()
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_key_ctrl_delete (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-Delete> key press;
        """
        # get contents
        _end = self.index("{} lineend".format(TK.INSERT))
        _text = self.get(TK.INSERT, _end)
        # try to find a white space
        _pos = _text.find(" ")
        # got one?
        if _pos >= 0:
            # reset index
            _end = self.index("{}+{}c".format(TK.INSERT, _pos + 1))
        # end if
        # remove a word at once
        self.delete(TK.INSERT, _end)
        # update line infos (deferred)
        self.update_line()
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_key_ctrl_return (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-Return> key press;
        """
        # manage line (create/switch)
        return self.manage_line("ctrl_return", "ctrl_switch")
    # end def


    def slot_on_key_delete (self, event=None, *args, **kw):
        """
            event handler: on <Del> key press;
        """
        # same as KEYRELEASE
        self.slot_on_keyrelease(event)
        # ensure line format (deferred)
        self.reformat_line(no_adjust=True)
    # end def


    def slot_on_key_return (self, event=None, *args, **kw):
        """
            event handler: on <Return> key press;
        """
        # manage line (create/switch)
        return self.manage_line("return", "return_switch")
    # end def


    def slot_on_key_tab (self, event=None, *args, **kw):
        """
            event handler: on <Tab> key press;
        """
        # manage line (create/switch)
        return self.manage_line("tab", "tab_switch")
    # end def


    def slot_on_keypress (self, event=None, *args, **kw):
        """
            event handler: general keyboard key press;
        """
        # param controls
        if event.keysym not in self.DEAD_KEYS:
            # update line infos (deferred)
            self.update_line()
        # end if
        # show insertion cursor
        self.see(TK.INSERT)
        # switch to specific method
        return self.switch_to_method(
            "slot_keypress_{}".format(self.get_line_tag()), event
        )
    # end def


    def slot_on_keyrelease (self, event=None, *args, **kw):
        """
            event handler: general keyboard key release;
        """
        # param controls
        if event.keysym not in self.DEAD_KEYS:
            # update line infos (deferred)
            self.update_line()
        # end if
    # end def


    def slot_on_keyup_delete (self, event=None, *args, **kw):
        """
            event handler: on <Del> key release;
        """
        # text area is empty?
        if len(self.get("1.0", "3.0")) < 2:
            # reset widget
            self.reset()
        # end if
        # notify app
        self.events.raise_event("Project:Modified")
    # end def


    def slot_on_select_all (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-A> key press;
        """
        # select only current line
        self.tag_add(TK.SEL, *self.INS_LINE)
        # not all widget's contents
        # break the tkevent chain
        return "break"
    # end def


    def switch_line (self, *args, new_tag=None, **kw):
        """
            event handler: switches current insertion line to @new_tag
            element constraints;
        """
        # switch tag for current line
        self.update_line(force_tag=new_tag)
        # ensure line format (deferred)
        self.reformat_line()
        # notify app
        self.events.raise_event("Project:Modified")
    # end def


    def switch_to_method (self, method_name, *args, **kw):
        """
            calls inner class method by @method_name string value and
            returns method's retvalue, if exists; returns None
            otherwise;
        """
        # param controls
        if method_name:
            # inits
            _method = getattr(self, method_name, None)
            # callable?
            if callable(_method):
                # call with args and get retvalue
                return _method(*args, **kw)
            # debugging
            else:
                # notify dev
                raise AttributeError(
                    _("[WARNING]\tUnable to call method: '{method}()'")
                    .format(method=method_name)
                )
            # end if
        # end if
        # failed
        return None
    # end def


    def update_current_tag (self, *args, index=None, **kw):
        """
            event handler: updates current line tag pointer;
        """
        # inits
        _tag = kw.get("force_tag") or self.get_line_tag(index)
        # got element tag?
        if _tag in self.ELEMENT:
            # update current tag
            self.current_tag = _tag
        # end if
        # return last available tag
        return self.current_tag
    # end def


    def update_line (self, *args, **kw):
        """
            event handler: updates line contents in order to keep it
            correctly up-to-date;
        """
        # deferred task (after idle tasks)
        self.after_idle(self._do_update_line, args, kw)
    # end def

# end class ScenarioText
