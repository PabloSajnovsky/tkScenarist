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
import os.path as OP
import tkinter.filedialog as FD
import tkinter.messagebox as MB
import tkRAD.core.path as P
import tkRAD.core.async as ASYNC
import tkRAD.widgets.rad_dialog as DLG


class NameDatabaseDialog (DLG.RADButtonsDialog):
    """
        Pitch templates management dialog;
    """

    # class constant defs
    #~ BUTTONS = ("OK", "Cancel")
    BUTTONS = ("OK",)

    # nb of rows to show at once
    ROW_LIMIT = 50


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                #~ "Dialog:NameDB:Action": self.slot_action,

                "Dialog:NameDB:Edit:Origin:Drop:List":
                    self.slot_edit_origin_drop_list,

                "Dialog:NameDB:Search:Criteria:Changed":
                    self.slot_search_criteria_changed,

                "Dialog:NameDB:Add:Name": self.slot_add_name,
                "Dialog:NameDB:Delete:Name": self.slot_delete_name,
                "Dialog:NameDB:Import:File": self.slot_import_file,
                "Dialog:NameDB:Show:Next": self.slot_show_next,
                "Dialog:NameDB:Show:Previous": self.slot_show_previous,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
    # end def


    def do_search_criteria (self, *args, **kw):
        """
            event handler;
        """
        print("do_search_criteria")
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
            # looks for ^/xml/widget/dlg_name_database.xml
            xml="dlg_name_database",
        )
        # member inits
        self.async = ASYNC.get_async_manager()
        self.database = self.tk_owner.database
        self.DBVIEW = self.container.dbview_names
        # event bindings
        self.bind_events(**kw)
        # first time query
        self.slot_search_criteria_changed()
    # end def


    def slot_add_name (self, *args, **kw):
        """
            event handler;
        """
        # init
        print("slot_add_name")
    # end def


    def slot_delete_name (self, *args, **kw):
        """
            event handler;
        """
        # init
        print("slot_delete_name")
    # end def


    def slot_edit_origin_drop_list (self, *args, **kw):
        """
            event handler;
        """
        print("slot_edit_origin_drop_list")
    # end def


    def slot_edit_origin_keypress (self, *args, **kw):
        """
            event handler;
        """
        print("slot_edit_origin_keypress")
        return False
    # end def


    def slot_import_file (self, *args, **kw):
        """
            event handler;
        """
        # init
        print("slot_import_file")
    # end def


    def slot_search_criteria_changed (self, *args, **kw):
        """
            event handler;
        """
        # deferred task
        self.async.run_after(1000, self.do_search_criteria)
    # end def


    def slot_show_next (self, *args, **kw):
        """
            event handler: shows next limited nb of rows;
        """
        # init
        print("slot_show_next")
    # end def


    def slot_show_previous (self, *args, **kw):
        """
            event handler: shows previous limited nb of rows;
        """
        # init
        print("slot_show_previous")
    # end def


    def user_confirm (self):
        """
            user confirmation dialog;
        """
        return MB.askyesno(
            title=_("Question"),
            message=_("Are you sure?"),
            parent=self,
        )
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # all is good
        return True
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class NameDatabaseDialog
