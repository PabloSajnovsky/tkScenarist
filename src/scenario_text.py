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
import tkinter as TK
import tkRAD.widgets.rad_widget_base as RW


class ScenarioText (RW.RADWidgetBase, TK.Text):
    """
        Scenario-specific text widget class;
    """

    # class constant defs
    CONFIG = {
        "autoseparators": True,
        "background": "white",
        "font": "monospace 12",
        "foreground": "black",
        "highlightthickness": 1,
        "undo": True,
        "wrap": "word",
    }

    DEFAULT_TAG = "scene"

    # NOTICE: element name == element tag
    ELEMENT = {
        "action": {
            "label": _("Action"),
            "config": {
                "spacing1": "10",
            },
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "character",
            "ctrl_return": "character",
        },
        "character": {
            "label": _("Character"),
            "on_return": "dialogue",
            "on_tab": "parenthetical",
            "tab_switch": "action",
            "ctrl_return": "action",
        },
        "dialogue": {
            "label": _("Dialogue"),
            "on_return": "character",
            "on_tab": "action",
            "tab_switch": "parenthetical",
            "ctrl_return": "action",
        },
        "parenthetical": {
            "label": _("Parenthetical"),
            "on_return": "dialogue",
            "on_tab": "action",
            "tab_switch": "character",
            "ctrl_return": "dialogue",
        },
        "scene": {
            "label": _("Scene"),
            "config": {
                "background": "grey90",
            },
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "action",
            "ctrl_return": "transition",
        },
        "transition": {
            "label": _("Transition"),
            "on_return": "scene",
            "on_tab": "transition",
            "tab_switch": "scene",
            "ctrl_return": "character",
        },
    }

    INS_LINE = (
        "{} linestart".format(TK.INSERT),
        "{} linestart + 1 line".format(TK.INSERT),
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


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        #~ self.events.connect_dict(
            #~ {
                #~ "Project:Modified": self.slot_project_modified,
            #~ }
        #~ )
        # tkinter event bindings
        # CAUTION:
        # self.tag_bind() triggers event only when mouse pointer
        # is *OVER* tag's region - WTF? /!\
        # we have to work with a tag dispatcher
        self.bind("<Key>", self.slot_on_keypress)
        self.bind("<KeyRelease>", self.slot_on_keyrelease)
        self.bind("<Return>", self.slot_on_key_return)
        self.bind("<Tab>", self.slot_on_key_tab)
        self.bind("<Control-Return>", self.slot_on_key_ctrl_return)
        self.bind("<Control-a>", self.slot_on_select_all)
        self.bind("<Control-A>", self.slot_on_select_all)
        self.bind("<Delete>", self.slot_on_key_delete)
    # end def


    def clear_text (self, *args, **kw):
        """
            event handler for clearing up text widget;
        """
        # clear text
        self.delete("1.0", "end")
    # end def


    def create_element_line (self, element_tag, index=None):
        """
            inserts a new element-formatted line at @index;
            inserts at insertion point if @index omitted;
        """
        # inits
        index = self.index(
            "{} linestart + 1 line"
            .format(self.index(index or TK.INSERT))
        )
        # got element tag?
        if element_tag in self.ELEMENT:
            # init specific creation method
            print(
                "trying to create new element line '{}' at index '{}'"
                .format(element_tag, index)
            )
            _method = getattr(
                self,
                "create_element_line_{}".format(element_tag),
                None
            )
            if callable(_method):
                # redirect to specific line creation
                return _method(element_tag, index)
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


    def get_line_tag (self, index=None, strict=False):
        """
            retrieves @index line tag, if given; retrieves insertion
            point line tag, if @index omitted; returns self.current_tag
            if @strict=False and no previous tag found; returns None
            otherwise;
        """
        # inits
        index = index or TK.INSERT
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
                    "tab": _element["on_tab"],
                    "tab_switch": "",
                    "return": _element["on_return"],
                    "ctrl_return": _element["ctrl_return"],
                }
            # virgin line
            else:
                # init values
                _map = {
                    "tag": _tag,
                    "tab": "",
                    "tab_switch": _element["tab_switch"],
                    "return": "",
                    "ctrl_return": "",
                }
            # end if
            # return mappings
            return _map
        # end if
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


    def init_deferred (self, kw):
        """
            deferred inits;
        """
        # tag styles inits
        self.init_styles(**kw)
        # event bindings
        self.bind_events(**kw)
        # first time init
        self.reset()
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.current_tag = self.DEFAULT_TAG
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
                # init element style
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
        # safe inits
        self.ELEMENT = self.ELEMENT.copy()
        # member inits
        self.init_members(**kw)
        # deferred inits
        self.after_idle(self.init_deferred, kw)
    # end def


    def insert_new_line (self, new_tag, index):
        """
            inserts a new @tag element-formatted line at @index;
        """
        # get current tag
        _current_tag = self.get_line_tag()
        # insert new line
        self.insert("{} lineend".format(TK.INSERT), "\n")
        # move to index location
        self.move_cursor(index)
        # remove previous tag
        self.tag_remove(_current_tag, *self.INS_LINE)
        # set new tag instead
        self.tag_add(new_tag, *self.INS_LINE)
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
            return bool(_chars != "()")
        # default case
        else:
            # inserted if not empty
            return bool(_chars)
        # end if
    # end def


    def move_cursor (self, index):
        """
            moves insertion cursor programmatically;
        """
        # move insertion cursor
        self.mark_set(TK.INSERT, index)
    # end def


    def reset (self, *args, **kw):
        """
            resets text to new;
        """
        # clear text
        self.clear_text()
        # reset members
        self.init_members(**kw)
        # reset default tag
        self.after_idle(self.update_line_tag)
    # end def


    def slot_keypress_scene (self, event=None, *args, **kw):
        """
            event handler: on 'scene' key press;
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
            self.insert(TK.INSERT, _char.upper())
            # update line infos
            self.update_line_tag()
            # break the tkevent chain
            return "break"
        # end if
    # end def


    def slot_on_key_ctrl_return (self, event=None, *args, **kw):
        """
            event handler: on <Ctrl-Return> key press;
        """
        print("slot_on_key_ctrl_return")
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_key_delete (self, event=None, *args, **kw):
        """
            event handler: on <Del> key press;
        """
        print("slot_on_key_delete")
    # end def


    def slot_on_key_return (self, event=None, *args, **kw):
        """
            event handler: on <Return> key press;
        """
        print("slot_on_key_return")
        # inits
        _map = self.get_element_mappings()
        # allowed to create new element line?
        if _map and _map["return"]:
            # allow new line
            self.create_element_line(_map["return"])
        else:
            # debugging
            print("[WARNING] *NOT* allowed to create new line")
        # end if
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_key_tab (self, event=None, *args, **kw):
        """
            event handler: on <Tab> key press;
        """
        print("slot_on_key_tab")
        # break the tkevent chain
        return "break"
    # end def


    def slot_on_keypress (self, event=None, *args, **kw):
        """
            event handler: general keyboard key press;
        """
        #~ print("slot_on_keypress")
        # notify app
        #~ self.events.raise_event("Project:Modified")
        return self.slot_keypress_scene(event)
    # end def


    def slot_on_keyrelease (self, event=None, *args, **kw):
        """
            event handler: general keyboard key release;
        """
        #~ print("slot_on_keyrelease")
        # update line infos
        self.update_line_tag()
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


    def update_current_tag (self, *args, index=None, **kw):
        """
            event handler: updates current line tag pointer;
        """
        # inits
        _tag = self.get_line_tag(index)
        # got element tag?
        if _tag in self.ELEMENT:
            # update current tag
            self.current_tag = _tag
        # end if
        # return last available tag
        return self.current_tag
    # end def


    def update_line_tag (self, *args, **kw):
        """
            event handler: updates line tag to keep it at the right
            place;
        """
        # inits
        _tag = self.update_current_tag()
        print("update_line_tag: current line tag:", _tag)
        # got element tag?
        if _tag in self.ELEMENT:
            # remove tag
            self.tag_remove(_tag, *self.INS_LINE)
            # reset tag all line long
            self.tag_add(_tag, *self.INS_LINE)
            # notify app
            self.events.raise_event(
                "Scenario:Current:Element:Update", element_tag=_tag
            )
        # end if
    # end def

# end class ScenarioText
