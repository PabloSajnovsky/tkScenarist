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
import tkinter.messagebox as MB
import tkRAD
import tkRAD.core.async as ASYNC
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
        # event bindings
        self.bind_events(**kw)
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # set text widget contents
        #~ self.text_set_contents(self.text_resources, fname)
        pass
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # reset Text widget
        #~ self.text_clear_contents(self.text_resources)
        pass
    # end def

# end class ProjectTabResources
