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
from datetime import timedelta, date
import json
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


    def bbox_add (self, bbox1, bbox2):
        """
            returns coordinates sum of bounding boxes;
        """
        return tuple(map(lambda x: sum(x), zip(bbox1, bbox2)))
    # end def


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
        self.bind("<Button-1>", self.slot_start_drag)
        self.bind("<Motion>", self.slot_drag_pending)
        self.bind("<ButtonRelease-1>", self.slot_drop)
        self.bind("<Control-ButtonRelease-1>", self.slot_remove_item)
        self.bind("<Double-Button-1>", self.slot_double_clicked)
        self.bind("<Control-Button-4>", self.slot_change_date_scale)
        self.bind("<Control-Button-5>", self.slot_change_date_scale)
        self.bind("<Control-MouseWheel>", self.slot_change_date_scale)
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


    def center_x (self):
        """
            returns x coordinates for canvas' center point;
        """
        # return center point x coordinates
        return self.winfo_reqwidth() // 2
    # end def


    def center_xy (self):
        """
            returns (x, y) coordinates for canvas' center point;
        """
        # return center point coordinates
        return (self.center_x(), self.center_y())
    # end def


    def center_y (self):
        """
            returns y coordinates for canvas' center point;
        """
        # return center point y coordinates
        return self.winfo_reqheight() // 2
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


    def dnd_reset (self, *args, **kw):
        """
            event handler for resetting D'n'D feature;
        """
        # inits
        self.drag_mode = 0
        self.drag_tag = ""
        self.drag_start_xy = (0, 0)
        self.drag_last_pos = (0, 0)
        self.auto_scroll = False
    # end def


    def get_bbox_center (self, tag):
        """
            returns (x, y) coordinates of central point for a bbox
            identified by group tag;
        """
        # inits
        _bbox = self.bbox(tag)
        # got bbox?
        if _bbox:
            # get coords
            x1, y1, x2, y2 = _bbox
            # return center xy
            return ((x1 + x2) // 2, (y1 + y2) // 2)
        # end if
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


    def get_group_tag (self, list_ids):
        """
            retrieves group tag from @list_ids;
        """
        # param controls
        if list_ids:
            # get foreground id tags
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


    def get_segment_center (self, start_xy, end_xy):
        """
            returns (x, y) coordinates of central point for a segment;
        """
        # inits
        x0, y0 = start_xy
        x1, y1 = end_xy
        # calculate
        return ((x0 + x1) // 2, (y0 + y1) // 2)
    # end def


    def get_xy_pos (self, cdate, item_name):
        """
            calculates (x, y) coordinates of top left datebar corner;
        """
        # inits
        _dr = self.date_ruler
        _il = self.item_list
        _x = (
            _dr.XY_ORIGIN[0]
            + _dr.tick_offset
            + _dr.get_width(_dr.date_min, cdate)
        )
        _y = _il.get_y_pos(item_name) + 1
        # return top left corner
        return (_x, _y)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # reset date bars
        self.date_bars = dict()
        # drag'n'drop feature
        self.dnd_reset()
        # date ruler feature
        self.date_ruler.reset()
        # item feature
        self.item_list.reset()
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
        # member inits
        self.init_members(**kw)
        # event bindings
        self.bind_events()
    # end def


    def item_list_update (self, item_dict):
        """
            updates list of resource items in canvas;
        """
        # really got items?
        if item_dict:
            # update item list
            self.item_list.fill_list(item_dict)
            # inits
            _w, _h = self.item_list.size
            # update date ruler
            self.date_ruler.update(offset_x=_w - 2)
            # update canvas
            self.update_canvas()
        # better clear all
        else:
            self.reset()
        # end if
    # end def


    def reset (self, *args, **kw):
        """
            resets canvas to new;
        """
        # clear canvas
        self.clear_canvas()
        # reset members
        self.init_members(**kw)
    # end def


    def size_xy (self):
        """
            returns (width, height) coordinates;
        """
        # get coordinates
        return (self.winfo_reqwidth(), self.winfo_reqheight())
    # end def


    def slot_change_date_scale (self, event=None, *args, **kw):
        """
            event handler: Ctrl-MouseWheel changes date scale;
        """
        # param controls
        if event:
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
                # update date ruler
                self.date_ruler.update(scale=_scale)
                # update canvas
                self.update_canvas()
            # end if
        # end if
    # end def


    def slot_datebar_validate (self, *args, **kw):
        """
            event handler: datebar dialog has been submitted;
        """
        print("slot_datebar_validate")
        # inits
        _datebar = kw.get("datebar")
        _item_name = kw.get("item_name")
        _status = kw.get("status")
        _begin, _end = self.date_ruler.get_correct_interval(
            kw.get("date_begin"), kw.get("date_end")
        )
        # resize date ruler if necessary
        self.date_ruler.resize(_begin, _end)
        # new datebar?
        if not _datebar:
            # inits
            _datebar = RCDateBar(
                self,
                rowid=self.item_list.items[_item_name],
                status=_status,
                date_begin=_begin.isoformat(),
                date_end=_end.isoformat(),
            )
            # add new to collection
            self.date_bars[_datebar.tag] = _datebar
        # end if
        # store new data in DB
        self.database.res_update_datebar(
            fk_type=_datebar.rowid,
            status=_datebar.status,
            date_begin=_datebar.date_begin,
            date_end=_datebar.date_end,
        )
        # redraw datebar
        _datebar.draw(_item_name)
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
            _tag = self.get_group_tag(self.find_overlapping(x, y, x, y))
            _datebar = self.date_bars.get(_tag)
            # show dialog
            DLG.DateBarDialog(
                self,
                item_name=_item["name"],
                datebar=_datebar,
            ).show()
        # end if
    # end def


    def slot_drag_pending (self, event=None, *args, **kw):
        """
            event handler: pending D'n'D on mouse motion;
        """
        #~ print("slot_drag_pending")
        # param controls
        if event:
            # dragging something?
            if self.drag_mode:
                # inits
                x, y = self.get_real_pos(event.x, event.y)
                x0, y0 = self.drag_last_pos
                dx, dy = (x - x0), (y - y0)
                # update pos
                self.drag_last_pos = (x, y)
                pass                                                            # FIXME
                # update canvas
                self.update_canvas()
                # scrolling
                self.scan_dragto(event.x, event.y, gain=-1)
            # auto-scrolling mode?
            elif self.auto_scroll:
                # scrolling
                self.scan_dragto(event.x, event.y, gain=-5)
            # end if
        # end if
    # end def


    def slot_drop (self, event=None, *args, **kw):
        """
            event handler: D'n'D dropping on mouse release;
        """
        print("slot_drop")
        # param controls
        if event and self.drag_mode:
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            pass                                                            # FIXME
        # end if
        # reset D'n'D mode
        self.dnd_reset()
        # update canvas
        self.update_canvas()
    # end def


    def slot_remove_item (self, event=None, *args, **kw):
        """
            event handler: mouse Ctrl+Click;
        """
        print("slot_remove_item")
        # param controls
        if event:
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            pass                                                            # FIXME
        # end if
        # reset D'n'D mode
        self.dnd_reset()
        # update canvas
        self.update_canvas()
    # end def


    def slot_start_drag (self, event=None, *args, **kw):
        """
            event handler: mouse Drag-and-drop feature;
        """
        print("slot_start_drag")
        # inits
        self.dnd_reset()
        # got mouse event?
        if event:
            # automatic scrolling feature
            self.scan_mark(event.x, event.y)
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            pass                                                            # FIXME
        # end if
    # end def


    def update_canvas (self, *args, **kw):
        """
            event handler for canvas contents updating;
        """
        # inits
        _bbox = self.bbox("all")
        # got items?
        if _bbox:
            # get all contents bbox
            x0, y0, x1, y1 = _bbox
            _cw, _ch = self.size_xy()
            x0, y0 = (min(0, x0 + 1), min(0, y0 + 1))
            #~ x1, y1 = (max(x1 - 1, _cw), max(y1 - 1, _ch))
            # reset scroll region size
            self.configure(scrollregion=(x0, y0, x1, y1))
            # project has been modified
            #~ self.events.raise_event("Project:Modified")
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
        print("update_datebars")
        # FIXME: should be deferred task?
        pass                                                                # FIXME
    # end def


    def viewport_center_xy (self):
        """
            returns (x, y) real canvas coordinates of viewport's center
            point;
        """
        # inits
        x, y = self.center_xy()
        # viewport's center point
        return (int(self.canvasx(x)), int(self.canvasy(y)))
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


    def draw (self, item_name):
        """
            (re)draws datebar on canvas;
        """
        # ensure no more previous
        self.clear()
        # inits
        _height = self.canvas.date_ruler.RULER_HEIGHT - 2
        _width = self.canvas.date_ruler.get_width(
            self.date_begin, self.date_end
        )
        _x, _y = self.canvas.get_xy_pos(self.date_begin, item_name)
        # draw datebar
        self.canvas.create_rectangle(
            self.canvas.box_rel((_x, _y), _width, _height),
            outline="black",
            fill=self.COLORS[self.status],
            width=1,
            tags=self.tag,
        )
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
        _x1 = _x0 + self.tick_offset
        _y0 += self.RULER_HEIGHT
        _y = _y0 - 5
        _cur_date, _end_date = self.get_correct_interval(
            self.date_min, self.date_max
        )
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
        # adjust tick width
        self.tick_width += self.PAD_X
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


    def get_width (self, date_min, date_max):
        """
            calculates timedelta interval in pixel width along with
            current scale value;
            returns integer value (pixels);
        """
        # inits
        _dmin, _dmax = self.get_correct_interval(date_min, date_max)
        _delta = _dmax - _dmin
        return int(
            self.tick_width * (
                _delta.days / (1.0, 7.0, 30.43685)[self.scale]
            )
        )
    # end def


    def init_members (self, *args, **kw):
        """
            virtual method to be reimplemented in subclass;
        """
        # member inits
        self.date_min = kw.get("date_min")
        self.date_max = kw.get("date_max")
        self.scale = kw.get("scale")
        self.tick_offset = 0
        self.tick_width = 0
    # end def


    def resize (self, date_min, date_max):
        """
            resizes date ruler along with @date_min and @date_max;
            parameters must be of datetime.date type;
        """
        # inits
        date_min, date_max = self.get_correct_interval(
            date_min, date_max
        )
        _inbound = lambda x: self.date_min <= x <= self.date_max
        # out of bounds?
        if not _inbound(date_min) or not _inbound(date_max):
            # must resize
            self.update(
                date_min=min(self.date_min, date_min, date_max),
                date_max=max(self.date_max, date_min, date_max),
            )
        # end if
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
        self.tick_offset = kw.pop("offset_x", self.tick_offset)
        self.scale = kw.pop("scale", self.scale)
        self.date_min = kw.pop("date_min", self.date_min)
        self.date_max = kw.pop("date_max", self.date_max)
        # fill along with scale resolution
        getattr(
            self, "fill_with_{}".format(self.get_scale_name())
        )(*args, **kw)
        # must redraw all current datebars
        self.canvas.update_datebars()
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
            returns y coordinate position for a given @item_name;
            raises error if @item_name is *NOT* in items;
        """
        # return y pos
        return int(
            self.XY_ORIGIN[1] +
            self.sorted_items.index(item_name) * self.LINE_HEIGHT
        )
    # end def


    def init_members (self, *args, **kw):
        """
            virtual method to be reimplemented in subclass;
        """
        # member inits
        self.items = None
        self.sorted_items = list()
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
                    font="sans 10",
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

# end class RCItemList
