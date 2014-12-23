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
import copy
import json
import tkRAD
from tkRAD.core import tools


class ProjectTabResources (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    # class constant defs
    RES_DEFAULTS = {

        _("Events"): {

            _("Casting"): {
                _("Animals"): {},
                _("Directors"): {},
                _("Female"): {},
                _("Male"): {},
            },

            _("Meeting"): {
                _("Locations"): {},
                _("Organizers"): {},
            },

            _("Promotion"): {
                _("Organizers"): {},
                _("Targets"): {},
            },
        },

        _("Hardware"): {

            _("Accessories"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Audio"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Logistics"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Video"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Wardrobe"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },
        },

        _("Staff"): {

            _("Actors"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("CG team"): {
                _("CG artist #1"): {},
                _("CG artist #2"): {},
                _("CG artist #3"): {},
                _("Team manager"): {},
            },

            _("Cookers"): {
                _("Chef"): {},
                _("Cooker #1"): {},
                _("Cooker #2"): {},
                _("Cooker #3"): {},
                _("Commis chef #1"): {},
                _("Commis chef #2"): {},
                _("Commis chef #3"): {},
                _("Waiter #1"): {},
                _("Waiter #2"): {},
                _("Waiter #3"): {},
                _("Waitress #1"): {},
                _("Waitress #2"): {},
                _("Waitress #3"): {},
            },

            _("Directors"): {
                _("Art director"): {},
                _("Author"): {},
                _("Film-maker"): {},
                _("Picture director"): {},
                _("Stage director"): {},
            },

            _("Engineers"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Make up"): {
                _("Hairdresser #1"): {},
                _("Hairdresser #2"): {},
                _("Hairdresser #3"): {},
                _("Make up artist #1"): {},
                _("Make up artist #2"): {},
                _("Make up artist #3"): {},
                _("Special FX artist #1"): {},
                _("Special FX artist #2"): {},
                _("Special FX artist #3"): {},
            },

            _("Producers"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Stunt team"): {
                _(""): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },

            _("Technicians"): {
                _("Electrician"): {},
                _(""): {},
                _(""): {},
                _(""): {},
            },
        },
    }


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        self.CBO_TYPE.bind(
            "<<ComboboxSelected>>", self.slot_combo_type_selected
        )
        self.CBO_SECTION.bind(
            "<<ComboboxSelected>>", self.slot_combo_section_selected
        )
    # end def


    def clear_combo (self, *widgets):
        """
            clears contents for combobox widget(s);
        """
        # browse widgets
        for _w in widgets:
            # clear widget
            _w.delete(0, "end")
            # clear selection
            _w.selection_clear()
        # end for
    # end def


    def clear_listbox (self, *widgets):
        """
            clears contents for listbox widget(s);
        """
        # browse widgets
        for _w in widgets:
            # clear widget
            _w.delete(0, "end")
            # clear selection
            _w.selection_clear(0, "end")
            # reset last selected
            _w.last_selected = -1
        # end for
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # inits
        fcontents = ""                                                      # FIXME
        #~ fcontents = self.text_get_contents(self.text_resources)
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_res_item (self):
        """
            retrieves resources item along with current resources type
            and section selected in combos or dict() if not found;
        """
        # inits
        _section = self.get_res_section()
        return _section.get(self.CBO_SECTION.get()) or dict()
    # end def


    def get_res_section (self):
        """
            retrieves resources section along with current resources
            type selected in combo or dict() if not found;
        """
        return self.RESOURCES.get(self.CBO_TYPE.get()) or dict()
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
        # looks for ^/xml/widget/tab_resources.xml
        self.xml_build("tab_resources")
        # widget inits
        _readonly = ["readonly"]
        self.CBO_TYPE = self.combo_res_type
        self.CBO_TYPE.state(_readonly)
        self.CBO_SECTION = self.combo_res_section
        self.CBO_SECTION.state(_readonly)
        self.LBOX_ITEM = self.listbox_res_item
        # event bindings
        self.bind_events(**kw)
        # reset once
        self.slot_tab_reset()
    # end def


    def reset_resources (self, new_dict):
        """
            resets self.RESOURCES dictionary with @new_dict;
        """
        if tools.is_pdict(new_dict):
            # reset dict (unreferenced)
            self.RESOURCES = copy.deepcopy(new_dict)
            # reset combos + listbox
            self.clear_combo(self.CBO_TYPE, self.CBO_SECTION)
            self.clear_listbox(self.LBOX_ITEM)
            self.CBO_TYPE.configure(values=sorted(self.RESOURCES))
            # got selection?
            if self.RESOURCES:
                self.CBO_TYPE.current(0)
                self.slot_combo_type_selected()
            # end if
        # end if
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # set text widget contents
        #~ self.text_set_contents(self.text_resources, fname)
        pass
    # end def


    def slot_combo_section_selected (self, event=None, *args, **kw):
        """
            event handler: item has been selected in combobox;
        """
        print("slot_combo_section_selected")
        # inits
        _item = self.get_res_item()
        # clear listbox
        self.clear_listbox(self.LBOX_ITEM)
        # got selection?
        if _item:
            # fill values
            self.LBOX_ITEM.insert(0, sorted(_item))
            # select first
            self.LBOX_ITEM.selection_set(0)
            self.slot_listbox_item_selected()
        # end if
    # end def


    def slot_combo_type_selected (self, event=None, *args, **kw):
        """
            event handler: item has been selected in combobox;
        """
        print("slot_combo_type_selected")
        # inits
        _section = self.get_res_section()
        # clear listbox
        self.clear_listbox(self.LBOX_ITEM)
        # reset combo
        self.clear_combo(self.CBO_SECTION)
        # got selection?
        if _section:
            # fill values
            self.CBO_SECTION.configure(values=sorted(_section))
            # select first
            self.CBO_SECTION.current(0)
            self.slot_combo_section_selected()
        # end if
    # end def


    def slot_listbox_item_selected (self, event=None, *args, **kw):
        """
            event handler: item has been selected in listbox;
        """
        print("slot_listbox_item_selected")
        # inits
        pass
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # reset combos
        self.reset_resources(self.RES_DEFAULTS)                             # FIXME: self.options?
    # end def

# end class ProjectTabResources
