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
import gc
from tkinter import ttk
import tkRAD.core.async as ASYNC
import tkRAD.widgets.rad_canvas as RC


class DBViewCanvas (RC.RADCanvas):
    """
        Database View canvas class;
    """

    # class constant defs
    CONFIG = {
        "bg": "white",
        "height": 300,
        "highlightbackground": "grey80",
        "highlightthickness": 0,
        "width": 600,
    } # end of CONFIG

    CONFIG_FIELD = {

        "body": {
            "align": "left",
            "font": "sans 10",
        },

        "header": {
            "align": "center",
            "font": "sans 11 bold",
            "width": 0,
        },
    }

    FIELD_ALIGN = {
        "left": "w",
        "right": "e",
    }


    def _do_set_field_options (self, group_tag, name, **options):
        """
            protected method def for internal use;
        """
        # param controls
        if group_tag in self.field_options:
            # inits
            _options = self.field_options[group_tag].get(name) or \
                                    self.CONFIG_FIELD[group_tag].copy()
            # override new options
            _options.update(options)
            # last but not least
            _options.update(name=name)
            # update field options
            self.field_options[group_tag][name] = _options
        # end if
    # end def


    def _do_update_canvas (self):
        """
            protected method def for internal use;
        """
        # inits
        _bbox = self.bbox("all")
        # got items?
        if _bbox:
            # reset scroll region size
            self.configure(scrollregion=_bbox)
        # no items
        else:
            # better clean up everything
            self.reset()
        # end if
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        #~ self.events.connect_dict(
            #~ {
                #~ "DBView:Test": self.slot_test_session,
            #~ }
        #~ )
        # tkinter event bindings
        # mouse wheel support
        for _seq in ("<Button-4>", "<Button-5>", "<MouseWheel>"):
            # tk event bindings
            self.bind_all(_seq, self.slot_on_mouse_wheel)
        # end for
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


    def destroy (self, *args, **kw):
        """
            event handler: tkinter widget destruction procedure;
        """
        # unbind events first
        self.unbind_events()
        # reset all for faster widget destruction
        self.reset()
        # then delegate to super class
        super().destroy(*args, **kw)
    # end def


    def ensure_visible_header (self, *args, **kw):
        """
            event handler: ensures header frame is always visible while
            scrolling canvas vertically;
        """
        # try out
        try:
            # reset pos
            _bbox = self.bbox("header")
            if _bbox:
                x0, y0, x1, y1 = _bbox
                y = self.canvasy(-0.5)
                self.move("header", 0, y - y0)
            # end if
            # set to foreground
            self.tag_raise("header", "all")
        except:
            pass
        # end try
    # end def


    def get_bbox_size (self, tag_or_id):
        """
            returns (width, height) bbox size along with @tag_or_id;
        """
        # inits
        _bbox = self.coords(tag_or_id)
        # got something?
        if _bbox:
            # init coords
            x0, y0, x1, y1 = _bbox
            # return size
            return (abs(x1 - x0), abs(y1 - y0))
        # end if
        # failed
        return (0, 0)
    # end def


    def get_field_options (self, group_tag, name):
        """
            retrieves field options for @group_tag and field @name;
        """
        # group_tag exists?
        if group_tag in self.field_options:
            # return options by field name
            return self.field_options[group_tag].get(name)
        # unsupported
        else:
            # no options
            return dict()
        # end if
    # end def


    def get_grid_tags (self, radix, index):
        """
            composes a grid tag name along with @radix and @index;
        """
        # inits
        _tag = "{}#{}".format(radix, index)
        # return tag, label tag, box tag
        return dict(
            tag=_tag,
            label="label_" + _tag,
            box="box_" + _tag
        )
    # end def


    def get_insertion_xy (self, row, column):
        """
            returns text (x, y) top left corner coordinates for
            insertion point;
        """
        # inits
        x, y = (0, 0)
        _rtag = self.get_grid_tags("row", row)["tag"]
        _ctag = self.get_grid_tags("column", column)["tag"]
        # calculate y along row
        _box = self.coords(_rtag)
        if _box:
            y = _box[1]
        else:
            y = self.gridman["rows"].get("next_y") or 0
        # end if
        # calculate x along column
        _box = self.coords(_ctag)
        if _box:
            x = _box[0]
        else:
            x = self.gridman["columns"].get("next_x") or 0
        # end if
        # return results
        return (x, y)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.async = ASYNC.get_async_manager()
        self.field_sequence = None
        self.field_options = dict(body=dict(), header=dict())
        self.column_index = 0
        self.row_index = 0
        self.gridman = dict(rows=dict(), columns=dict())
    # end def


    def init_widget (self, **kw):
        r"""
            virtual method to be implemented in subclass;
        """
        # member inits
        self.init_members(**kw)
        # event bindings
        self.bind_events()
    # end def


    def insert_label (self, group_tag, **kw):
        """
            inserts a text label into virtual grid;
        """
        # inits
        _row = kw.get("row") or self.row_index
        _column = kw.get("column") or self.column_index
        _rtags = self.get_grid_tags("row", _row)
        _ctags = self.get_grid_tags("column", _column)
        x, y = self.get_insertion_xy(_row, _column)
        # next column
        if kw.get("column") is None:
            # update pos
            self.column_index += 1
        # end if
        # update canvas
        self.update_canvas()
    # end def


    def insert_row (self, row_dict, row_index=None):
        """
            inserts a given @row_dict into data body at @row_index
            line, starting from 0;
        """
        # param inits
        if row_index is None:
            # reset value
            row_index = self.row_index
            # set next row
            self.next_row()
        # end if
        # browse field names
        for _column, _name in enumerate(self.field_sequence):
            # inits
            _data = str(row_dict.get(_name) or "")
            # get field options
            _opts = self.get_field_options("body", _name)
            # create label
            self.insert_label(
                "body", row=row_index, column=_column, text=_data,
                **_opts
            )
        # end for
    # end def


    def next_row (self, *args, **kw):
        """
            event handler: sets indices for next row label insertion;
        """
        # inits
        self.row_index += 1
        self.column_index = 0
    # end def


    def reset (self, *args, **kw):
        """
            event handler: resets all in widget;
        """
        # stop pending threads
        self.async.stop(
            self._do_update_canvas,
        )
        # clear canvas
        self.clear_canvas(*args, **kw)
        # reset members
        self.init_members(**kw)
        # force garbage collection
        gc.collect()
    # end def


    def set_field_options (self, group_tag, name, **options):
        """
            sets @options for a given field @name;
        """
        # param controls
        if name in self.field_sequence:
            # inits
            group_tag = str(group_tag).lower()
            # body options
            if group_tag in ("body", "both", "all"):
                # set options for body field name
                self._do_set_field_options("body", name, **options)
            # end if
            # header options
            if group_tag in ("header", "both", "all"):
                # set options for header field name
                self._do_set_field_options("header", name, **options)
            # end if
            # return all options
            return self.field_options
        # end if
    # end def


    def set_header (self, *names, **options):
        """
            resets view and rebuilds along with new field @names and
            @options;
        """
        # reset all
        self.reset()
        # update field names ordered sequence
        self.field_sequence = names
        # browse names
        for _name in names:
            # init specific / generic options
            _options = options.get(_name) or options
            # set field options
            _opts = self.set_field_options("all", _name, **_options)
            # set header label
            self.insert_label(
                "header",
                text=_(_name),          # i18n support for header names
                **_opts["header"][_name]
            )
        # end for
        # new line
        self.next_row()
    # end def


    def slot_on_mouse_wheel (self, event=None, *args, **kw):
        r"""
            event handler: mouse wheel support;
        """
        # inits
        _platform = os.name.lower()
        # MS-Windows specifics
        if _platform == "nt":
            # init step
            _step = -event.delta // 120
        # Apple MacOS specifics
        elif _platform == "mac":
            # init step
            _step = -event.delta
        # other POSIX / UNIX-like
        else:
            # init step
            _step = (event.num == 5) - (event.num == 4)
        # end if
        # do vertical scrolling
        self.yview_scroll(_step, "units")
    # end def


    def unbind_events (self, **kw):
        """
            event unbindings;
        """
        # CAUTION: tkRAD event unbindings are automatic
        # tkinter event unbindings
        # mouse wheel support
        for _seq in ("<Button-4>", "<Button-5>", "<MouseWheel>"):
            # tk event unbindings
            self.unbind_all(_seq)
        # end for
    # end def


    def update_canvas (self, *args, **kw):
        """
            event handler for canvas contents updating;
        """
        # deferred task
        self.async.run_after_idle(self._do_update_canvas)
    # end def


    def update_grid (self, group_tag, section, tags, index, dimension, **kw):
        """
            updates all grid dimensions along with new parameters;
        """
        # param controls
        if section in self.gridman:
            # update keywords
            self.gridman[section].update(kw)
            # update dimension
            _tag = tags.get("tag")
            _dim0 = self.gridman[section].get(_tag) or 0
            _dim1 = max(dimension, _dim0)
            self.gridman[section][_tag] = _dim1
            # got to update all dims in section?
            if dimension != _dim0:
                # do move labels
                _seq = self.gridman[section].setdefault(
                    "sequence", list()
                )
                # new tag?
                if _tag not in _seq:
                    # insert tag into sequence
                    _seq.insert(index, _tag)
                # end if
                # inits
                dd = _dim1 - _dim0
                dx, dy = {"rows": (0, dd), "columns": (dd, 0)}[section]
                # move by tags
                for _t in _seq[index + 1:]:
                    self.move(_t, dx, dy)
                # end for
                # resize cells
                _index = {"rows": -1, "columns": -2}[section]
                for _id in self.find_withtag(tags["box"]):
                    # resize relative to coordinates
                    _coords = self.coords(_id)
                    _coords[_index] = _coords[_index - 2] + _dim1
                    self.coords(_id, *_coords)
                    # got text alignment?
                    if _anchor:
                        # inits
                        x0, y0, x1, y1 = _coords
                        # align center?
                        if _anchor == "center":
                            # box center
                            x, y = ((x0 + x1)//2, (y0 + y1)//2)
                            self.coords(_id, x, y)
                            self.itemconfigure(_id, anchor="center")
                        # align right hand?
                        elif "e" in _anchor:
                            # box padding
                            xb, yb = self.LABEL_BOX[-2:]
                            x, y = (x1 - xb, y1 - yb)
                            self.coords(_id, x, y)
                            self.itemconfigure(_id, anchor="se")
                        # end if
                    # end if
                # end for
            # end if
        # end if
    # end def


    def yview (self, *args):
        """
            hack for header visibility;
        """
        # delegate to super
        super().yview(*args)
        # ensure header is always visible
        self.ensure_visible_header()
    # end def


    def yview_moveto (self, *args):
        """
            hack for header visibility;
        """
        # delegate to super
        super().yview_moveto(*args)
        # ensure header is always visible
        self.ensure_visible_header()
    # end def


    def yview_scroll (self, *args):
        """
            hack for header visibility;
        """
        # delegate to super
        super().yview_scroll(*args)
        # ensure header is always visible
        self.ensure_visible_header()
    # end def

# end class DBViewCanvas



class DBViewLabel:
    """
        DBView grid cell structure;
        Simplifies resizing and text alignment features;
    """

    # class constant defs

    BOX_OPTIONS = {
        "fill": "white",
        "outline": "black",
        "width": 1,
    }

    LABEL_BOX = (-5, -5, +5, +5)

    TEXT_OPTIONS = {
        "align": "left",
        "fill": "black",
        "font": "sans 10",
        "width": None,
    }


    def __init__ (self, dbviewcanvas, **kw):
        """
            class constructor;
        """
        # instance safe inits
        self.__box_options = self.BOX_OPTIONS.copy()
        self.__text_options = self.TEXT_OPTIONS.copy()
        # member inits
        self.canvas = dbviewcanvas
        self.on_width_changed = kw.get("on_width_changed")
        self.on_height_changed = kw.get("on_height_changed")
        self.text_options = kw.get("text_options")
        self.box_options = kw.get("box_options")
        self.id_box = 0
        self.id_text = 0
    # end def


    def box_add (self, *boxes):
        """
            returns coordinates sum of many boxes;
        """
        return tuple(map(lambda x: sum(x), zip(*boxes)))
    # end def


    @property
    def box_options (self):
        """
            internal property def;
        """
        # return private member
        return self.__box_options
    # end def

    @box_options.setter
    def box_options (self, options):
        # got overridings?
        if options:
            # override defaults
            self.__box_options.update(options)
        # end if
    # end def

    @box_options.deleter
    def box_options (self):
        # delete private member
        del self.__box_options
    # end def


    def box_size (self, box):
        """
            returns (width, height) size of given @box;
        """
        # param controls
        if box:
            # inits
            x0, y0, x1, y1 = box
            # return (width, height)
            return (abs(x1 - x0), abs(y1 - y0))
        # no box
        else:
            # no size
            return (0, 0)
        # end if
    # end def


    def configure_box (self, **box_options):
        """
            configures box canvas item only;
        """
        # param inits
        self.box_options = box_options
        # item exists?
        if self.id_box:
            # configure canvas item
            self.canvas.itemconfigure(self.id_box, **self.box_options)
        # end if
    # end def


    def configure_text (self, text, **text_options):
        """
            configures text canvas item only;
        """
        # param inits
        self.text_options = text_options
        # item exists?
        if self.id_text:
            # configure canvas item
            self.canvas.itemconfigure(
                self.id_text, text=text, **self.text_options
            )
            # update surrounding box frame along with new constraints
            self.update_box()
        # end if
    # end def


    def create_label (self, left_x, top_y, text, **text_options):
        """
            creates canvas label object the first time;
            updates text contents if already created;
        """
        # already created?
        if self.id_text:
            # update text contents
            self.configure_text(text, **text_options)
        # first time creation
        else:
            # inits
            xb0, yb0, xb1, yb1 = self.LABEL_BOX
            # create text item
            self.id_text = self.canvas.create_text(
                left_x - xb0 + 1, top_y - yb0,
                anchor="nw",
            )
            self.configure_text(text, **text_options)
            # create surrounding box frame item
            _box = self.get_surrounding_box()
            self.id_box = self.canvas.create_rectangle(
                _box, **self.box_options
            )
            # put text over box frame
            self.canvas.tag_raise(self.id_text, self.id_box)
        # end if
    # end def


    def get_surrounding_box (self):
        """
            returns coordinates of text item's immediate surrounding
            box;
        """
        # allowed to proceed?
        if self.id_text:
            # return surrounding box
            return self.box_add(
                self.canvas.bbox(self.id_text), self.LABEL_BOX
            )
        # end if
    # end def


    def label_size_changed (self, widths, heights):
        """
            notifies owner about inner size changes;
        """
        print("label size changed: widths:", widths, "heights:", heights)
        # got callback?
        if callable(self.on_width_changed):
            # notify owner
            self.on_width_changed(widths)
        # end if
        # got callback?
        if callable(self.on_height_changed):
            # notify owner
            self.on_height_changed(heights)
        # end if
    # end def


    def reset (self, *args, **kw):
        """
            event handler: resets all canvas items to new;
        """
        # delete from canvas
        self.canvas.delete(self.id_box)
        self.canvas.delete(self.id_text)
        # reset IDs
        self.id_box = 0
        self.id_text = 0
    # end def


    @property
    def text_options (self):
        """
            internal property def;
        """
        # return private member
        return self.__text_options
    # end def

    @text_options.setter
    def text_options (self, options):
        # got overridings?
        if options:
            # override defaults
            self.__text_options.update(options)
            # strip forbidden options
            self.__text_options.pop("anchor", None)
        # end if
    # end def

    @text_options.deleter
    def text_options (self):
        # delete private member
        del self.__text_options
    # end def


    def update_box (self, *args, **kw):
        """
            event handler: updates box dims along text item new
            constraints;
        """
        # allowed to proceed?
        if self.id_box and self.id_text:
            # inits
            _box = self.canvas.coords(self.id_box)
            _w0, _h0 = self.box_size(_box)
            _w1, _h1 = self.box_size(self.get_surrounding_box())
            # width delta
            _dw = _w1 - _w0
            # height delta
            _dh = _h1 - _h0
            # size changed?
            if _dw or _dh:
                # reset width
                _box[2] = _box[0] + _w1
                # reset height
                _box[3] = _box[1] + _h1
                # update box size
                self.canvas.coords(self.id_box, *_box)
                # notify changes
                self.label_size_changed(
                    width=(_w0, _w1, _dw), height=(_h0, _h1, _dh)
                )
            # end if
        # end if
    # end def


    def update_label (self, *args, **kw):
        """
            event handler: updates all inner canvas items at once;
        """
        pass
    # end def


    def update_text (self, *args, **kw):
        """
            event handler: updates text alignment along box item new
            constraints;
        """
        # allowed to proceed?
        if self.id_box and self.id_text:
            # inits
            pass
        # end if
    # end def

# end class DBViewLabel
