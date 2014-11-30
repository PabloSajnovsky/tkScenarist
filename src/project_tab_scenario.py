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
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,

                "Scenario:Combo:Item:Selected":
                    self.slot_combo_item_selected,
                "Scenario:Current:Element:Update":
                    self.slot_update_current_element,
                "Scenario:Elements:Init": self.slot_elements_init,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # always return a dict
        return self.TEXT.get_file_contents(fname)
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.mainwindow = self.winfo_toplevel()
        self.mainframe = self.mainwindow.mainframe
        # looks for ^/xml/widget/tab_scenario.xml
        self.xml_build("tab_scenario")
        # widget inits
        self.TEXT = self.text_scenario
        self.COMBO = self.combo_elements
        self.COMBO.state(["readonly"])
        self.COMBO.current_selected = ""
        self.COMBO.elements = dict()
        self.CBO_CUR_ELT = self.get_stringvar("combo_current_element")
        self.LBL_TAB = self.get_stringvar("lbl_on_tab")
        self.LBL_RET = self.get_stringvar("lbl_on_return")
        self.LBL_CTRL_RET = self.get_stringvar("lbl_on_ctrl_return")
        # event bindings
        self.bind_events(**kw)
    # end def


    def set_combo_text (self, text):
        """
            sets combobox' entry text;
        """
        # param controls
        if text in self.COMBO.elements and \
                                    text != self.COMBO.current_selected:
            # reset current selected
            self.COMBO.current_selected = text
            # reset selection
            self.COMBO.current(-1)
            # set text
            self.CBO_CUR_ELT.set(text)
        # end if
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # set text widget contents
        self.TEXT.file_setup(fname, archive)
    # end def


    def slot_combo_item_selected (self, *args, **kw):
        """
            event handler: item has been selected on combobox;
        """
        print("slot_combo_item_selected")
    # end def


    def slot_elements_init (self, *args, elements=None, **kw):
        """
            event handler: elements have been init'ed;
        """
        print("slot_elements_init")
        # param controls
        if elements:
            # inits
            self.COMBO.current_selected = ""
            self.COMBO.elements = dict()
            # browse elements
            for _element in elements:
                # reset values
                self.COMBO.elements[
                    self.TEXT.get_label(_element)
                    ] = _element
            # end for
            # reset combobox contents
            self.COMBO.configure(values=sorted(self.COMBO.elements))
        # end if
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
        self.TEXT.reset()
    # end def


    def slot_update_current_element (self, *args, **kw):
        """
            event handler: updates current element info;
        """
        # inits
        _label = lambda n: self.TEXT.get_label(n)
        _map = self.TEXT.get_element_mappings()
        # reset widgets
        self.set_combo_text(_label(_map["tag"]))
        self.LBL_TAB.set(_label(_map["tab"] or _map["tab_switch"]))
        self.LBL_RET.set(_label(_map["return"]))
        self.LBL_CTRL_RET.set(
            _label(_map["ctrl_return"] or _map["ctrl_switch"])
        )
    # end def

# end class ProjectTabScenario
