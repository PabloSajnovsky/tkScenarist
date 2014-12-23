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
                _("1-Director"): None,
                _("2-Male #1"): None,
                _("2-Male #2"): None,
                _("2-Male #3"): None,
                _("3-Female #1"): None,
                _("3-Female #2"): None,
                _("3-Female #3"): None,
                _("4-Animal #1"): None,
                _("4-Animal #2"): None,
                _("4-Animal #3"): None,
            },

            _("Meeting"): {
                _("Location #1"): None,
                _("Location #2"): None,
                _("Location #3"): None,
            },

            _("Promotion"): {
                _("Location #1"): None,
                _("Location #2"): None,
                _("Location #3"): None,
            },
        },

        _("Hardware"): {

            _("Audio"): {
                _("Boom pole"): None,
                _("Cables"): None,
                _("Microphone"): None,
                _("Mixer"): None,
                _("Recorder"): None,
            },

            _("Logistics"): {
                _("Autobus"): None,
                _("Minibus"): None,
                _("Personal car"): None,
                _("Train"): None,
                _("Truck"): None,
            },

            _("Video"): {
                _("Camera"): None,
                _("Crane"): None,
                _("Dolly"): None,
                _("Mount"): None,
                _("Opticals"): None,
                _("Steady"): None,
            },
        },

        _("Staff"): {

            _("01-Producers"): {
                _("Executive producer"): None,
                _("Film producer"): None,
                _("Line producer"): None,
                _("Production manager"): None,
                _("Unit manager"): None,
            },

            _("02-Directors"): {
                _("Art director"): None,
                _("Director of photography"): None,
                _("Film author"): None,
                _("Film maker"): None,
                _("Stage director"): None,
            },

            _("03-Actors"): {
                _("1-Main role (male)"): None,
                _("2-Main role (female)"): None,
                _("3-Secundary #1"): None,
                _("4-Secundary #2"): None,
                _("Extra #1"): None,
                _("Extra #2"): None,
                _("Extra #3"): None,
            },

            _("04-Grip"): {
                _("1-Key grip"): None,
                _("2-Best boy"): None,
                _("3-Dolly grip"): None,
                _("Grip #1"): None,
                _("Grip #2"): None,
                _("Grip #3"): None,
            },

            _("05-Lighting"): {
                _("1-Gaffer"): None,
                _("2-Best boy"): None,
                _("Technician #1"): None,
                _("Technician #2"): None,
                _("Technician #3"): None,
            },

            _("06-Electrical"): {
                _("Electrician #1"): None,
                _("Electrician #2"): None,
                _("Electrician #3"): None,
            },

            _("07-Production sound"): {
                _("1-Production sound mixer"): None,
                _("2-Boom operator"): None,
                _("3-Utility sound technician"): None,
            },

            _("08-Costume dept"): {
                _("1-Costume designer"): None,
                _("2-Costume supervisor"): None,
                _("3-Key costumer"): None,
                _("4-Costume standby"): None,
                _("Cutter #1"): None,
                _("Cutter #2"): None,
                _("Cutter #3"): None,
            },

            _("09-Hair and make-up"): {
                _("1-Key make-up artist"): None,
                _("2-Make-up supervisor"): None,
                _("3-Make-up artist"): None,
                _("4-Key hair"): None,
                _("5-Hair stylist"): None,
            },

            _("10-Special effects"): {
                _("1-SFX supervisor"): None,
                _("SFX assistant #1"): None,
                _("SFX assistant #2"): None,
                _("SFX assistant #3"): None,
            },

            _("11-Stunt team"): {
                _("1-Stunt coordinator"): None,
                _("Stuntman #1"): None,
                _("Stuntman #2"): None,
                _("Stuntman #3"): None,
            },

            _("12-CG team"): {
                _("1-Team manager"): None,
                _("CG artist #1"): None,
                _("CG artist #2"): None,
                _("CG artist #3"): None,
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
            self.LBOX_ITEM.insert(0, *sorted(_item))
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
