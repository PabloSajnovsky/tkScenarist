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
import tkRAD.widgets.rad_dialog as DLG


class PitchTemplatesDialog (DLG.RADButtonsDialog):
    """
        Pitch templates management dialog;
    """

    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Template:Delete": self.slot_template_delete,
                "Dialog:Template:Modify": self.slot_template_modify,
                "Dialog:Template:New": self.slot_template_new,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
    # end def


    def init_widget (self, **kw):
        r"""
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_pitch_templates.xml
            xml="dlg_pitch_templates",
        )
        # event bindings
        self.bind_events()
    # end def


    def slot_template_delete (self, *args, **kw):
        """
            event handler;
        """
        print("template delete")
    # end def


    def slot_template_modify (self, *args, **kw):
        """
            event handler;
        """
        print("template modify")
    # end def


    def slot_template_new (self, *args, **kw):
        """
            event handler;
        """
        print("template new")
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # put here your own code in subclass
        # succeeded
        return True
    # end def

# end class PitchTemplatesDialog
