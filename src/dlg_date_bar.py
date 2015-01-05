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
from datetime import date
import calendar
import tkRAD.widgets.rad_dialog as DLG


class DateBarDialog (DLG.RADButtonsDialog):
    """
        Resources Planning Date Bar edition dialog;
    """

    # class constant defs
    BUTTONS = ("OK", "Cancel")
    DATE_ERROR = _("invalid date")


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        #~ self.events.connect_dict(
            #~ {
            #~ }
        #~ )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
    # end def


    def init_combos (self, *groups):
        """
            sets default values for date combos groups;
            group is combo tuple(day, month, year);
        """
        # inits
        _DAYS = ["{:02d}".format(i) for i in range(1, 32)]
        _MONTHS = list(calendar.month_abbr)[1:]
        _YEAR = date.today().year
        _YEARS = list(range(_YEAR - 1, _YEAR + 5))
        # browse groups
        for _group in groups:
            # inits
            _day, _month, _year = _group
            # day values
            _day.configure(values=_DAYS, state="readonly")
            _day.current(0)
            # month values
            _month.configure(values=_MONTHS, state="readonly")
            _month.current(0)
            # year values
            _year.configure(values=_YEARS, state="readonly")
            _year.current(1)
        # end for
    # end def


    def init_widget (self, **kw):
        r"""
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_date_bar.xml
            xml="dlg_date_bar",
        )
        # member inits
        _w = self.container
        self.LBL_NAME = _w.get_stringvar("item_name")
        self.LBL_NAME.set(kw.get("item_name") or "sample demo")
        self.OPT_STATUS = _w.get_stringvar("opt_status")
        self.CBO_BEGIN = (
            _w.combo_begin_day,
            _w.combo_begin_month,
            _w.combo_begin_year,
        )
        self.LBL_ERR_BEGIN = _w.get_stringvar("lbl_begin_error")
        self.CBO_END = (
            _w.combo_end_day,
            _w.combo_end_month,
            _w.combo_end_year,
        )
        self.LBL_ERR_END = _w.get_stringvar("lbl_end_error")
        self.COMBOS = self.CBO_BEGIN + self.CBO_END
        self.init_combos(self.CBO_BEGIN, self.CBO_END)
        self.reset_combos(**kw)
        # event bindings
        self.bind_events(**kw)
    # end def


    def reset_combos (self, **kw):
        """
            resets date combos to fit real date values;
        """
        # inits
        _today = date.today()
        _begin = kw.get("date_begin") or _today
        _end = kw.get("date_end") or _today
        # reset dates
        self.reset_date(_begin, self.CBO_BEGIN)
        self.reset_date(_end, self.CBO_END)
    # end def


    def reset_date (self, cdate, group):
        """
            resets @cdate datetime.date object into combo @group;
        """
        # date inits
        _cday = cdate.day
        _cmonth = cdate.month
        _cyear = cdate.year
        # combo inits
        _day, _month, _year = group
        # reset date
        _day.current(_cday - 1)
        _month.current(_cmonth - 1)
        _year.set(_cyear)
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # all is good
        #~ return True
        return False # debugging
    # end def

# end class DateBarDialog
