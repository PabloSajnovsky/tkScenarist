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
import csv
import tkinter.messagebox as MB
import tkinter.filedialog as FD
import tkRAD.core.async as ASYNC
import tkRAD.core.path as P
import tkRAD.widgets.rad_dialog as DLG


class NameDBImportDialog (DLG.RADButtonsDialog):
    """
        Name database CSV file importation dialog;
    """

    # class constant defs
    BUTTONS = ("OK", )


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Import:Action": self.slot_action,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_ok)
    # end def


    def enable_widget (self, widget, state):
        """
            enables/disables a tkinter widget along with @state value;
            if @state is None, widget keeps unchanged;
        """
        # param controls
        if state is not None:
            widget.configure(
                state={True: "normal"}.get(bool(state), "disabled")
            )
        # end if
    # end def


    def init_widget (self, **kw):
        r"""
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_namedb_import.xml
            xml="dlg_namedb_import",
        )
        # member inits
        self.async = ASYNC.get_async_manager()
        self.database = self.tk_owner.database
        # event bindings
        self.bind_events(**kw)
    # end def


    def slot_action (self, *args, **kw):
        """
            event handler;
        """
        print("slot_action")
    # end def


    def switch_buttons (self, flag=True):
        """
            enables/disables buttons group;
        """
        # buttons
        #~ self.enable_widget(self.container.btn_, flag)
        #~ self.enable_widget(self.container.btn_, flag)
        #~ self.enable_widget(self.container.btn_, flag)
        #~ self.enable_widget(self.container.btn_, flag)
        #~ self.enable_widget(self.container.btn_, flag)
        #~ self.enable_widget(self.container.btn_, flag)
        pass
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # stop all running threads
        #~ self.async.lock(self.do_search_criteria)
        # all is good
        return True
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class NameDBImportDialog
