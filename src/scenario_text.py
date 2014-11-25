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
        "act break": {
            "tag": "_actbreak_",
            "config": dict(),
        },
        "action": {
            "tag": "_action_",
            "config": dict(),
        },
        "character": {
            "tag": "_character_",
            "config": dict(),
        },
        "dialogue": {
            "tag": "_dialogue_",
            "config": dict(),
        },
        "note": {
            "tag": "_note_",
            "config": dict(),
        },
        "parenthetical": {
            "tag": "_parenthetical_",
            "config": dict(),
        },
        "scene": {
            "tag": "_scene_",
            "config": dict(background="grey80"),
        },
        "shot": {
            "tag": "_shot_",
            "config": dict(),
        },
        "transition": {
            "tag": "_transition_",
            "config": dict(),
        },
    }


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
        self.bind("<KeyRelease>", self.slot_on_keypress)
    # end def


    def clear_text (self, *args, **kw):
        """
            event handler for clearing up text widget;
        """
        # clear text
        self.delete("1.0", "end")
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
            # init element style
            self.tag_configure(_element["tag"], **_element["config"])
        # end for
    # end def


    def init_widget (self, **kw):
        r"""
            virtual method to be implemented in subclass;
        """
        # inits
        self.async = ASYNC.get_async_manager()
        self.ELEMENT_NAMES = tuple(sorted(self.ELEMENT.keys()))
        # member inits
        self.init_members(**kw)
        # tag styles inits
        self.init_styles(**kw)
        # event bindings
        self.bind_events(**kw)
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


    def slot_on_keypress (self, event=None, *args, **kw):
        """
            event handler: on keyboard key press;
        """
        # inits
        pass
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        pass
    # end def

# end class ScenarioText
