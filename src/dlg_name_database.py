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
                "Dialog:NameDB:Search:Criteria:Changed":
                    self.slot_search_criteria_changed,

                "Dialog:NameDB:Search:Filter:All":
                    self.slot_search_filter_all,
                "Dialog:NameDB:Search:Filter:Clicked":
                    self.slot_search_filter_clicked,

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
        # search
        _query = self.get_cvar("search_mention", checkbutton=False)
        _name = self.get_cvar("search_chk_name")
        _origin = self.get_cvar("search_chk_origin")
        _description = self.get_cvar("search_chk_description")
        # filters
        _all = self.get_cvar("search_chk_all")
        _male = self.get_cvar("search_chk_male")
        _female = self.get_cvar("search_chk_female")
        # all names priority?
        if _all["value"]:
            # clear others
            _male["cvar"].set("")
            _female["cvar"].set("")
        # end if
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


    def get_cvar (self, cvarname, checkbutton=True):
        """
            returns a dict(cvar=object, value=obj_value); if
            @checkbutton is True, changes obj_value to boolean;
        """
        # inits
        _cvar = self.container.get_stringvar(cvarname)
        # got object?
        if _cvar:
            # get raw value
            _value = _cvar.get()
            # asked for a checkbutton value?
            if checkbutton:
                # get boolean
                _value = bool(_value == "1")
            # end if
            # succeeded
            return dict(cvar=_cvar, value=_value)
        # end if
        # failed
        return None
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
        self.current_offset = 0
        self.offset_max = 0
        # event bindings
        self.bind_events(**kw)
        # first time query
        self.slot_search_criteria_changed()
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


    def slot_search_filter_all (self, *args, **kw):
        """
            event handler;
        """
        # uncheck 'male'/'female' checkboxes
        self.container.get_stringvar("search_chk_male").set("")
        self.container.get_stringvar("search_chk_female").set("")
        # refresh query
        self.slot_search_criteria_changed()
    # end def


    def slot_search_filter_clicked (self, *args, **kw):
        """
            event handler;
        """
        # uncheck 'all' checkbox
        self.container.get_stringvar("search_chk_all").set("")
        # refresh query
        self.slot_search_criteria_changed()
    # end def


    def slot_show_next (self, *args, **kw):
        """
            event handler: shows next limited nb of rows;
        """
        # inits
        self.current_offset = min(
            self.current_offset + self.ROW_LIMIT, self.offset_max
        )
        # refresh query
        self.slot_search_criteria_changed()
    # end def


    def slot_show_previous (self, *args, **kw):
        """
            event handler: shows previous limited nb of rows;
        """
        # inits
        self.current_offset = max(
            0, self.current_offset - self.ROW_LIMIT
        )
        # refresh query
        self.slot_search_criteria_changed()
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
