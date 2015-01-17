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
import tkinter.constants as TK
import tkRAD.widgets.rad_dialog as DLG


class ExportPDFDialog (DLG.RADButtonsDialog):
    """
        Resources Planning Date Bar edition dialog;
    """

    # class constant defs
    BUTTONS = ("OK",)


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide events
        self.events.connect_dict(
            {
                "Dialog:ExportPDF:Export": self.slot_export_pdf,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
    # end def


    def init_widget (self, **kw):
        """
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_export_pdf.xml
            xml="dlg_export_pdf",
        )
        # member inits
        self.mainframe = self.tk_owner.mainframe
        self.keep_looping = False
        # widget inits
        _w = self.container
        self.BTN_EXPORT = _w.btn_export
        # event bindings
        self.bind_events(**kw)
    # end def


    def slot_export_pdf (self, *args, **kw):
        """
            event handler: button clicked;
        """
        print("slot_export_pdf")
        # switch on important task
        self.slot_pending_task_on()
        # change export button
        self.BTN_EXPORT.configure(
            text=_("Stop"), command=self.slot_stop_export,
        )
    # end def

    def slot_stop_export (self, *args, **kw):
        """
            event handler: breaking exportation loop;
        """
        print("slot_stop_export")
        self.keep_looping = False
    # end def

# end class ExportPDFDialog
