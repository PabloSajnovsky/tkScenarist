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
import os.path as OP
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

    DEFAULT_DIR = "^/data/csv"

    FILE_TYPES = (
        (_("CSV files"), "*.csv"),
        (_("Text files"), "*.txt"),
        (_("All files"), "*.*"),
    )


    def _do_open_file (self, fpath):
        """
            effective procedure for opening file to import;
        """
        # is a genuine CSV file?
        if self.is_csv(fpath):
            # update options dir
            self.options["dirs"]["namedb_import_dir"] = OP.dirname(fpath)
            # update file infos
            self.container.get_stringvar("lbl_file_path")\
                .set(P.shorten_path(fpath, limit=45))
            # update dialect fields
        # not a CSV file
        else:
            # notify user
            MB.showwarning(
                title=_("Attention"),
                message=_("Invalid CSV file format. Not supported."),
                parent=self,
            )
        # end if
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Import:File:Browse": self.slot_file_browse,
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
        self.DEFAULT_DIR = P.normalize(self.DEFAULT_DIR)
        # event bindings
        self.bind_events(**kw)
    # end def


    def is_csv (self, fpath):
        """
            returns True if @fpath is evaluated to be a CSV file
            format, False otherwise;
        """
        return True # FIXME
    # end def


    def slot_file_browse (self, *args, **kw):
        """
            event handler: shows a file dialog for importing file
            selection;
        """
        # init
        _path = FD.askopenfilename(
            title=_("Please, select a file to import"),
            initialdir=self.options.get(
                "dirs", "namedb_import_dir", fallback=self.DEFAULT_DIR
            ),
            filetypes=self.FILE_TYPES,
            multiple=False,
            parent=self,
        )
        # user selected a path?
        if _path:
            # do open file for importation
            self._do_open_file(_path)
        # end if
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
