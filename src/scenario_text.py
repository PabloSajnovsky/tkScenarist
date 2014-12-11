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
import string
import tkinter as TK
import tkRAD.widgets.rad_widget_base as RW
from tkRAD.core import tools


class ScenarioText (RW.RADWidgetBase, TK.Text):
    """
        Scenario-specific text widget class;
    """

    # class constant defs
    CONFIG = {
        "autoseparators": False, # useless: private undo/redo maechanism
        "background": "white",
        "font": "monospace 12",
        "foreground": "black",
        "highlightthickness": 1,
        "undo": True,
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
            "on_return_create": "action",
            "on_tab_create": "character",
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
            "on_return_create": "dialogue",
            "on_tab_create": "parenthetical",
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
            "on_return_create": "character",
            "on_tab_create": "action",
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
            "on_return_create": "dialogue",
            "on_tab_create": "dialogue",
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
            "on_return_create": "action",
            "on_tab_create": "character",
            "tab_switch": "action",
            "ctrl_return": "transition",
        },
        "transition": {
            "label": _("Transition"),
            "config": {
                "justify": "right",
                "rmargin": "10",
            },
            "on_return_create": "scene",
            "on_tab_create": "transition",
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

    # characters generating undo/redo stack separators
    SEPARATORS = string.whitespace + string.punctuation

    # allowed nb of cancellations
    UNDO_LIMIT = 2000


    def __init__ (self, master=None, **kw):
        # default values
        self.CONFIG = self.CONFIG.copy()
        self.CONFIG.update(kw)
        # super inits
        TK.Text.__init__(self, master)
        self.configure(**self._only_tk(self.CONFIG))
        RW.RADWidgetBase.__init__(self, master, **self.CONFIG)
    # end def


    def _do_delete (self, index1, index2=None):
        """
            standard method reimplementation;
        """
        # super class delegate
        super().delete(index1, index2)
        # update line infos (deferred)
        self.update_line()
        # hook method
        self.update_modified()
    # end def


    def _do_insert (self, index, chars, *args):
        """
            standard method reimplementation;
        """
        # super class delegate
        super().insert(index, chars, *args)
        # update line infos (deferred)
        self.update_line()
        # hook method
        self.update_modified()
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Scenario:Switch:Line": self.switch_line,
                "Scenario:Settings:Update": self.slot_update_settings,
            }
        )
        # tkinter event bindings
        """
            CAUTION:
            self.tag_bind() triggers event only when mouse pointer
            is *OVER* tag's region - WTF? /!\
            we have to work with classical hotkeys
        """
        self.bind("<Key>", self.slot_on_keypress)
        #~ self.bind("<KeyRelease>", self.slot_on_keyrelease)
        self.bind("<ButtonRelease>", self.slot_on_click)
        self.bind("<FocusIn>", self.slot_on_focus_in)
        self.bind("<Tab>", self.slot_on_key_tab)
        self.bind("<Return>", self.slot_on_key_return)
        self.bind("<Control-Return>", self.slot_on_key_ctrl_return)
        self.bind("<Control-a>", self.slot_on_select_all)
        self.bind("<Control-A>", self.slot_on_select_all)
        self.bind("<Control-z>", self.slot_edit_undo)
        self.bind("<Control-Z>", self.slot_edit_redo)
        self.bind("<Delete>", self.slot_on_key_delete)
        #~ self.bind("<KeyRelease-Delete>", self.slot_on_keyup_delete)
        self.bind("<Control-Delete>", self.slot_on_key_ctrl_delete)
        self.bind("<BackSpace>", self.slot_on_key_backspace)
        #~ self.bind("<KeyRelease-BackSpace>", self.slot_on_keyup_delete)
        self.bind("<Control-BackSpace>", self.slot_on_key_ctrl_backspace)
    # end def


    def clear_text (self, *args, **kw):
        """
            event handler for clearing up text widget;
        """
        # clear text
        self.delete("1.0", TK.END)
        self.edit_reset()
    # end def


    def create_element_line (self, element_tag, index=None):
        """
            inserts a new @element_tag formatted line at @index;
            inserts at insertion point if @index omitted;
        """
        # inits
        index = self.index(
            "{} linestart + 1 line".format(index or TK.INSERT)
        )
        # got element tag?
        if element_tag in self.ELEMENT:
            # try out
            try:
                # got some preprocessing?
                self.switch_to_method(
                    "manage_line_{}".format(self.get_line_tag())
                )
            # fallback - default behaviour
            except AttributeError:
                # nothing to do out there
                pass
            # end try
            # try out
            try:
                # switch to specific line creation
                return self.switch_to_method(
                    "create_element_line_{}".format(element_tag),
                    element_tag, index
                )
            # fallback - default behaviour
            except AttributeError:
                # simply insert new line
                return self.insert_new_line(element_tag, index)
            # end try
        # end if
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


    def delete (self, index1, index2=None):
        """
            standard method reimplementation;
        """
        # allowed to undo/redo?
        if self.undo_enabled():
            # private undo stack management
            self.undo_stack.push_delete(
                self.index(index1),
                *self.get_tagged_text(index1, index2)
            )
            # try out
            try:
                # do delete
                self._do_delete(index1, index2)
            # got error
            except:
                # remove stacking
                self.undo_stack.pop()
                raise
            # end try
        # no undo/redo management
        else:
            # simply delete
            self._do_delete(index1, index2)
        # end if
    # end def


    def delete_selection (self, *args, **kw):
        """
            event handler: deletes eventual selected portion of text;
            returns True on success, False otherwise;
        """
        # try out selection
        try:
            self.delete(TK.SEL_FIRST, TK.SEL_LAST)
            return True
        except:
            return False
        # end try
    # end def


    def edit_redo (self):
        """
            standard method reimplementation;
        """
        # allowed to undo/redo?
        if self.undo_enabled():
            # inits
            _sequence = self.undo_stack.get_redo_elements()
            _index = None
            # browse elements
            for _element in _sequence:
                # element has been inserted?
                if _element.mode == "+":
                    # insert it again
                    self._do_insert(
                        _element.start_index, *_element.args
                    )
                    # update index
                    _index = _element.end_index
                # element has been deleted?
                else:
                    # remove it
                    self._do_delete(
                        _element.start_index, _element.end_index
                    )
                    # update index
                    _index = _element.start_index
                # end if
            # end for
            # got position?
            if _index:
                # reset cursor pos
                self.move_cursor(_index)
                self.after_idle(self.see, TK.INSERT)
            # end if
        # end if
    # end def


    def edit_reset (self):
        """
            standard method reimplementation;
        """
        # super class delegate
        super().edit_reset()
        # private undo stack management
        self.undo_stack.reset()
    # end def


    def edit_separator (self):
        """
            standard method reimplementation;
        """
        # allowed to undo/redo?
        if self.undo_enabled():
            # private undo stack management
            self.undo_stack.add_separator()
        # end if
    # end def


    def edit_undo (self):
        """
            standard method reimplementation;
        """
        # allowed to undo/redo?
        if self.undo_enabled():
            # inits
            _sequence = self.undo_stack.get_undo_elements()
            _index = None
            # browse elements
            for _element in _sequence:
                # element has been inserted?
                if _element.mode == "+":
                    # remove it
                    self._do_delete(
                        _element.start_index, _element.end_index
                    )
                    # update index
                    _index = _element.start_index
                # element has been deleted?
                else:
                    # insert it again
                    self._do_insert(
                        _element.start_index, *_element.args
                    )
                    # update index
                    _index = _element.end_index
                # end if
            # end for
            # got position?
            if _index:
                # reset cursor pos
                self.move_cursor(_index)
                self.after_idle(self.see, TK.INSERT)
            # end if
        # end if
    # end def


    def file_setup (self, fname, archive):
        """
            sets up widget along with all files/contents in @fname and
            @archive;
        """
        # inits
        _get_fc = lambda k: archive.read(fname[k]).decode(ENCODING)
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
        # clear undo/redo stack
        self.edit_reset()
        # move insertion cursor
        self.move_cursor("1.0")
        # update line data
        self.update_line()
        # open file is *NOT* a modified project
        self.update_modified(flag=False)
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
                    "tab": _element.get("on_tab_create") or "",
                    "tab_switch": "",
                    "return": _element.get("on_return_create") or "",
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
            resides plus line number of current insertion cursor; this
            method is implemented to be ready-to-use for a scene
            browser listbox widget;
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


    def get_options_element (self):
        """
            retrieves RC file element settings or ELEMENT_DEFAULTS if
            not found;
        """
        return json.loads(
            self.options.get(
                self.get_rc_section(), "text_settings", fallback="[]"
            )
        ) or self.ELEMENT_DEFAULTS
    # end def


    def get_rc_section (self):
        """
            retrieves RC file section name for this class;
        """
        return self.classname().lower()
    # end def


    def get_tagged_text (self, index1, index2=None):
        """
            retrieves tuple sequence of chars, tags, chars, tags, ...
            for text found between @index1 and @index2;
        """
        # inits
        index1 = index1 or TK.INSERT
        index2 = index2 or TK.INSERT
        # inline text?
        if self.get_line_number(index1) == self.get_line_number(index2):
            # simple structure
            return (self.get(index1, index2), self.tag_names(index1))
        # multiple line selection
        else:
            # inits
            _index = index1
            _tags = self.tag_names(_index)
            _args = []
            # loop till reached
            while self.compare(_index, "<", index2):
                # inits
                _tn = self.tag_names(_index)
                # got a change?
                if _tn != _tags:
                    # add chars
                    _args.append(self.get(index1, _index))
                    # add tags
                    _args.append(_tags)
                    # update index
                    index1 = _index
                    # update tags
                    _tags = _tn
                # end if
                # next char
                _index = self.index("{}+1c".format(_index))
            # end while
            # last section
            _args.append(self.get(index1, index2))
            _args.append(self.tag_names(index1))
            # return results
            return tuple(_args)
        # end if
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


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.current_tag = self.DEFAULT_TAG
        self.reset_elements(self.get_options_element())
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
        # member inits
        self.undo_stack = TextUndoStack(limit=self.UNDO_LIMIT)
        # deferred task def
        def deferred ():
            # first time init
            self.reset(**kw)
            # event bindings
            self.bind_events(**kw)
        # end def
        # deferred inits
        self.after_idle(deferred)
    # end def


    def insert (self, index, chars, *args):
        """
            standard method reimplementation;
        """
        # allowed to undo/redo?
        if self.undo_enabled():
            # private undo stack management
            self.undo_stack.push_insert(self.index(index), chars, *args)
        # end if
        # do insert
        self._do_insert(index, chars, *args)
    # end def


    def insert_new_line (self, new_tag, index):
        """
            inserts a new @tag element-formatted line at @index;
        """
        # no current selection to delete?
        if not self.delete_selection():
            # insert new line
            self.edit_separator()
            self.insert("{} lineend".format(TK.INSERT), "\n")
            # move to index location
            self.move_cursor(index)
            # remove previous tag
            self.tag_remove(self.tag_names(TK.INSERT), *self.INS_LINE)
            # set new tag instead
            self.tag_add(new_tag, *self.INS_LINE)
        # end if
    # end def


    def inserted_chars (self, index=None):
        """
            returns True if chars have been inserted in @index line;
            returns False otherwise;
        """
        # inits
        index = index or TK.INSERT
        _chars = self.get_line_contents(index).strip("\n\t")
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


    def key_filter (self, event, use_filter=None):
        """
            keyboard keypress filter; parameter @use_filter admits
            'upper', 'lower', 'capitalize', callable(event) or None;
        """
        # inits
        _char = event.char
        _modifiers = (event.state & 0x8c)
        # letter char?
        if _char and ord(_char) > 31 and not _modifiers:
            # delete eventual selection
            self.delete_selection()
            # should use filter?
            if use_filter:
                # callable?
                if callable(use_filter):
                    # reset char
                    _char = use_filter(event)
                # set to uppercase?
                elif use_filter.startswith("up"):
                    # reset char
                    _char = _char.upper()
                # set to lowercase?
                elif use_filter.startswith("low"):
                    # reset char
                    _char = _char.lower()
                # should capitalize first word?
                elif use_filter.startswith("cap"):
                    # inits
                    _ins = TK.INSERT
                    # need to capitalize first word of sentence?
                    if self.compare(_ins, "==", self.INS_LINE[0]) or \
                            self.get("{}-2c".format(_ins), _ins) in \
                                                    (". ", "! ", "? "):
                        # reset char
                        _char = _char.upper()
                    # end if
                # end if
            # end if
            # insert char (with undo/redo features)
            self.insert(
                TK.INSERT, _char, self.get_line_tag()
            )
            # break the tkevent chain by now
            return "break"
        # end if
        # do *NOT* break the tkevent chain here
        return None
    # end def


    def line_selected (self, index=None):
        """
            returns True if line at @index is currently into a
            selection range or have some selection in it;
        """
        # inits
        _line = self.get_line_number(index)
        # try out
        try:
            _first = self.get_line_number(TK.SEL_FIRST)
            _last = self.get_line_number(TK.SEL_LAST)
        except:
            return False
        else:
            return bool(_line in (_first, _last))
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


    def manage_line_character (self):
        """
            this method is used by self.create_element_line();
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
            deferred task (after idle);
        """
        def deferred ():
            # inits
            _tag = self.update_current_tag(TK.INSERT)
            _text = self.get(*self.INS_LINE_END)
            _cursor = self.index(TK.INSERT)
            # reformat along with element tag constraints
            _text, _adjust = self.switch_to_method(
                "reformat_line_{}".format(_tag), _text
            )
            # reset text (apart from undo/redo maechanism)
            self._do_delete(*self.INS_LINE_END)
            self._do_insert(self.INS_LINE_END[0], _text, _tag)
            # should keep cursor pos?
            if kw.get("keep_cursor"):
                _adjust = ""
            # end if
            # reset cursor pos
            self.move_cursor("{} {}".format(_cursor, _adjust))
        # end def
        # deferred task (after idle tasks)
        self.after_idle(deferred)
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


    def replace_text (self, text, start=None, end=None,
                                smart_delete=False, keep_cursor=False):
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
        # reset to new
        self.update_modified(flag=False)
    # end def


    def reset_elements (self, new_dict):
        """
            resets self.ELEMENT dictionary with @new_dict;
        """
        if tools.is_pdict(new_dict):
            # reset dict (weakref)
            self.ELEMENT = new_dict.copy()
            # reset configs
            self.init_styles()
            # notify app
            self.events.raise_event(
                "Scenario:Elements:Init",
                elements=tuple(sorted(self.ELEMENT))
            )
        # end if
    # end def


    def set_options_element (self, e_dict):
        """
            resets RC file element settings with @e_dict contents;
        """
        # param controls
        if tools.is_pdict(e_dict):
            # reset options settings
            _rc = self.get_rc_section()
            self.options[_rc]["text_settings"] = json.dumps(e_dict)
        # end if
    # end def


    def slot_edit_redo (self, event=None, *args, **kw):
        """
            event handler: edit > redo;
        """
        # redo entries
        self.edit_redo()
        # break the tkevent chain
        return "break"
    # end def


    def slot_edit_undo (self, event=None, *args, **kw):
        """
            event handler: edit > undo;
        """
        # undo entries
        self.edit_undo()
        # break the tkevent chain
        return "break"
    # end def


    def slot_keypress_action (self, event=None, *args, **kw):
        """
            event handler: on 'action' element key press;
        """
        # use key filter (with undo/redo features)
        return self.key_filter(event, use_filter="capitalize")
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
        # use key filter
        return self.key_filter(event, use_filter="upper")
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


    def slot_on_key_backspace (self, event=None, *args, **kw):
        """
            event handler: on <BackSpace> key press;
        """
        # ensure line format (deferred)
        self.reformat_line(keep_cursor=True)
        # no selection to delete?
        if not self.delete_selection():
            # delete char (undo/redo feature support)
            self.delete("{}-1c".format(TK.INSERT))
        # end if
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_key_ctrl_backspace (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-BackSpace> key press;
        """
        # no current selection to delete?
        if not self.delete_selection():
            # get contents
            _start = self.index(self.INS_LINE_END[0])
            _text = self.get(_start, TK.INSERT)
            # try to find a white space (backward)
            _pos = _text.rfind(" ")
            # got one?
            if _pos >= 0:
                # reset index
                _start = self.index("{}+{}c".format(_start, _pos))
            # end if
            # remove word at once
            self.delete(_start, TK.INSERT)
        # end if
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_key_ctrl_delete (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-Delete> key press;
        """
        # no current selection to delete?
        if not self.delete_selection():
            # get contents
            _end = self.index(self.INS_LINE_END[-1])
            _text = self.get(TK.INSERT, _end)
            # try to find a white space (forward)
            _pos = _text.find(" ")
            # got one?
            if _pos >= 0:
                # reset index
                _end = self.index("{}+{}c".format(TK.INSERT, _pos + 1))
            # end if
            # remove word at once
            self.delete(TK.INSERT, _end)
        # end if
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
        # ensure line format (deferred)
        self.reformat_line(keep_cursor=True)
        # no selection to delete?
        if not self.delete_selection():
            # delete char (undo/redo feature support)
            self.delete(TK.INSERT)
        # end if
        # break the tkevent chain
        return "break"
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
            # show insertion cursor
            self.see(TK.INSERT)
            # keypress is a separator-generate symbol?
            if event.char and event.char in self.SEPARATORS:
                # add undo/redo separator
                self.edit_separator()
            # end if
        # end if
        # switch to specific method
        return self.switch_to_method(
            "slot_keypress_{}".format(self.get_line_tag()), event
        )
    # end def


    #~ def slot_on_keyrelease (self, event=None, *args, **kw):
        #~ """
            #~ event handler: general keyboard key release;
        #~ """
        #~ # no more to do out there
        #~ pass
    #~ # end def


    #~ def slot_on_keyup_delete (self, event=None, *args, **kw):
        #~ """
            #~ event handler: on <Del> key release;
        #~ """
        #~ # text area is empty?
        #~ if len(self.get("1.0", "3.0")) < 2:
            #~ # reset widget
            #~ self.reset()
            #~ # hook method
            #~ self.update_modified()
        #~ # end if
    #~ # end def


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


    def slot_update_settings (self, *args, **kw):
        """
            event handler: settings have been changed;
        """
        # reset project settings (safe)
        self.reset_elements(kw.get("project_settings"))
        # reset global settings
        self.set_options_element(kw.get("global_settings"))
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


    def undo_enabled (self):
        """
            returns True if widget undo feature is enabled, False
            otherwise;
        """
        return bool(self.cget("undo"))
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
            deferred task (after idle);
        """
        def deferred ():
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
        # deferred task (after idle tasks)
        self.after_idle(deferred)
    # end def


    def update_modified (self, *args, flag=True, **kw):
        """
            event handler: updates line contents in order to keep it
            correctly up-to-date;
        """
        # reset internal flag
        self.edit_modified(flag)
        # notify app
        self.events.raise_event("Project:Modified", flag=flag)
    # end def

# end class ScenarioText



class TextUndoStack (list):
    """
        undo/redo stack structure for Text widget;
    """

    # class constant defs
    SEPARATOR = object()

    class Element:

        def __init__ (self, mode, index, *args):
            """
                class constructor;
            """
            # member inits
            self.mode = mode
            self.start_index = index
            self.args = args
        # end def


        def __repr__ (self):
            """
                string format for debugging session;
            """
            return str(self)
        # end def


        def __str__ (self):
            """
                string format for debugging session;
            """
            return "<Element '{}' ({}, {}) {}>".format(
                self.mode, self.start_index, self.end_index, self.args
            )
        # end def


        @property
        def end_index (self):
            """
                read-only property;
                retrieves end index;
            """
            return "{}+{}c".format(self.start_index, self.text_length())
        # end def


        def text_length (self):
            """
                evaluates full text length over all items;
            """
            return sum(map(len, self.args[::2]))
        # end def

    # end class Element


    def __init__ (self, limit=200):
        """
            class constructor;
        """
        # member inits
        self.limit = limit
        self.reset()
    # end def


    def add_separator (self):
        """
            adds a separator to help determine undo/redo element
            sequences;
        """
        # really need to add one?
        if not self or self[-1] is not self.SEPARATOR:
            # add separator
            self.append(self.SEPARATOR)
        # end if
    # end def


    def append (self, element):
        """
            standard method reimplementation;
        """
        # should delete redo sequences?
        if self.current_index >= 0:
            # remove following elements
            del self[self.current_index + 1:]
        # better reset
        else:
            # ensure all is clear
            self.clear()
        # end if
        # undo/redo limitation support
        if self.limit > 1:
            # remove oldest
            del self[:1 - self.limit]
        # special case
        elif self.limit == 1:
            # better clear all (faster)
            self.clear()
        # end if
        # should add separator between elements of different modes?
        if len(self) and hasattr(element, "mode"):
            # inits
            _last = self[-1]
            # is Element of different mode?
            if hasattr(_last, "mode") and _last.mode != element.mode:
                # add separator
                super().append(self.SEPARATOR)
            # end if
        # end if
        # super class delegate
        super().append(element)
        # update index
        self.update_index()
    # end def


    def get_redo_elements (self):
        """
            retrieves all elements in an unique redo sequence list;
        """
        # inits
        _sequence = []
        # move to next redo op
        self.current_index += 1
        # trap separator(s), moving forward
        _ci = self.trap(self.SEPARATOR, +1)
        # got elements to redo?
        if _ci < len(self):
            # should redo all at once?
            if self.SEPARATOR not in self[_ci + 1:]:
                # retrieve all remaining elements
                _sequence = self[_ci:]
                # update index
                self.current_index = len(self) - 1
            # should redo till first encountered separator?
            else:
                # get separator index
                _sep = self[_ci + 1:].index(self.SEPARATOR)
                # retrieve elements
                _sequence = self[_ci:_ci + _sep + 1]
                # update index
                self.current_index = _ci + _sep + 1
            # end if
        # end if
        # rebind index
        self.rebind_index()
        # return results
        return _sequence
    # end def


    def get_undo_elements (self):
        """
            retrieves all elements in an unique undo sequence list;
        """
        # inits
        _sequence = []
        # trap separator(s), moving backward
        _ci = self.trap(self.SEPARATOR, -1)
        # got elements to undo?
        if _ci >= 0:
            # should undo all elements at once?
            if self.SEPARATOR not in self[:_ci]:
                # retrieve all elements
                _sequence = self[:_ci + 1]
                # update index
                self.current_index = -1
            # should undo till last encountered separator?
            else:
                # get separator index
                _sep = self[_ci::-1].index(self.SEPARATOR)
                # retrieve elements
                _sequence = self[_ci - _sep + 1:_ci + 1]
                # update index
                self.current_index = _ci - _sep
            # end if
        # end if
        # return results
        return reversed(_sequence)
    # end def


    def pop (self):
        """
            standard method reimplementation;
            here, pop() does *NOT* admit any parameter;
            poping a stack always implies removing its last element;
            will raise IndexError if poping an empty stack;
        """
        # super class delegate
        super().pop()
        # update index
        self.update_index()
    # end def


    def push_delete (self, index, chars, *args):
        """
            push element on stack with mode 'delete';
            undo inserts, redo deletes;
        """
        # add 'delete' element
        if chars or args:
            self.append(self.Element("-", index, chars, *args))
        # end if
    # end def


    def push_insert (self, index, chars, *args):
        """
            push element on stack with mode 'insert';
            undo deletes, redo inserts;
        """
        # add 'insert' element
        if chars or args:
            self.append(self.Element("+", index, chars, *args))
        # end if
    # end def


    def rebind_index (self):
        """
            rebinds self.current_index into class list limits;
        """
        self.current_index = (
            max(0, min(len(self) - 1, self.current_index))
        )
    # end def


    def reset (self):
        """
            resets all stack members;
        """
        # inits
        self.clear()
        self.update_index()
    # end def


    def trap (self, element, sx=1):
        """
            traps given @element, moving @sx direction/step;
            if @sx < 0, moves backward;
            if @sx > 0, moves forward;
            updates and returns new self.current_index;
        """
        # inits
        _len = len(self)
        _ci = self.current_index
        # param controls
        if sx and 0 <= _ci < _len:
            # loop while element is encountered
            while self[_ci] is element:
                # update index
                _ci += sx
                # out of bound?
                if not (0 <= _ci < _len):
                    # trap out
                    break
                # end if
            # end while
        # end if
        # rebind index
        self.current_index = max(-1, min(_len, _ci))
        # return updated index
        return self.current_index
    # end def


    def update_index (self):
        """
            updates index along with stack length;
        """
        # inits
        self.current_index = len(self) - 1
        # return result
        return self.current_index
    # end def

# end class TextUndoStack
