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


class ProjectTabScenario (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,

                "Scenario:Current:Element:Update":
                    self.slot_update_current_element,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # inits
        fcontents = self.text_get_contents(self.TEXT)
        # always return a dict
        return {fname: fcontents}
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
        # looks for ^/xml/widget/tab_scenario.xml
        self.xml_build("tab_scenario")
        # widget inits
        self.TEXT = self.text_scenario
        self.LBL_CUR_ELT = self.get_stringvar("lbl_current_element")
        self.LBL_TAB = self.get_stringvar("lbl_on_tab")
        self.LBL_RET = self.get_stringvar("lbl_on_return")
        self.LBL_CTRL_RET = self.get_stringvar("lbl_on_ctrl_return")
        # event bindings
        self.bind_events(**kw)
        # reset tab
        self.after_idle(self.slot_tab_reset)
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # set text widget contents
        self.text_set_contents(self.TEXT, fname)
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # reset status
        self.TEXT.edit_modified(flag)
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # reset Text widget
        self.text_clear_contents(self.TEXT)
    # end def


    def slot_update_current_element (self, *args, element_tag=None, **kw):
        """
            event handler: updates current element info;
        """
        # param controls
        if element_tag:
            # inits
            _label = lambda n: self.TEXT.get_label(n)
            _map = self.TEXT.get_element_mappings(element_tag)
            # reset widgets
            self.LBL_CUR_ELT.set(_label(element_tag))
            self.LBL_TAB.set(_label(_map["tab"]))
            self.LBL_RET.set(_label(_map["return"]))
            self.LBL_CTRL_RET.set(_label(_map["ctrl_return"]))
        # end if
    # end def

# end class ProjectTabScenario
