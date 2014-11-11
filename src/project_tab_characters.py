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
import tkRAD


class ProjectTabCharacters (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Characters:List:Add": self.slot_list_add,
                "Characters:List:Delete": self.slot_list_delete,

                "Project:Modified": self.slot_project_modified,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
    # end def


    def get_file_contents (self, fname):
        """
            returns formatted string as file contents;
        """
        # multiple files and contents
        _dict = dict()
        # list of character names
        _fname = fname["names"]
        _fcontents = "\n".join(
            self.listbox_characters_list.get(0, "end")
        )
        _dict[_fname] = _fcontents
        # character logs
        _fname = fname["logs"]
        _fcontents = ""                                                     # FIXME
        _dict[_fname] = _fcontents
        # character relations
        _fname = fname["relations"]
        _fcontents = ""                                                     # FIXME
        _dict[_fname] = _fcontents
        # always return a dict
        return _dict
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.mainwindow = self.winfo_toplevel()
        self.mainframe = self.mainwindow.mainframe
        self.text_clear_contents = self.mainwindow.text_clear_contents
        self.text_get_contents = self.mainwindow.text_get_contents
        self.text_set_contents = self.mainwindow.text_set_contents
        self.character_logs = dict()
        # looks for ^/xml/widget/tab_characters.xml
        self.xml_build("tab_characters")
        # event bindings
        self.bind_events(**kw)
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


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # reset status
        self.text_characters_log.edit_modified(flag)
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # member inits
        self.character_logs.clear()
        # Listbox widgets
        self.listbox_characters_list.delete(0, "end")
        # Text widgets
        self.text_clear_contents(self.text_characters_log)
        # Canvas widgets
        self.canvas_characters_relations.delete("all")
    # end def

# end class ProjectTabCharacters
