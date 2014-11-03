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
import webbrowser
import tkinter.messagebox as MB
import tkRAD
#~ from tkRAD.core import tools
from . import project_file_management as PFM


class MainWindow (tkRAD.RADXMLMainWindow):
    """
        Application's GUI main window;
    """

    # class constant defs
    ONLINE_DOC_URL = "https://github.com/tarball69/tkScenarist/wiki"


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Characters:List:Add":
                    self.slot_characters_list_add,
                "Characters:List:Delete":
                    self.slot_characters_list_delete,

                "Edit:Preferences":
                    self.slot_edit_preferences,
                "Edit:Redo":
                    self.slot_edit_redo,
                "Edit:Undo":
                    self.slot_edit_undo,

                "Entry:Key:Pressed":
                    self.slot_entry_key_pressed,

                "Help:About":
                    self.slot_help_about,
                "Help:Online:Documentation":
                    self.slot_help_online_documentation,
                "Help:Tutorial":
                    self.slot_help_tutorial,

                "Project:Export:PDF":
                    self.project_fm.slot_project_export_pdf,
                "Project:Information:Refresh":
                    self.project_fm.slot_project_refresh_info,
                "Project:Modified":
                    self.project_fm.slot_project_modified,
                "Project:New":
                    self.project_fm.slot_project_new,
                "Project:Open":
                    self.project_fm.slot_project_open,
                "Project:Save:As":
                    self.project_fm.slot_project_save_as,
                "Project:Save":
                    self.project_fm.slot_project_save,

                "Text:Key:Pressed":
                    self.slot_entry_key_pressed,

                "Tools:NameDatabase":
                    self.slot_tools_name_db,
            }
        )
    # end def


    def get_cvar_text (self, cvarname):
        """
            retrieves text from a tk.StringVar() control variable;
        """
        return self.mainframe.get_stringvar(cvarname).get()
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.project_fm = PFM.ProjectFileManagement(self)
        # looks for ^/xml/menu/topmenu.xml
        self.topmenu.xml_build()
        # toggle statusbar through menu
        self.connect_statusbar("show_statusbar")
        # looks for ^/xml/widget/mainwindow.xml
        self.xml_build()
        # event bindings
        self.bind_events(**kw)
    # end def


    def slot_characters_list_add (self, *args, **kw):
        """
            event handler for characters list;
        """
        print("Characters:List:Add")
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def slot_characters_list_delete (self, *args, **kw):
        """
            event handler for characters list;
        """
        print("Characters:List:Delete")
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def slot_edit_preferences (self, *args, **kw):
        """
            event handler for menu Edit > Preferences;
        """
        print("Menu:Edit:Preferences")
    # end def


    def slot_edit_redo (self, *args, **kw):
        """
            event handler for menu Edit > Redo;
        """
        print("Menu:Edit:Redo")
    # end def


    def slot_edit_undo (self, *args, **kw):
        """
            event handler for menu Edit > Undo;
        """
        print("Menu:Edit:Undo")
    # end def


    def slot_entry_key_pressed (self, *args, **kw):
        """
            event handler for ttkentry key press;
        """
        # notify something has changed
        self.events.raise_event("Project:Modified")
        # validate entry keystrokes
        return True
    # end def


    def slot_help_about (self, *args, **kw):
        """
            event handler for menu Help > About;
        """
        MB.showinfo(
            title=_("About..."),
            message=
                "{title}\n{description}\n{copyright}"
                "\n\nAuthor: {author}"
                "\nCurrent maintainer: {maintainer}"
                .format(**self.app.APP),
            parent=self,
        )
    # end def


    def slot_help_online_documentation (self, *args, **kw):
        """
            event handler for menu Help > Online Documentation;
        """
        # launching online documentation
        webbrowser.open(self.ONLINE_DOC_URL)
        # warning message
        MB.showwarning(
            title=_("Attention"),
            message=_("Launching web browser, please wait."),
            parent=self,
        )
    # end def


    def slot_help_tutorial (self, *args, **kw):
        """
            event handler for menu Help > Tutorial;
        """
        print("Menu:Help:Tutorial")
    # end def


    def slot_tools_name_db (self, *args, **kw):
        """
            event handler for menu Tools > Name database;
        """
        print("Menu:Tools:Name database")
    # end def

# end class MainWindow
