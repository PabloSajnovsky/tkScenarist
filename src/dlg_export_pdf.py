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
from . import pdf_export as PDF


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


    def export_loop (self, kw):
        """
            tk exportation loop;
        """
        print("export_loop")
        # inits
        _export_list = kw.get("export_list")
        _step = kw.get("step") or 0
        print("export list:", _export_list)
        self.after(500)
        # loop again
        if self.keep_looping:
            self.after_idle(self.export_loop, kw)
        # end of exportation process
        else:
            # release important task
            self.events.raise_event("DialogPendingTaskOff")
            # reset button
            self.enable_button("OK")
            # reset export button
            self.BTN_EXPORT.configure(
                text=_("Export"), command=self.slot_export_pdf
            )
        # end if
    # end def


    def get_export_list (self):
        """
            retrieves user's exportation list and returns a list of doc
            names to export;
        """
        # inits
        _names = (
            "scenario", "storyboard", "pitch_concept", "draft_notes",
            "characters", "resources",
        )
        _export_list = []
        _cvar = lambda n: self.container.get_stringvar("chk_" + n).get()
        # browse doc names
        for _name in _names:
            # user selected?
            if _cvar(_name):
                # append to list
                _export_list.append(_name)
            # end if
        # end for
        # get list
        return _export_list
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
        self.BTN_EXPORT = self.container.btn_export
        # event bindings
        self.bind_events(**kw)
    # end def


    def slot_export_pdf (self, *args, **kw):
        """
            event handler: button clicked;
        """
        print("slot_export_pdf")
        # switch on important task
        self.events.raise_event("DialogPendingTaskOn")
        # disable button
        self.disable_button("OK")
        # change export button
        self.BTN_EXPORT.configure(
            text=_("Stop"), command=self.slot_stop_export,
        )
        # inits
        self.keep_looping = True
        # launch exportation loop
        self.after_idle(
            self.export_loop,
            dict(export_list=self.get_export_list())
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
