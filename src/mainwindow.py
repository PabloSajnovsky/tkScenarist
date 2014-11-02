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


class MainWindow (tkRAD.RADXMLMainWindow):
    """
        Application's GUI main window
    """

    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Project:Export:PDF": self.slot_project_export_pdf,
                "Project:New": self.slot_project_new,
                "Project:Open": self.slot_project_open,
                "Project:Save:As": self.slot_project_save_as,
                "Project:Save": self.slot_project_save,

                "Edit:Preferences": self.slot_edit_preferences,
                "Edit:Redo": self.slot_edit_redo,
                "Edit:Undo": self.slot_edit_undo,

                "Tools:NameDatabase": self.slot_tools_name_db,

                "Help:About": self.slot_help_about,
                "Help:Online:Documentation": self.slot_help_online_documentation,
                "Help:Tutorial": self.slot_help_tutorial,

                "Characters:List:Add": self.slot_characters_list_add,
                "Characters:List:Delete": self.slot_characters_list_delete,
            }
        )
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
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
    # end def


    def slot_characters_list_delete (self, *args, **kw):
        """
            event handler for characters list;
        """
        print("Characters:List:Delete")
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
        webbrowser.open("https://github.com/tarball69/tkScenarist/wiki")
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


    def slot_project_export_pdf (self, *args, **kw):
        """
            event handler for menu Project > Export PDF;
        """
        print("Menu:Project:Export PDF")
    # end def


    def slot_project_new (self, *args, **kw):
        """
            event handler for menu Project > New;
        """
        print("Menu:Project:New")
    # end def


    def slot_project_open (self, *args, **kw):
        """
            event handler for menu Project > Open;
        """
        print("Menu:Project:Open")
    # end def


    def slot_project_save (self, *args, **kw):
        """
            event handler for menu Project > Save;
        """
        print("Menu:Project:Save")
    # end def


    def slot_project_save_as (self, *args, **kw):
        """
            event handler for menu Project > Save as...;
        """
        print("Menu:Project:Save as...")
    # end def


    def slot_tools_name_db (self, *args, **kw):
        """
            event handler for menu Tools > Name database;
        """
        print("Menu:Tools:Name database")
    # end def

# end class MainWindow
