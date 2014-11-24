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
import tkRAD.core.async as ASYNC
import tkRAD.widgets.rad_dialog as DLG
from . import dlg_namedb_import as DNI


class NameDatabaseDialog (DLG.RADButtonsDialog):
    """
        Name database preview dialog;
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
        self.bind("<Escape>", self._slot_button_ok)
    # end def


    def do_search_criteria (self, *args, **kw):
        """
            event handler;
        """
        # switch off buttons
        self.switch_buttons(False)
        # inits
        _cvar = lambda n: self.container.get_stringvar(n).get()
        _criteria = {
            "query": _cvar("search_mention"),
            "name": _cvar("search_chk_name"),
            "origin": _cvar("search_chk_origin"),
            "description": _cvar("search_chk_description"),
            "all": _cvar("search_chk_all"),
            "male": _cvar("search_chk_male"),
            "female": _cvar("search_chk_female"),
        }
        # get DB rows
        _rows = self.database.get_character_names(
            limit=self.ROW_LIMIT,
            offset=self.current_offset,
            **_criteria
        )
        # show query header
        self.DBVIEW.set_header(
            *self.database.get_column_names(),
            body_options={
                "Gender": {"text": {"align": "center"}},
                "Description": {"text": {"width": 400}},
            }
        )
        # got results?
        if _rows:
            # update offset max
            self.offset_max = max(self.current_offset, self.offset_max)
            # show rows in DBView
            for _row in _rows:
                self.DBVIEW.insert_row(dict(_row))
            # end for
        # no results
        elif self.current_offset > self.offset_max:
            # limit offset to offset max
            self.current_offset = self.offset_max
            # restart query
            self.do_search_criteria()
        # end if
        # switch on buttons
        self.switch_buttons(True)
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
        self.reset_offset()
        # event bindings
        self.bind_events(**kw)
        # first time query
        self.slot_search_criteria_changed(delay=200)
    # end def


    def reset_offset (self, *args, **kw):
        """
            event handler: resets offset pointers;
        """
        # inits
        self.current_offset = 0
        self.offset_max = 0
    # end def


    def slot_import_file (self, *args, **kw):
        """
            event handler;
        """
        # show file import dialog
        DNI.NameDBImportDialog(self).show()
        # reset DB view
        self.slot_search_criteria_changed(delay=100)
    # end def


    def slot_search_criteria_changed (self, *args, **kw):
        """
            event handler;
        """
        # reset offset
        self.reset_offset()
        # deferred task
        self.async.run_after(
            kw.get("delay") or 1000, self.do_search_criteria
        )
    # end def


    def slot_search_filter_all (self, *args, **kw):
        """
            event handler;
        """
        # uncheck 'male'/'female' checkboxes
        self.container.get_stringvar("search_chk_male").set("")
        self.container.get_stringvar("search_chk_female").set("")
        # refresh query
        self.slot_search_criteria_changed(delay=500)
    # end def


    def slot_search_filter_clicked (self, *args, **kw):
        """
            event handler;
        """
        # uncheck 'all' checkbox
        self.container.get_stringvar("search_chk_all").set("")
        # refresh query
        self.slot_search_criteria_changed(delay=500)
    # end def


    def slot_show_next (self, *args, **kw):
        """
            event handler: shows next limited nb of rows;
        """
        # inits
        self.current_offset += self.ROW_LIMIT
        # refresh query
        self.async.run_after(500, self.do_search_criteria)
    # end def


    def slot_show_previous (self, *args, **kw):
        """
            event handler: shows previous limited nb of rows;
        """
        # not at beginning?
        if self.current_offset > 0:
            # inits
            self.current_offset = max(
                0, self.current_offset - self.ROW_LIMIT
            )
            # refresh query
            self.async.run_after(500, self.do_search_criteria)
        # end if
    # end def


    def switch_buttons (self, flag=True):
        """
            enables/disables buttons group;
        """
        # buttons
        self.enable_widget(self.container.btn_show_next, flag)
        self.enable_widget(self.container.btn_show_previous, flag)
        self.enable_widget(self.container.btn_import_file, flag)
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # stop all running threads
        self.async.lock(self.do_search_criteria)
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
