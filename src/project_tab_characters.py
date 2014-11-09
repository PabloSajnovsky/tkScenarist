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
import tkinter.messagebox as MB
from tkRAD.core import tools


class ProjectTabCharacters:
    """
        application's project tab characters class;
    """

    # class constant defs


    def __init__ (self, tk_owner):
        """
            class constructor;
        """
        # member inits
        self.tk_owner = tk_owner
        self.mainframe = tk_owner.mainframe
        self.notify = tk_owner.statusbar.notify
        self.cvar_get_text = tk_owner.cvar_get_text
        self.cvar_set_text = tk_owner.cvar_set_text
        self.text_set_contents = tk_owner.text_set_contents
        self.text_get_contents = tk_owner.text_get_contents
        # member inits
        self.character_logs = dict()
    # end def


    def reset (self, *args, **kw):
        """
            reset tab characters to new
        """
        # member inits
        self.character_logs.clear()
        # Listbox widgets
        self.mainframe.listbox_characters_list.delete(0, "end")
        # Text widgets
        self.text_set_contents(self.mainframe.text_characters_log, "")
        # Canvas widgets
        self.mainframe.canvas_characters_relations.delete("all")
    # end def


    def slot_list_add (self, *args, **kw):
        """
            event handler for characters list;
        """
        print("Characters:List:Add")
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def slot_list_delete (self, *args, **kw):
        """
            event handler for characters list;
        """
        print("Characters:List:Delete")
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def

# end class ProjectTabCharacters
