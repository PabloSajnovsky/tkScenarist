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
    } # end of CONFIG


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
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,
            }
        )
        # tkinter event bindings
        self.bind("<ButtonRelease>", self.update_insertion_row)
        self.bind("<KeyRelease>", self.slot_on_keypress)
    # end def


    def clear_text (self, *args, **kw):
        """
            event handler for clearing up text widget;
        """
        # clear text
        self.delete("1.0", "end")
        self.update_insertion_row()
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.ins_row_index = "1.0"
    # end def


    def init_styles (self, **kw):
        """
            tag styles inits;
        """
        # inits
        self.tag_configure(
            TK.INSERT,
            background="grey90",
        )
    # end def


    def init_widget (self, **kw):
        r"""
            virtual method to be implemented in subclass;
        """
        # member inits
        self.init_members(**kw)
        # tag styles inits
        self.init_styles(**kw)
        # event bindings
        self.bind_events(**kw)
        # clear text
        self.clear_text()
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
        self.update_insertion_row()
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        pass
    # end def


    def update_insertion_row (self, *args, **kw):
        """
            event handler: updates style for current insertion row;
        """
        # remove previous
        self.tag_remove(TK.INSERT, self.ins_row_index, "end")
        # new position
        self.ins_row_index = self.index("insert linestart")
        # new tag
        self.tag_add(
            TK.INSERT, "insert linestart", "insert linestart + 1 line"
        )
    # end def

# end class ScenarioText
