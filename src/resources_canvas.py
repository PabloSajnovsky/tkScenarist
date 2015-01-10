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
import os
import json
from calendar import monthrange
from datetime import timedelta, date, datetime
import tkinter.messagebox as MB
import tkinter.simpledialog as SD
import tkRAD.widgets.rad_canvas as RC
from . import dlg_date_bar as DLG


class ResourcesCanvas (RC.RADCanvas):
    """
        Resources planning canvas class;
    """

    # class constant defs
    CONFIG = {
        "background": "grey80",
        "height": None,
        "highlightbackground": "grey20",
        "highlightthickness": 1,
        "takefocus": 0,
        "width": 0,
    } # end of CONFIG


    def bbox_size (self, tag_or_id):
        """
            returns box size (width, height) of bbox(tag_or_id);
        """
        # inits
        _bbox = self.bbox(tag_or_id)
        # got bbox?
        if _bbox:
            # inits
            _x0, _y0, _x1, _y1 = _bbox
            # return box size
            return (abs(_x1 - _x0), abs(_y1 - _y0))
        # end if
        # failed - no dims
        return (0, 0)
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:DateBar:Validate": self.slot_datebar_validate,
            }
        )
        # tkinter event bindings
        self.bind("<Configure>", self.update_canvas)
        self.bind("<Control-ButtonRelease-1>", self.slot_remove_item)
        self.bind("<Double-Button-1>", self.slot_double_clicked)
        # mouse wheel support
        for _b in ("Button-4", "Button-5", "MouseWheel"):
            # tk event bindings
            self.bind(
                "<{}>".format(_b), self.slot_on_mouse_wheel
            )
            self.bind(
                "<Control-{}>".format(_b), self.slot_change_date_scale
            )
        # end for
    # end def


    def box_rel (self, xy0, width, height):
        """
            returns box coordinates relative to @xy0 (x0, y0) point of
            origin and to @width, @height dimensions;
        """
        # inits
        x0, y0 = xy0
        return (x0, y0, x0 + width, y0 + height)
    # end def


    def can_scroll_x (self):
        """
            this is a Tcl/Tk bugfix; returns True if canvas is really
            allowed to operate, False otherwise;
        """
        # inits
        _w = self.bbox_size("all")[0]
        _cw = self.winfo_width()
        # get authorization
        return _w and _w >= _cw - 1
    # end def


    def can_scroll_y (self):
        """
            this is a Tcl/Tk bugfix; returns True if canvas is really
            allowed to operate, False otherwise;
        """
        # inits
        _h = self.bbox_size("all")[1]
        _ch = self.winfo_height()
        # get authorization
        return _h and _h >= _ch - 1
    # end def


    def clear_canvas (self, *args, **kw):
        """
            event handler for clearing up canvas;
        """
        # clear canvas
        self.delete("all")
        self.configure(scrollregion=(0, 0, 0, 0))
        self.xview_moveto(0)
        self.yview_moveto(0)
    # end def


    def get_file_contents (self):
        """
            returns file contents as string of chars;
        """
        # inits
        _dict = dict()
        pass                                                                # FIXME
        return json.dumps(_dict)
    # end def


    def get_group_tag (self, x, y):
        """
            retrieves group tag from real canvas pos @(x, y);
        """
        # init
        list_ids = self.find_overlapping(x, y, x, y)
        # param controls
        if list_ids:
            # get foreground tag id
            _tags = self.gettags(list_ids[-1]) or [""]
            # extract group tag
            return _tags[0]
        # end if
        # failed
        return ""
    # end def


    def get_real_pos (self, x, y):
        """
            returns real position coordinates for canvas viewport
            coordinates;
        """
        return (int(self.canvasx(x)), int(self.canvasy(y)))
    # end def


    def get_xy_pos (self, cdate, item_name):
        """
            calculates (x, y) coordinates of top left datebar corner;
        """
        # inits
        _x = (
            self.date_ruler.XY_ORIGIN[0]
            + self.date_ruler.tick_offset
            + self.date_ruler.get_width(
                self.date_ruler.date_min, cdate
            )
        )
        _y = self.item_list.get_y_pos(item_name)
        # return top left corner
        return (_x, _y)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # reset date bars
        self.date_bars.clear()
        # date ruler feature
        self.date_ruler.reset(**kw)
        # item feature
        self.item_list.reset(**kw)
    # end def


    def init_widget (self, **kw):
        """
            virtual method to be implemented in subclass;
        """
        # database inits
        self.database = self.winfo_toplevel().database
        # date ruler inits
        self.date_ruler = RCDateRuler(self)
        # item list inits
        self.item_list = RCItemList(self)
        # datebar collection inits
        self.date_bars = dict()
        # member inits
        self.init_members(**kw)
        # event bindings
        self.bind_events()
    # end def


    def item_list_update (self, item_dict):
        """
            updates list of resource items in canvas;
        """
        # clear canvas
        self.clear_canvas()
        # really got items?
        if item_dict:
            # update item list
            self.item_list.fill_list(item_dict)
            # get datebars from DB
            self.reset_datebars(item_dict)
            # inits
            _w, _h = self.item_list.size
            # update date ruler + datebars
            self.date_ruler.tick_offset = _w - 2
            self.update_datebars()
        # better clear all (except date ruler's timescale)
        else:
            self.reset(except_scale=True)
        # end if
    # end def


    def reset (self, *args, **kw):
        """
            resets canvas to new;
        """
        print(__class__.__name__, "reset")
        # clear canvas
        self.clear_canvas()
        # reset members
        self.init_members(**kw)
    # end def


    def reset_datebars (self, item_dict):
        """
            reloads datebar data from DB and recreates RCDateBar object
            collection;
        """
        # inits
        self.date_bars.clear()
        # param controls
        if item_dict:
            # get recordset
            _rows = self.database.res_get_datebars(item_dict.values())
            # browse recordset
            for _row in _rows:
                # inits
                _datebar = RCDateBar(
                    self,
                    rowid=_row["fk_type"],
                    tag=_row["tag"],
                    status=_row["status"],
                    date_begin=_row["date_begin"],
                    date_end=_row["date_end"],
                )
                # add to collection
                self.date_bars[_datebar.tag] = _datebar
            # end for
        # end if
    # end def


    def slot_change_date_scale (self, event=None, *args, **kw):
        """
            event handler: Ctrl-MouseWheel changes date scale;
        """
        # allowed to proceed?
        if event and self.bbox("all"):
            # inits
            _scale = self.date_ruler.get_scale_value(
                self.date_ruler.scale
                # scroll down increases scale
                + int(event.num == 5 or event.delta < 0)
                # scroll up decreases scale
                - int(event.num == 4 or event.delta > 0)
            )
            # got to update?
            if _scale != self.date_ruler.scale:
                # return to origin
                self.xview_moveto(0)
                # update date ruler + datebars
                self.date_ruler.scale = _scale
                self.update_datebars()
            # end if
        # end if
    # end def


    def slot_datebar_validate (self, *args, **kw):
        """
            event handler: datebar dialog has been submitted;
        """
        # inits
        _datebar = kw.get("datebar")
        _item_name = kw.get("item_name")
        # new datebar?
        if not _datebar:
            # inits
            _datebar = RCDateBar(
                self,
                rowid=self.item_list.items[_item_name],
            )
            # add new to collection
            self.date_bars[_datebar.tag] = _datebar
        # end if
        # update datebar data
        _datebar.status = kw.get("status")
        _datebar.date_begin, _datebar.date_end = (
            self.date_ruler.get_correct_interval(
                kw.get("date_begin"), kw.get("date_end")
            )
        )
        # store new data in DB
        self.database.res_update_datebar(
            fk_type=_datebar.rowid,
            tag=_datebar.tag,
            status=_datebar.status,
            date_begin=str(_datebar.date_begin),
            date_end=str(_datebar.date_end),
        )
        # must redraw all current datebars
        self.update_datebars()
        # notify app
        self.events.raise_event("Project:Modified")
    # end def


    def slot_double_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse double-clicked;
        """
        # allowed to proceed?
        if event and self.bbox("all"):
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            _item = self.item_list.get_item_from(x, y)
            _tag = self.get_group_tag(x, y)
            _datebar = self.date_bars.get(_tag)
            # show dialog
            DLG.DateBarDialog(
                self,
                item_name=_item["name"],
                datebar=_datebar,
            ).show()
        # end if
    # end def


    def slot_on_mouse_wheel (self, event=None, *args, **kw):
        """
            event handler: mouse wheel support;
        """
        # inits
        _os = os.name.lower()
        # MS-Windows specifics
        if _os == "nt":
            # init step
            _step = -event.delta // 120
        # Apple MacOS specifics
        elif _os == "mac":
            # init step
            _step = -event.delta
        # other POSIX / UNIX-like
        else:
            # init step
            _step = (event.num == 5) - (event.num == 4)
        # end if
        # got <Shift> modifier?
        if event.state & 0x01:
            # do horizontal scrolling
            self.xview_scroll(_step, "units")
        else:
            # do vertical scrolling
            self.yview_scroll(_step, "units")
        # end if
    # end def


    def slot_remove_item (self, event=None, *args, **kw):
        """
            event handler: mouse Ctrl+Click;
        """
        # allowed to proceed?
        if event and self.bbox("all"):
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            _tag = self.get_group_tag(x, y)
            # registered datebar?
            if _tag in self.date_bars:
                # remove from canvas
                _datebar = self.date_bars.pop(_tag)
                _datebar.clear()
                # remove from DB
                self.database.res_del_datebar(_datebar.tag)
                # return to origin
                self.xview_moveto(0)
                # update ruler + datebars
                self.update_datebars()
                # notify app
                self.events.raise_event("Project:Modified")
            # end if
        # end if
    # end def


    def update_canvas (self, *args, **kw):
        """
            event handler for canvas contents updating;
        """
        # ensure visible
        self.update_pos()
        # inits
        _bbox = self.bbox("all")
        # got items?
        if _bbox:
            # get all contents bbox
            x0, y0, x1, y1 = _bbox
            x0, y0 = (min(0, x0 + 1), min(0, y0 + 1))
            # reset scroll region size
            self.configure(scrollregion=(x0, y0, x1, y1))
        # no items
        else:
            # better clean up everything
            self.reset()
        # end if
    # end def


    def update_datebars (self, *args, **kw):
        """
            event handler: updates all present datebars;
        """
        # FIXME: should be deferred task?
        if self.date_bars:
            # inits
            _names = self.item_list.swapped_items
            _dmin = _dmax = None
            # browse collection
            for _datebar in self.date_bars.values():
                # resize bounds
                if _dmin:
                    _dmin = min(_dmin, _datebar.date_begin)
                    _dmax = max(_dmax, _datebar.date_end)
                else:
                    _dmin = _datebar.date_begin
                    _dmax = _datebar.date_end
                # end if
            # end for
            # redraw date ruler
            self.date_ruler.update(date_min=_dmin, date_max=_dmax)
            # browse collection
            for _datebar in self.date_bars.values():
                # redraw datebar
                _datebar.draw(_names[_datebar.rowid])
            # end for
        # no datebars
        else:
            # show default date ruler
            self.date_ruler.update()
        # end if
        # update canvas
        self.update_canvas()
    # end def


    def update_pos (self, *args, **kw):
        """
            event handler: ensures all specific components are always
            visible while scrolling canvas contents;
        """
        # ensure visible
        self.item_list.update_pos()
        self.date_ruler.update_pos()
    # end def


    def xview (self, *args):
        """
            hack for components visibility on contents scrolling;
        """
        # Tcl/Tk bugfix
        if self.can_scroll_x():
            # delegate to super
            super().xview(*args)
            # ensure visible components
            self.update_pos()
        # end if
    # end def


    def xview_moveto (self, *args):
        """
            hack for components visibility on contents scrolling;
        """
        # Tcl/Tk bugfix
        if self.can_scroll_x():
            # delegate to super
            super().xview_moveto(*args)
            # ensure visible components
            self.update_pos()
        # end if
    # end def


    def xview_scroll (self, *args):
        """
            hack for components visibility on contents scrolling;
        """
        # Tcl/Tk bugfix
        if self.can_scroll_x():
            # delegate to super
            super().xview_scroll(*args)
            # ensure visible components
            self.update_pos()
        # end if
    # end def


    def yview (self, *args):
        """
            hack for components visibility on contents scrolling;
        """
        # Tcl/Tk bugfix
        if self.can_scroll_y():
            # delegate to super
            super().yview(*args)
            # ensure visible components
            self.update_pos()
        # end if
    # end def


    def yview_moveto (self, *args):
        """
            hack for components visibility on contents scrolling;
        """
        # Tcl/Tk bugfix
        if self.can_scroll_y():
            # delegate to super
            super().yview_moveto(*args)
            # ensure visible components
            self.update_pos()
        # end if
    # end def


    def yview_scroll (self, *args):
        """
            hack for components visibility on contents scrolling;
        """
        # Tcl/Tk bugfix
        if self.can_scroll_y():
            # delegate to super
            super().yview_scroll(*args)
            # ensure visible components
            self.update_pos()
        # end if
    # end def

# end class ResourcesCanvas



class RCCanvasItem:
    """
        Resources Canvas CanvasItem base class;
    """

    def __init__ (self, canvas, **kw):
        """
            class constructor;
        """
        # member inits
        self.canvas = canvas
        self.tag = kw.get("tag")
        self.tag_labels = "{}_labels".format(self.tag)
        # other inits
        self.init_members(**kw)
    # end def


    def clear (self, *args, **kw):
        """
            clears component on canvas;
        """
        # clear component
        self.canvas.delete(self.tag, self.tag_labels)
    # end def


    def init_members (self, *args, **kw):
        """
            virtual method to be reimplemented in subclass;
        """
        # member inits
        pass
    # end def


    def reset (self, *args, **kw):
        """
            resets component on canvas;
        """
        # ensure no more previous
        self.clear(*args, **kw)
        # reset members
        self.init_members(*args, **kw)
    # end def


    @property
    def tag (self):
        """
            property attribute;
            must be a string;
            defaults to '{classname}#{id(self)}' on incorrect value;
        """
        return self.__tag
    # end def

    @tag.setter
    def tag (self, value):
        # must be a string of chars
        if value and isinstance(value, str):
            # inits
            self.__tag = value
        else:
            # default
            self.__tag = (
                "{}#{}".format(self.__class__.__name__, id(self))
            )
        # end if
    # end def

    @tag.deleter
    def tag (self):
        del self.__tag
    # end def

# end class RCCanvasItem



class RCDateBar (RCCanvasItem):
    """
        Resources Canvas Date Bar component class;
    """

    # class constant defs
    COLORS = {
        "OK": "royal blue",
        "N/A": "firebrick",
    }


    @property
    def date_begin (self):
        """
            property attribute;
            admits datetime.date type or ISO 8601 'YYYY-MM-DD'
            formatted string in input;
        """
        return self.__date_begin
    # end def

    @date_begin.setter
    def date_begin (self, value):
        if isinstance(value, date):
            self.__date_begin = value
        elif value and isinstance(value, str):
            self.__date_begin = self.get_iso_date(value)
        elif value is not None:
            raise TypeError(
                "attribute 'date_begin' must be of "
                "datetime.date type or at least an "
                "ISO 8601 'YYYY-MM-DD' formatted "
                "string value in input."
            )
        # end if
    # end def

    @date_begin.deleter
    def date_begin (self):
        del self.__date_begin
    # end def


    @property
    def date_end (self):
        """
            property attribute;
            admits datetime.date type or ISO 8601 'YYYY-MM-DD'
            formatted string in input;
        """
        return self.__date_end
    # end def

    @date_end.setter
    def date_end (self, value):
        if isinstance(value, date):
            self.__date_end = value
        elif value and isinstance(value, str):
            self.__date_end = self.get_iso_date(value)
        elif value is not None:
            raise TypeError(
                "attribute 'date_end' must be of "
                "datetime.date type or at least an "
                "ISO 8601 'YYYY-MM-DD' formatted "
                "string value in input."
            )
        # end if
    # end def

    @date_end.deleter
    def date_end (self):
        del self.__date_end
    # end def


    def draw (self, item_name):
        """
            (re)draws datebar on canvas;
        """
        # ensure no more previous
        self.clear()
        # inits
        _height = int(self.canvas.item_list.LINE_HEIGHT * 0.8)
        _width = self.canvas.date_ruler.get_width(
            self.date_begin, self.date_end,
            overlap=1 # last day is *INCLUDED*
        )
        _x, _y = self.canvas.get_xy_pos(self.date_begin, item_name)
        _y -= _height // 2 - 2
        # draw datebar
        self.canvas.create_rectangle(
            self.canvas.box_rel((_x, _y), _width, _height),
            outline="black",
            fill=self.COLORS[self.status],
            width=1,
            tags=self.tag,
        )
    # end def


    def get_iso_date (self, date_str):
        """
            tries to convert an ISO 8601 'YYYY-MM-DD' formatted string
            to a regular datetime.date object;
            returns object on success, raises error otherwise;
        """
        # inits
        _dt = datetime.strptime(date_str, "%Y-%m-%d")
        return date(_dt.year, _dt.month, _dt.day)
    # end def


    def init_members (self, *args, **kw):
        """
            virtual method to be reimplemented in subclass;
        """
        # member inits
        self.rowid = kw.get("rowid")
        self.status = kw.get("status")
        self.date_begin = kw.get("date_begin")
        self.date_end = kw.get("date_end")
    # end def

# end class RCDateBar



class RCDateRuler (RCCanvasItem):
    """
        Resources Canvas Date Ruler component class;
    """

    # class constant defs
    FONT = "sans 8"
    PAD_X = 5
    RULER_HEIGHT = 24
    SCALES = ("days", "weeks", "months")
    XY_ORIGIN = (0, 0)


    @property
    def date_max (self):
        """
            property attribute;
            admits only instances of datetime.date class;
            defaults to date.today() + 7 days if set to incorrect value;
        """
        return self.__date_max
    # end def

    @date_max.setter
    def date_max (self, value):
        # must be an instance of datetime.date class
        if isinstance(value, date):
            # inits
            self.__date_max = value
        # go to default value
        else:
            # defaults to today() + 7 days
            self.__date_max = date.today() + timedelta(days=7)
        # end if
    # end def

    @date_max.deleter
    def date_max (self):
        del self.__date_max
    # end def


    @property
    def date_min (self):
        """
            property attribute;
            admits only instances of datetime.date class;
            defaults to date.today() if set to incorrect value;
        """
        return self.__date_min
    # end def

    @date_min.setter
    def date_min (self, value):
        # must be an instance of datetime.date class
        if isinstance(value, date):
            # inits
            self.__date_min = value
        # go to default value
        else:
            # defaults to today()
            self.__date_min = date.today()
        # end if
    # end def

    @date_min.deleter
    def date_min (self):
        del self.__date_min
    # end def


    def draw_ruler (self, *args, **kw):
        """
            really draws ruler along with callback functions; requires
            'get_date_label' and 'next_date' keywords / callback
            functions; callback function must admit a datetime.date
            object as unique input parameter;
        """
        # inits
        self.tick_width = 0
        _cb_label = kw.get("get_date_label")
        _cb_next = kw.get("next_date")
        _labels = list()
        _x0, _y0 = self.XY_ORIGIN
        _y0 += self.RULER_HEIGHT
        _y = _y0 - 5
        _cur_date, _end_date = self.get_correct_interval(
            self.date_min, self.date_max
        )
        # add one more tick to include overflows
        _end_date = _cb_next(_end_date)
        # clear ruler
        self.clear()
        # loop till reached
        while _cur_date <= _end_date:
            # insert text label
            _id = self.canvas.create_text(
                _x0, _y,
                anchor="s",
                fill="black",
                font=self.FONT,
                text=_cb_label(_cur_date),
                tags=(self.tag, self.tag_labels),
            )
            # add to list
            _labels.append(_id)
            # get size
            _w, _h = self.canvas.bbox_size(_id)
            # compute adjustments
            self.tick_width = max(_w, self.tick_width)
            # next date
            _cur_date = _cb_next(_cur_date)
        # end while
        # adjust tick width and offset
        self.tick_width += self.PAD_X
        self.tick_offset = max(
            self.tick_width // 2 + self.PAD_X, self.tick_offset
        )
        _x1 = _x0 + self.tick_offset
        # browse labels
        for _index, _id in enumerate(_labels):
            # inits
            _x = _x1 + _index * self.tick_width
            # reset pos
            self.canvas.coords(_id, _x, _y)
            # draw tick
            self.canvas.create_line(
                _x, _y0, _x, _y0 - 3,
                fill="black",
                tags=(self.tag, self.tag_labels),
                width=1,
            )
        # end for
        # draw frame
        self.frame_id = self.canvas.create_rectangle(
            _x0, _y0,
            self.canvas.bbox(self.tag_labels)[2],
            _y0 - self.RULER_HEIGHT,
            outline="black",
            fill="grey90",
            width=1,
            tags=self.tag,
        )
        # raise ruler above all
        self.canvas.tag_raise(self.tag, "all")
        self.canvas.tag_raise(self.tag_labels, self.frame_id)
    # end def


    def fill_with_days (self, *args, **kw):
        """
            fills ruler with day values between date min and date max;
        """
        # call with callbacks
        self.draw_ruler(
            *args,
            get_date_label=lambda d: d.strftime("%a %x"),
            next_date=lambda d: d + timedelta(days=1),
            **kw
        )
    # end def


    def fill_with_months (self, *args, **kw):
        """
            fills ruler with month values between date min and date max;
        """
        # subfunction def
        def next_month (cdate):
            # inits
            _y = cdate.year
            _m = cdate.month + 1
            _d = cdate.day
            # overflow?
            if _m > 12:
                _y += 1
                _m = 1
            # end if
            return date(_y, _m, _d)
        # end def
        # call with callbacks
        self.draw_ruler(
            *args,
            get_date_label=lambda d: d.strftime("%b %Y"),
            next_date=next_month,
            **kw
        )
    # end def


    def fill_with_weeks (self, *args, **kw):
        """
            fills ruler with week values between date min and date max;
        """
        # call with callbacks
        self.draw_ruler(
            *args,
            get_date_label=lambda d: d.strftime("%a %x"),
            next_date=lambda d: d + timedelta(days=7),
            **kw
        )
    # end def


    def get_correct_interval (self, date_min, date_max):
        """
            returns a formatted tuple of dates to match a correct time
            interval; parameters must be of datetime.date type;
        """
        # param controls
        if date_min > date_max:
            return (date_max, date_min)
        else:
            return (date_min, date_max)
        # end if
    # end def


    def get_scale_name (self, scale=None):
        """
            returns scale name along with @scale value, if given or
            along with self.scale otherwise;
            admitted values are 0 (days), 1 (weeks) and 2 (months);
        """
        return self.SCALES[
            self.get_scale_value(
                self.scale if scale is None else scale
            )
        ]
    # end def


    def get_scale_value (self, value):
        """
            rebinds @value such as 0 <= @value < len(self.SCALES);
            defaults to 0 on incorrect @value;
        """
        # must be an integer
        try:
            return max(0, min(len(self.SCALES) - 1, int(value)))
        except:
            # default to nil
            return 0
        # end try
    # end def


    def get_width (self, date_min, date_max, overlap=0):
        """
            calculates timedelta interval in pixel width along with
            current scale value;
            parameter @overlap is number of days to include on more;
            returns integer value (pixels);
        """
        # inits
        _dmin, _dmax = self.get_correct_interval(date_min, date_max)
        _delta = _dmax - _dmin
        _days = _delta.days + overlap
        # scale is DAYS
        if not self.scale:
            return int(self.tick_width * _days)
        # scale is WEEKS
        elif self.scale == 1:
            return int(self.tick_width * _days / 7.0)
        # scale is MONTHS
        elif self.scale == 2:
            # inits
            _months = int(
                (_dmax.year - _dmin.year) * 12
                + _dmax.month - _dmin.month
            )
            _days = _dmax.day / monthrange(_dmax.year, _dmax.month)[-1]
            print("months:", _months)
            print("date:", _dmax, monthrange(_dmax.year, _dmax.month))
            return int(self.tick_width * (_months + _days))
        # end if
    # end def


    def init_members (self, *args, **kw):
        """
            virtual method to be reimplemented in subclass;
        """
        # member inits
        self.date_min = kw.get("date_min")
        self.date_max = kw.get("date_max")
        if not kw.get("except_scale"):
            self.scale = kw.get("scale")
        # end if
        self.tick_offset = 0
        self.tick_width = 0
    # end def


    @property
    def scale (self):
        """
            property attribute;
            admits only integers;
            is automatically rebound to 0 <= s < len(self.SCALES);
            defaults to 0 on incorrect values;
        """
        return self.__scale
    # end def

    @scale.setter
    def scale (self, value):
        # inits
        self.__scale = self.get_scale_value(value)
    # end def

    @scale.deleter
    def scale (self):
        del self.__scale
    # end def


    def update (self, *args, **kw):
        """
            fills date ruler with new values along with scale
            resolution, e.g. scale=0 (days), scale=1 (weeks), scale=2
            (months);
            admits 'date_min' and 'date_max' keywords;
            dates must be of Python's datetime.date() format;
        """
        # inits
        self.date_min = kw.pop("date_min", None)
        self.date_max = kw.pop("date_max", None)
        # fill along with scale resolution
        getattr(
            self, "fill_with_{}".format(self.get_scale_name())
        )(*args, **kw)
    # end def


    def update_pos (self, *args, **kw):
        """
            ensures component is always visible while scrolling canvas
            contents;
        """
        # try out
        try:
            # reset pos
            self.canvas.move(
                self.tag,
                0,
                self.canvas.canvasy(0)
                - self.canvas.bbox(self.tag)[1]
            )
            # set to foreground
            self.canvas.tag_raise(self.tag, "all")
        except:
            pass
        # end try
    # end def

# end class RCDateRuler



class RCItemList (RCCanvasItem):
    """
        Resources Canvas Item List component class;
    """

    # class constant defs
    LINE_HEIGHT = 20
    XY_ORIGIN = (0, RCDateRuler.RULER_HEIGHT)


    def get_item_from (self, x, y):
        """
            retrieves item from given (x, y) canvas coordinates;
        """
        # got items?
        if self.items:
            # inits
            _x0, _y0 = self.XY_ORIGIN
            # only need y
            _index = min(
                len(self.items) - 1,
                max(0, y - _y0) // self.LINE_HEIGHT
            )
            _name = self.sorted_items[_index]
            # return item
            return dict(name=_name, rowid=self.items[_name])
        # end if
    # end def


    def get_y_pos (self, item_name):
        """
            returns y coordinate of central axis for a given
            @item_name; raises error if @item_name is *NOT* in items;
        """
        # return y pos
        return int(
            self.XY_ORIGIN[1] +
            (self.sorted_items.index(item_name) + 0.5) *
            self.LINE_HEIGHT
        )
    # end def


    def init_members (self, *args, **kw):
        """
            virtual method to be reimplemented in subclass;
        """
        # member inits
        self.items = None
        self.sorted_items = None
        self.swapped_items = None
    # end def


    def fill_list (self, item_dict):
        """
            fills list with items in @item_dict;
        """
        # clear all
        self.reset()
        # got items?
        if item_dict:
            # inits
            self.items = item_dict
            self.sorted_items = sorted(item_dict)
            self.swapped_items = dict(
                zip(item_dict.values(), item_dict.keys())
            )
            _x0, _y0 = self.XY_ORIGIN
            # adjust coords
            _x0 += 5
            _y0 += 5
            # browse items
            for _index, _item in enumerate(self.sorted_items):
                # add text label
                self.canvas.create_text(
                    _x0, _y0 + _index * self.LINE_HEIGHT,
                    anchor="nw",
                    fill="black",
                    font="sans 9",
                    text=_item,
                    tags=(self.tag, self.tag_labels),
                )
            # end for
            # update box size
            _w, _h = self.canvas.bbox_size(self.tag_labels)
            # draw frame
            self.frame_id = self.canvas.create_rectangle(
                self.canvas.box_rel(self.XY_ORIGIN, _w + 10, _h + 10),
                outline="black",
                fill="grey90",
                width=1,
                tags=self.tag,
            )
            # raise tags upon any other
            self.canvas.tag_raise(self.tag, "all")
            self.canvas.tag_raise(self.tag_labels, self.frame_id)
        # end if
    # end def


    @property
    def size (self):
        """
            property attribute;
            read-only size (width, height);
        """
        return self.canvas.bbox_size(self.tag)
    # end def


    def update_pos (self, *args, **kw):
        """
            ensures component is always visible while scrolling canvas
            contents;
        """
        # try out
        try:
            # reset pos
            self.canvas.move(
                self.tag,
                self.canvas.canvasx(0) - self.canvas.bbox(self.tag)[0],
                0
            )
            # set to foreground
            self.canvas.tag_raise(self.tag, "all")
        except:
            pass
        # end try
    # end def

# end class RCItemList
