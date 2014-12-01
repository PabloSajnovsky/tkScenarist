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
import json
import random
import tkRAD
import tkRAD.core.async as ASYNC
import tkRAD.core.path as P


class ProjectTabScenario (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    # class constant defs
    DEFAULT_HINT = _(
        "ONE PAGE of script is roughly equal to ONE MINUTE of movie."
    )

    # use i18n support to redefine filepath
    # according to locale language
    INFO_HINTS_FPATH = _("^/data/json/info_hints.en.json")


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,

                "Scenario:Current:Element:Update":
                    self.slot_update_current_element,
                "Scenario:Elements:Init": self.slot_elements_init,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        self.COMBO.bind(
            "<<ComboboxSelected>>", self.slot_combo_item_selected
        )
        self.LISTBOX.bind(
            "<<ListboxSelect>>", self.slot_listbox_item_selected
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
        self.async = ASYNC.get_async_manager()
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
        self.LBL_HINT = self.get_stringvar("lbl_info_hint")
        self.LISTBOX = self.listbox_scene_browser
        # get hints data
        self.reset_hints()
        # event bindings
        self.bind_events(**kw)
    # end def


    def reset_hints (self, fpath=None):
        """
            resets self.INFO_HINTS class member along with @fpath JSON
            file contents;
        """
        # param inits
        fpath = P.normalize(fpath or self.INFO_HINTS_FPATH)
        # get data
        with open(fpath) as _file:
            # reset member
            self.INFO_HINTS = json.load(_file)
        # end with
    # end def


    def set_combo_text (self, text):
        """
            sets combobox' entry text;
        """
        # param controls
        if text in self.COMBO.elements and \
                                    text != self.COMBO.current_selected:
            # update current selected
            self.update_selected(text)
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
            event handler: item has been selected in combobox;
        """
        # inits
        _text = self.CBO_CUR_ELT.get()
        # got something new?
        if _text != self.COMBO.current_selected:
            # update current selected
            self.update_selected(_text)
            # notify app
            self.events.raise_event(
                "Scenario:Switch:Line",
                new_tag=self.COMBO.elements[_text]
            )
        # end if
    # end def


    def slot_listbox_item_selected (self, *args, **kw):
        """
            event handler: item has been selected in listbox;
        """
        # inits
        print("slot_listbox_item_selected")
    # end def


    def slot_elements_init (self, *args, elements=None, **kw):
        """
            event handler: elements have been init'ed;
        """
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
        # reset hints
        self.reset_hints()
    # end def


    def slot_update_current_element (self, *args, **kw):
        """
            event handler: updates current element info;
        """
        # inits
        _label = lambda n: self.TEXT.get_label(n)
        _map = self.TEXT.get_element_mappings()
        _tag = _map["tag"]
        # reset widgets
        self.set_combo_text(_label(_tag))
        self.LBL_TAB.set(_label(_map["tab"] or _map["tab_switch"]))
        self.LBL_RET.set(_label(_map["return"]))
        self.LBL_CTRL_RET.set(
            _label(_map["ctrl_return"] or _map["ctrl_switch"])
        )
        # update hints
        self.async.run_after(700, self.update_hints, _tag)
    # end def


    def update_hints (self, element_tag):
        """
            shows off hints text according to @element_tag value;
            displays default hints otherwise;
        """
        # inits
        _hints = (
            self.INFO_HINTS.get(element_tag)
            or self.INFO_HINTS.get("default")
            or [self.DEFAULT_HINT]
        )
        # ensure to show default hint sometimes
        if random.randint(1, 10) == 7:
            # force default
            _hints = [self.DEFAULT_HINT]
        # end if
        # update hints text
        self.LBL_HINT.set(str(random.choice(_hints)))
    # end def


    def update_selected (self, text):
        """
            updates current selected value;
        """
        # reset current selected
        self.COMBO.current_selected = text
        # reset selection
        self.COMBO.selection_clear()
    # end def

# end class ProjectTabScenario
