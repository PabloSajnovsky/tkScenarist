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
                "Project:New": self.slot_project_new,
                "Project:Open": self.slot_project_open,
                "Project:Save": self.slot_project_save,

                "Edit:Undo": self.slot_edit_undo,
                "Edit:Redo": self.slot_edit_redo,

                "Tools:NameDatabase": self.slot_tools_name_db,

                "Help:About": self.slot_about_dialog,
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


    def slot_about_dialog (self, *args, **kw):
        """
            event handler for menu Help > About;
        """
        print(__name__)
    # end def


    def slot_edit_redo (self, *args, **kw):
        """
            event handler for menu Edit > Redo;
        """
        pass
    # end def


    def slot_edit_undo (self, *args, **kw):
        """
            event handler for menu Edit > Undo;
        """
        pass
    # end def


    def slot_project_new (self, *args, **kw):
        """
            event handler for menu Project > New;
        """
        pass
    # end def


    def slot_project_open (self, *args, **kw):
        """
            event handler for menu Project > Open;
        """
        pass
    # end def


    def slot_project_save (self, *args, **kw):
        """
            event handler for menu Project > Save;
        """
        pass
    # end def


    def slot_tools_name_db (self, *args, **kw):
        """
            event handler for menu Tools > Name database;
        """
        pass
    # end def

# end class MainWindow
