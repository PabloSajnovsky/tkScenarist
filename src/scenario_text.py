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

    # NOTICE: element name == element tag
    DEFAULT_ELEMENT = "scene"

    # NOTICE: element name == element tag
    ELEMENT = {
        "action": {
            "label": _("Action"),
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
            "config": dict(background="grey90"),
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
        # self.tag_bind() triggers event only when mouse pointer
        # is *OVER* tag's region - WTF? /!\
        # we have to work with a tag dispatcher
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
        self.ELEMENT_TAGS = tuple(sorted(self.ELEMENT.keys()))
        self.current_element = self.DEFAULT_ELEMENT
    # end def


    def init_styles (self, **kw):
        """
            tag styles inits;
        """
        # browse elements
        for _tag, _element in self.ELEMENT.items():
            # inits
            _config = _element.get("config") or dict()
            # init element style
            self.tag_configure(_tag, **_config)
        # end for
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
        self.after(100, self.init_deferred, kw)
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
            event handler: on 'scene' key press;
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
            event handler: general keyboard key press;
        """
        print("slot_on_keypress")
        # notify app
        self.events.raise_event("Project:Modified")
        return self.slot_keypress_scene(event)
    # end def


    def switch_to_element (self, element_tag, text_index=None):
        """
            switches to element @element_tag at @text_index, if
            possible;
        """
        # inits
        text_index = text_index or TK.INSERT
        # do setup element?
        if False:                                                           # FIXME
            # create element
            # update current element
            self.current_element = element_tag
            # notify app
            self.events.raise_event(
                "Scenario:Current:Element", element_tag=element_tag
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
