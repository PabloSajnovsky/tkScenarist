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
import tkRAD.core.async as ASYNC


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

    DEFAULT_ELEMENT = "scene"

    ELEMENT = {
        "act_break": {
            "label": "_actbreak_",
            "on_return": "scene",
            "on_tab": "action",
            "tab_switch": "scene",
            "ctrl_return": "scene",
        },
        "action": {
            "label": "_action_",
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "character",
            "ctrl_return": "character",
        },
        "character": {
            "label": "_character_",
            "on_return": "dialogue",
            "on_tab": "parenthetical",
            "tab_switch": "action",
            "ctrl_return": "action",
        },
        "dialogue": {
            "label": "_dialogue_",
            "on_return": "character",
            "on_tab": "action",
            "tab_switch": "parenthetical",
            "ctrl_return": "action",
        },
        "note": {
            "label": "_note_",
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "action",
            "ctrl_return": "character",
        },
        "parenthetical": {
            "label": "_parenthetical_",
            "on_return": "dialogue",
            "on_tab": "action",
            "tab_switch": "character",
            "ctrl_return": "dialogue",
        },
        "scene": {
            "label": "_scene_",
            "config": dict(background="grey90"),
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "action",
            "ctrl_return": "transition",
        },
        "shot": {
            "label": "_shot_",
            "on_return": "action",
            "on_tab": "character",
            "tab_switch": "action",
            "ctrl_return": "scene",
        },
        "transition": {
            "label": "_transition_",
            "on_return": "scene",
            "on_tab": "transition",
            "tab_switch": "scene",
            "ctrl_return": "character",
        },
    }

    INS_LINE = ("insert linestart", "insert linestart + 1 line")


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
        # self.tag_bind() triggers events only when mouse pointer
        # is *OVER* the tag region - WTF? /!\
        # must work with a tag dispatcher
        self.bind("<Key>", self.slot_on_keypress)
        self.bind("<Return>", self.slot_on_key_return)
        self.bind("<Tab>", self.slot_on_key_tab)
        self.bind("<Control-Return>", self.slot_on_key_ctrl_return)
    # end def


    def clear_text (self, *args, **kw):
        """
            event handler for clearing up text widget;
        """
        # clear text
        self.delete("1.0", "end")
    # end def


    def get_element_tag (self, element_name=None):
        """
            returns element tag from @element_name, if exists;
            returns None otherwise;
        """
        # inits
        element_name = element_name or self.current_element
        _element = self.ELEMENT.get(element_name) or dict()
        # return result
        return _element.get("label")
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
        self.switch_to_element(self.DEFAULT_ELEMENT)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.current_element = self.DEFAULT_ELEMENT
    # end def


    def init_styles (self, **kw):
        """
            tag styles inits;
        """
        # browse elements
        for _element in self.ELEMENT.values():
            # inits
            _config = _element.get("config") or dict()
            # init element style
            self.tag_configure(_element["label"], **_config)
        # end for
    # end def


    def init_widget (self, **kw):
        r"""
            virtual method to be implemented in subclass;
        """
        # inits
        self.async = ASYNC.get_async_manager()
        self.ELEMENT = self.ELEMENT.copy()
        self.ELEMENT_NAMES = tuple(sorted(self.ELEMENT.keys()))
        # member inits
        self.init_members(**kw)
        # deferred inits
        self.after(100, self.init_deferred, kw)
    # end def


    def put_element_tag (self, *args, **kw):
        """
            event handler: put element tag at linestart if no tags are
            already out there;
        """
        # inits
        _tags = self.tag_names(TK.INSERT)
        # no tags out there?
        if not _tags:
            # set new tag
            self.update_line_tag()
        # warn dev
        else:
            print(
                "put_element_tag() - current line already tagged:",
                _tags
            )
        # end if
    # end def


    def reset (self, *args, **kw):
        """
            resets text to new;
        """
        # clear text
        self.clear_text()
        # reset members
        self.init_members(**kw)
    # end def


    def slot_keypress_scene (self, event=None, *args, **kw):
        """
            event handler: on keyboard key press;
        """
        # inits
        _char = event.char
        _modifiers = (event.state & 0x8c)
        # letter char?
        if _char and ord(_char) > 31 and not _modifiers:
            # set to uppercase
            self.insert(TK.INSERT, event.char.upper())
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


    def slot_on_key_return (self, event=None, *args, **kw):
        """
            event handler: on <Return> key press;
        """
        print("slot_on_key_return")
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
            event handler: on keyboard key press;
        """
        print("slot_on_keypress")
        # notify app
        self.events.raise_event("Project:Modified")
        return self.slot_keypress_scene(event)
    # end def


    def switch_to_element (self, element_name, text_index=None):
        """
            switches to element @element_name at @text_index, if
            possible;
        """
        # inits
        text_index = text_index or TK.INSERT
        # do setup element?
        if False:                                                           # FIXME
            # create element
            # update current element
            self.current_element = element_name
            # notify app
            self.events.raise_event(
                "Scenario:Current:Element", element_name=element_name
            )
        # end if
    # end def


    def update_line_tag (self, *args, **kw):
        """
            event handler: updates line tag to keep it at the right
            place;
        """
        # inits
        _tag = self.get_element_tag()
        # remove tag
        self.tag_remove(_tag, *self.INS_LINE)
        # reset tag
        self.tag_add(_tag, *self.INS_LINE)
    # end def

# end class ScenarioText