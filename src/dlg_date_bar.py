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
from calendar import monthrange
from datetime import date
from calendar import month_name
import tkRAD.widgets.rad_dialog as DLG


class DateBarDialog (DLG.RADButtonsDialog):
    """
        Resources Planning Date Bar edition dialog;
    """

    # class constant defs
    BUTTONS = ("OK", "Cancel")


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
        # browse combos
        for _cbo in self.CBO_BEGIN[1:]:
            _cbo.bind(
                "<<ComboboxSelected>>", self.slot_combo_begin_selected
            )
        # end for
        # browse combos
        for _cbo in self.CBO_END[1:]:
            _cbo.bind(
                "<<ComboboxSelected>>", self.slot_combo_end_selected
            )
        # end for
    # end def


    def get_date (self, group):
        """
            tries to retrieve a datetime.date object from date data
            stored in @group; returns datetime.date(year, month, 1) on
            failure;
        """
        # inits
        _day, _month, _year = group
        _y = int(_year.get())
        _m = _month.current() + 1
        try:
            # retrieve current date
            return date(_y, _m, int(_day.get()))
        except:
            # retrieve default date
            return date(_y, _m, 1)
        # end try
    # end def


    def get_days (self, cdate):
        """
            retrieves a formatted days range from @cdate.year and
            @cdate.month e.g. [01..28] for February, [01..31] for March
            and so on;
        """
        return [
            "{:02d}".format(i)
            for i in range(
                1, monthrange(cdate.year, cdate.month)[1] + 1
            )
        ]
    # end def


    def init_combos (self, *groups):
        """
            sets default values for date combos groups;
            group is combo tuple(day, month, year);
        """
        # inits
        _days = self.get_days(date.today())
        _months = list(month_name)[1:]
        _year = date.today().year
        _years = list(range(_year - 1, _year + 2))
        # browse groups
        for _group in groups:
            # inits
            _day, _month, _year = _group
            # day values
            _day.configure(values=_days, state="readonly")
            _day.current(0)
            # month values
            _month.configure(values=_months, state="readonly")
            _month.current(0)
            # year values
            _year.configure(values=_years, state="readonly")
            _year.current(0)
        # end for
    # end def


    def init_widget (self, **kw):
        """
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_date_bar.xml
            xml="dlg_date_bar",
        )
        # member inits
        self.datebar = kw.get("datebar")
        _w = self.container
        self.LBL_NAME = _w.get_stringvar("item_name")
        self.LBL_NAME.set(kw.get("item_name") or "sample demo")
        self.OPT_STATUS = _w.get_stringvar("opt_status")
        self.OPT_STATUS.set(
            self.datebar and self.datebar.status == "N/A" and "N/A"
            or "OK"
        )
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
        if self.datebar:
            _begin = self.datebar.date_begin
            _end = self.datebar.date_end
        else:
            _begin = _today
            _end = _today
        # end if
        # reset dates
        self.reset_date(_begin, self.CBO_BEGIN)
        self.reset_date(_end, self.CBO_END)
    # end def


    def reset_date (self, cdate, group):
        """
            resets @cdate datetime.date object into combo @group;
        """
        # date inits
        _year = date.today().year
        _ymin = min(_year - 1, cdate.year)
        _ymax = max(_year + 5, cdate.year)
        # combo inits
        _day, _month, _year = group
        # reset date
        _day.configure(values=self.get_days(cdate))
        _day.current(cdate.day - 1)
        _month.current(cdate.month - 1)
        _year.configure(values=list(range(_ymin, _ymax + 1)))
        _year.set(cdate.year)
    # end def


    def slot_combo_begin_selected (self, event=None, *args, **kw):
        """
            event handler: combobox item has been selected;
        """
        # update days range
        self.update_days_range(self.CBO_BEGIN)
    # end def


    def slot_combo_end_selected (self, event=None, *args, **kw):
        """
            event handler: combobox item has been selected;
        """
        # update days range
        self.update_days_range(self.CBO_END)
    # end def


    def update_days_range (self, group):
        """
            updates days range for new (year, month) values in @group;
        """
        # inits
        _days = self.get_days(self.get_date(group))
        _day = group[0]
        _index = _day.current()
        _day.configure(values=_days)
        _day.current(min(_index, len(_days) - 1))
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        """
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # inits
        _begin = self.get_date(self.CBO_BEGIN)
        _end = self.get_date(self.CBO_END)
        # incorrect interval?
        if _begin > _end:
            # swap dates
            _begin, _end = _end, _begin
        # end if
        # notify app
        self.events.raise_event(
            "Dialog:DateBar:Validate",
            datebar=self.datebar,
            item_name=self.LBL_NAME.get(),
            status=self.OPT_STATUS.get(),
            date_begin=_begin,
            date_end=_end,
        )
        # all is good
        return True
    # end def

# end class DateBarDialog
