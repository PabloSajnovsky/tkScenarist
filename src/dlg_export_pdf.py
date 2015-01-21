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
import tkRAD.core.async as ASYNC
from tkRAD.core import tools
from . import pdf_export as PDF


class ExportPDFDialog (DLG.RADButtonsDialog):
    """
        Resources Planning Date Bar edition dialog;
    """

    # class constant defs
    BUTTONS = ("OK", )

    ITEM_NAMES = (
        "characters", "draft_notes", "pitch_concept", "resources",
        "scenario", "storyboard",
    )

    OPT_NAMES = (
        "print_scene_left", "print_scene_right", "print_shot_left",
        "print_shot_right", "show_in_viewer",
    )


    def _export_loop (self, kw):
        """
            tk exportation loop;
            for internal use;
        """
        # loop controls
        if self.__keep_looping:
            # nothing to export?
            if not kw.get("export_list"):
                # stop looping
                self.slot_stop_export()
                # notify
                self.show_status(
                    _("Nothing to export. Aborted.")
                )
            # do ops by steps
            else:
                # get method to call
                _method = getattr(
                    self,
                    "_step_{}".format(
                        tools.ensure_int(kw.get("step"))
                    ),
                    None
                )
                # call step
                try:
                    _method(kw)
                # something went wrong
                except Exception as e:
                    # better trap out from here
                    self.slot_stop_export()
                    # notify
                    self.show_status(
                        _(
                            "Got an error while trying to export. "
                            "Aborting."
                        )
                    )
                    # sys.stdout
                    print(
                        "[ERROR] while trying to export: {}.".format(e)
                    )
                # end try
            # end if
            # loop again
            self.async.run_after(50, self._export_loop, kw)
        # end of exportation process
        else:
            # reset progressbar
            self.set_progressbar(100)
            # release important task
            self.events.raise_event("DialogPendingTaskOff")
            # reset button
            self.enable_button("OK")
            # reset export button
            self.BTN_EXPORT.configure(
                text=_("Export"), command=self.slot_export_pdf
            )
            # reset process after a while
            self.async.run_after(5000, self.reset)
        # end if
    # end def


    def _generic_step (self, message, kw, callback):
        """
            generic step procedure;
            for internal use;
        """
        # notify
        self.show_status(message)
        # progressbar
        self.set_progressbar(
            25.0 * (kw["step"] + (kw["progress"] / 100.0))
        )
        # use API callback
        kw["progress"] = callback(kw["doc"])
        # loop until complete
        if kw["progress"] >= 100:
            # reset progress
            kw["progress"] = 0
            # next step
            kw["step"] += 1
        # end if
    # end def


    def _step_0 (self, kw):
        """
            very first step in export loop (inits);
            for internal use;
        """
        # inits
        _export_list = kw.get("export_list")
        _doc_index = tools.ensure_int(kw.get("doc_index"))
        # still got to export docs?
        if _doc_index < len(_export_list):
            # inits
            _doc_name = _export_list[_doc_index]
            # notify
            self.show_status(
                _("Trying to export '{}'...")
                .format(_(self.get_fancy_name(_doc_name)))
            )
            # get PDF document
            kw["doc"] = PDF.get_pdf_document(_doc_name, **kw)
            # reset progressbar
            kw["progress"] = 0
            # prepare for next document
            kw["doc_index"] = _doc_index + 1
            # next step
            kw["step"] = 1
        # no more to export
        else:
            # stop looping
            self.slot_stop_export()
            # notify
            self.show_status(
                _("All selected items exported. Done.")
            )
        # end if
    # end def


    def _step_1 (self, kw):
        """
            building elements;
            for internal use;
        """
        # generic step structure
        self._generic_step(
            _("Building elements..."),
            kw,
            PDF.build_elements
        )
    # end def


    def _step_2 (self, kw):
        """
            building final document;
            for internal use;
        """
        # generic step structure
        self._generic_step(
            _("Exporting to PDF..."),
            kw,
            PDF.build_document
        )
        # return to step 0 on completion
        kw["step"] %= 3
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide events
        self.events.connect_dict(
            {
                "Dialog:ExportPDF:Checkbutton:Click":
                    self.slot_on_checkbutton_clicked,

                "Dialog:ExportPDF:Export": self.slot_export_pdf,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_ok)
    # end def


    def cancel_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog cancellation method;
            this is a hook called by '_slot_button_cancel()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # put here your own code in subclass
        self.slot_stop_export()
        self.slot_stop_async()
        # succeeded
        return True
    # end def


    def check_cvar (self, cvarname, state=True):
        """
            checks/unchecks checkbutton's control variable along with
            @state boolean value;
            if @state is None, keeps checkbutton unchanged;
        """
        # param controls
        if state is not None:
            self.container.get_stringvar(cvarname).set(
                "1" if tools.ensure_int(state) else ""
            )
        # end if
    # end def


    def cvar_checked (self, cvarname):
        """
            returns True if control variable @cvarname is checked,
            False otherwise;
        """
        return bool(
            self.container.get_stringvar(cvarname).get() == "1"
        )
    # end def


    def get_export_list (self):
        """
            retrieves user's exportation list and returns a list of doc
            names to export;
        """
        # inits
        _list = []
        # browse doc names
        for _name in self.ITEM_NAMES:
            # user selected?
            if self.cvar_checked("chk_" + _name):
                # append to list
                _list.append(_name)
            # end if
        # end for
        # get list
        return _list
    # end def


    def get_fancy_name (self, doc_name):
        """
            returns a fancier name to show off for a given @doc_name;
        """
        return str(doc_name).replace("_", "/").title()
    # end def


    def get_options (self):
        """
            returns dict of options {name: state, ...};
            state is a boolean value (True, False);
        """
        # inits
        _options = dict()
        # browse options
        for _name in self.OPT_NAMES:
            # inits
            _options[_name] = self.cvar_checked("chk_" + _name)
        # end for
        return _options
    # end def


    def init_rc_options (self, **kw):
        """
            RC options widget inits;
        """
        # inits
        _s = self.get_rc_section()
        # update widgets
        for _cvarname in self.ALL_NAMES:
            _chk = "chk_" + _cvarname
            self.check_cvar(
                _chk, self.options.get(_s, _chk, fallback=None)
            )
        # end for
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
        self.ALL_NAMES = self.ITEM_NAMES + self.OPT_NAMES
        self.mainframe = self.tk_owner.mainframe
        self.async = ASYNC.get_async_manager()
        self.__keep_looping = False
        # widget inits
        _w = self.container
        self.LBL_STATUS = _w.get_stringvar("lbl_export_status")
        self.PROGRESSBAR = _w.progressbar_export
        self.PBAR_VALUE = _w.get_stringvar("pbar_value")
        self.BTN_EXPORT = _w.btn_export
        self.init_rc_options(**kw)
        # event bindings
        self.bind_events(**kw)
    # end def


    def progressbar_wait (self, *args, **kw):
        """
            event handler: simulates progressbar waiting for ops;
        """
        # stop animation
        self.PROGRESSBAR.stop()
        # set indeterminate mode
        self.PROGRESSBAR.configure(mode="indeterminate")
        # restart animation
        self.PROGRESSBAR.start()
    # end def


    def reset (self, *args, **kw):
        """
            event handler: resets export process informations;
        """
        # reset status
        self.show_status("")
        # reset progressbar
        self.set_progressbar(0)
    # end def


    def save_rc_options (self, *args, **kw):
        """
            event handler: saves RC options from widget states;
        """
        # inits
        _s = self.get_rc_section()
        # save RC options
        for _cvarname in self.ALL_NAMES:
            _chk = "chk_" + _cvarname
            self.options[_s][_chk] = str(int(self.cvar_checked(_chk)))
        # end for
    # end def


    def set_progressbar (self, value):
        """
            sets progressbar to @value (between 0 and 100);
        """
        # set determinate mode
        self.PROGRESSBAR.configure(mode="determinate")
        # stop animation
        self.PROGRESSBAR.stop()
        # set value
        self.PBAR_VALUE.set(str(tools.ensure_int(value)))
    # end def


    def show_status (self, message):
        """
            shows message in exportation status;
        """
        self.LBL_STATUS.set(str(message))
    # end def


    def slot_export_pdf (self, *args, **kw):
        """
            event handler: button clicked;
        """
        # stop eventually pending tasks
        self.slot_stop_async()
        # switch on important task
        self.events.raise_event("DialogPendingTaskOn")
        # disable button
        self.disable_button("OK")
        # change export button
        self.BTN_EXPORT.configure(
            text=_("Stop"), command=self.slot_stop_export,
        )
        # notify
        self.show_status(
            _("Trying to export selected items, please wait.")
        )
        # waiting for ops
        self.progressbar_wait()
        # inits
        self.__keep_looping = True
        # launch exportation loop
        self.async.run_after_idle(
            self._export_loop,
            dict(
                export_list=self.get_export_list(),
                options=self.get_options(),
                data=self.mainframe.tab_title_data.get_data(),
                doc_index=0,
                step=0,
            )
        )
    # end def


    def slot_on_checkbutton_clicked (self, event=None, *args, **kw):
        """
            event handler: checkbutton has been clicked;
        """
        # save RC options
        self.save_rc_options()
    # end def


    def slot_stop_async (self, *args, **kw):
        """
            event handler: stop all async tasks for this dialog;
        """
        self.async.stop(self._export_loop, self.reset)
    # end def


    def slot_stop_export (self, *args, **kw):
        """
            event handler: breaking exportation loop;
        """
        # break tk loop
        self.__keep_looping = False
        # notify
        self.show_status(
            _("User asked for cancellation.")
        )
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # inits
        _ret = not self.verify_pending_task()
        # all is OK?
        if _ret:
            # stop pending tasks before quitting
            self.slot_stop_async()
        # end if
        return _ret
    # end def

# end class ExportPDFDialog
