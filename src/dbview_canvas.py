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
            "text": {
                "align": "left",
                "font": "sans 10",
            },
            "box": {
            },
        },
        "header": {
            "text": {
                "align": "center",
                "font": "sans 11 bold",
            },
            "box": {
            },
        },
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


    def _do_update_all (self):
        """
            protected method def for internal use;
        """
        print("_do_update_all")
        # update all columns
        self._do_update_dimension(self.columns, (1, 0))
        # update all rows
        self._do_update_dimension(self.rows, (0, 1))
        # now, we can update scrolling area (deferred)
        self.update_canvas()
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


    def _do_update_dimension (self, collection, move_matrix):
        """
            updates size and position of all items in all managers of
            @collection;
            parameter @move_matrix determines move direction;
        """
        # inits
        _dmove = 0
        _previous = None
        _sx, _sy = move_matrix
        # browse collection
        for _manager in collection:
            # resize all items at once
            _manager.resize_all()
            # got to move?
            if _previous:
                # update move delta
                _dmove += _previous.get_move_delta()
                # move all by tag
                self.move(_manager.tag, _sx * _dmove, _sy * _dmove)
                # has moved
                _previous.reset_move()
            # end if
            # update item
            _previous = _manager
        # end for
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


    def get_column_manager (self, index):
        """
            returns the DBViewColumnManager object located at @index,
            if already exists; creates and then returns otherwise;
        """
        # get manager
        try:
            _manager = self.columns[index]
        except:
            _manager = None
        # end try
        # not found?
        if not _manager:
            # create a new one
            _manager = DBViewColumnManager()
            # register
            self.columns.insert(index, _manager)
        # end if
        # return current manager
        return _manager
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


    def get_insertion_xy (self, row, column, rman, cman):
        """
            returns (x, y) coordinates of top left insertion point;
        """
        # inits
        x, y = (0, 0)
        _coordx = self.coords(cman.tag)
        _coordy = self.coords(rman.tag)
        # can evaluate?
        if _coordx:
            # reset x
            x = _coordx[0]
        # end if
        # can evaluate?
        if _coordy:
            # reset y
            y = _coordy[1]
        # end if
        # return coords
        return (x, y)
    # end def


    def get_row_manager (self, index):
        """
            returns the DBViewRowManager object located at @index, if
            already exists; creates and then returns otherwise;
        """
        # get manager
        try:
            _manager = self.rows[index]
        except:
            _manager = None
        # end try
        # not found?
        if not _manager:
            # create a new one
            _manager = DBViewRowManager()
            # register
            self.rows.insert(index, _manager)
        # end if
        # return current manager
        return _manager
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
        self.rows = []
        self.columns = []
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


    def insert_label (self, group_tag, text, **kw):
        """
            inserts a text label into virtual grid;
        """
        # inits
        _row = kw.get("row") or self.row_index
        _column = kw.get("column") or self.column_index
        _fopts = kw.get("field_options") or dict()
        _text_opts = _fopts.get("text")
        _box_opts = _fopts.get("box")
        # get managers
        _rman = self.get_row_manager(_row)
        _cman = self.get_column_manager(_column)
        # other inits
        _tags = (group_tag, _rman.tag, _cman.tag)
        _text_opts.update(tags=_tags)
        _box_opts.update(tags=_tags)
        # create label
        _label = DBViewLabel(
            self,
            text_options=_text_opts,
            box_options=_box_opts,
            on_width_changed=_cman.on_dimension_changed,
            on_height_changed=_rman.on_dimension_changed,
        )
        # insert label
        x, y = self.get_insertion_xy(_row, _column, _rman, _cman)
        _label.create_label(x, y, text)
        # register label
        _rman.insert_item(_row, _label)
        _cman.insert_item(_column, _label)
        # next column
        if kw.get("column") is None:
            # update pos
            self.column_index += 1
        # end if
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
            print("field:", _name, "options:", _opts)
            # create label
            self.insert_label(
                "body", row=row_index, column=_column, text=_data,
                field_options=_opts,
            )
        # end for
        # update all (deferred)
        self.update_all()
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
            self._do_update_all,
            self._do_update_canvas,
        )
        # clear canvas
        self.clear_canvas(*args, **kw)
        # reset members
        self.init_members(**kw)
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


    def set_header (self, *names, header_options=None, body_options=None):
        """
            resets view and rebuilds along with new field @names and
            @options;
        """
        # reset all
        self.reset()
        # update field names ordered sequence
        self.field_sequence = names
        # default inits
        header_options = header_options or dict()
        body_options = body_options or dict()
        # browse names
        for _name in names:
            # init specific / generic options
            _hopts = header_options.get(_name) or header_options
            _bopts = body_options.get(_name) or body_options
            # set field options
            self.set_field_options("header", _name, **_hopts)
            _fopts = self.set_field_options("body", _name, **_bopts)
            # set header label
            self.insert_label(
                "header",
                text=_(_name),          # i18n support for header names
                field_options=_fopts["header"][_name]
            )
        # end for
        # new line
        self.next_row()
        # update all (deferred)
        self.update_all()
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


    def update_all (self, *args, **kw):
        """
            event handler: updates all rows and columns (deferred);
        """
        # deferred task
        self.async.run_after_idle(self._do_update_all)
    # end def


    def update_canvas (self, *args, **kw):
        """
            event handler: updates canvas scrollregion (deferred);
        """
        # deferred task
        self.async.run_after_idle(self._do_update_canvas)
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



class DBViewDimensionManager:
    """
        DBView Row/Column labels collection manager;
    """

    # class constant defs
    # redefine this in subclasses to fit your needs
    # e.g. "width", "height", ...
    DIMENSION_NAME = "dimension"


    def __init__ (self, tag=None):
        """
            class constructor;
        """
        # member inits
        self.tag = tag or "group#{}".format(id(self))
        self.dimension = 0
        self.move_delta = 0
        self.collection = list()
    # end def


    def add_item (self, item):
        """
            adds a new item to collection;
        """
        self.collection.append(item)
    # end def


    def get_move_delta (self):
        """
            returns current move delta;
        """
        return self.move_delta
    # end def


    def insert_item (self, index, item):
        """
            inserts a new item into collection, at given @index
            position;
        """
        self.collection.insert(index, item)
    # end def


    def on_dimension_changed (self, new_dimension):
        """
            updates global collection dimension;
        """
        # inits
        _dmove = new_dimension - self.dimension
        # got to enlarge?
        if _dmove > 0:
            # update to largest dimension
            self.dimension = new_dimension
            # add to future collection moves
            self.move_delta += _dmove
        # end if
    # end def


    def reset_move (self, *args, **kw):
        """
            event handler: resets move delta;
        """
        self.move_delta = 0
    # end def


    def resize_all (self, *args, **kw):
        """
            event handler: resizes all items in collection;
        """
        # browse items in collection
        for _item in self.collection:
            # force resizing
            _item.resize(**{self.DIMENSION_NAME: self.dimension})
        # end for
    # end def

# end class DBViewDimensionManager



class DBViewColumnManager (DBViewDimensionManager):
    """
        DBView Column labels collection manager;
    """

    # class constant defs
    # redefine this in subclasses to fit your needs
    # e.g. "width", "height", ...
    DIMENSION_NAME = "width"

# end class



class DBViewRowManager (DBViewDimensionManager):
    """
        DBView Row labels collection manager;
    """

    # class constant defs
    # redefine this in subclasses to fit your needs
    # e.g. "width", "height", ...
    DIMENSION_NAME = "height"

# end class DBViewRowManager



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
        self.id_box = 0
        self.id_text = 0
        # callbacks
        self.on_width_changed = kw.get("on_width_changed")
        self.on_height_changed = kw.get("on_height_changed")
        # options
        self.text_options = kw.get("text_options")
        self.box_options = kw.get("box_options")
    # end def


    def box_add (self, *boxes):
        """
            returns coordinates sum of many boxes;
        """
        return tuple(map(lambda x: sum(x), zip(*boxes)))
    # end def


    def box_center (self, x0, y0, x1, y1):
        """
            returns (x, y) coordinates of @box central point;
        """
        # return center coords
        return ((x0 + x1) // 2, (y0 + y1) // 2)
    # end def


    def box_coords (self, new_coords=None):
        """
            returns current coordinates of text surrounding box frame
            if @new_coords omitted;
            sets up new coords otherwise;
        """
        # allowed to proceed?
        if self.id_box:
            # need coords
            if not new_coords:
                # return coords
                return self.canvas.coords(self.id_box)
            # set new coords
            else:
                # setup
                self.canvas.coords(self.id_box, *new_coords)
            # end if
        # end if
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


    def box_resize (self, width=None, height=None, box=None):
        """
            forces surrounding box frame to fit new dims;
        """
        # inits
        _box = box or self.box_coords()
        # resize width?
        if width:
            # reset width
            _box[2] = _box[0] + width
        # end if
        # resize height?
        if height:
            # reset width
            _box[3] = _box[1] + height
        # end if
        # resize box
        self.box_coords(_box)
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
            # inits
            _tk_opts = self.text_options.copy()
            # strip unwanted
            _tk_opts.pop("align", None)
            # configure canvas item
            self.canvas.itemconfigure(
                self.id_text, text=text, **_tk_opts
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
            # create surrounding box frame item
            _box = self.get_surrounding_box()
            self.id_box = self.canvas.create_rectangle(
                _box, **self.box_options
            )
            # setup label text
            self.configure_text(text, **text_options)
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


    def label_size_changed (self, width, height):
        """
            notifies owners about inner size changes;
        """
        print("label size changed: width:", width, "height:", height)
        # got callback?
        if callable(self.on_width_changed):
            # notify owner
            self.on_width_changed(width)
        # end if
        # got callback?
        if callable(self.on_height_changed):
            # notify owner
            self.on_height_changed(height)
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


    def resize (self, width=None, height=None):
        """
            forces label's surrounding box frame to fit new dims;
        """
        # delegate
        self.box_resize(width, height)
        # should align text?
        if width:
            print("DBViewLabel.resize(): aligning text")
            # update text alignment
            self.update_text()
        # end if
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
            _box = self.box_coords()
            _w0, _h0 = self.box_size(_box)
            _w1, _h1 = self.box_size(self.get_surrounding_box())
            # width delta
            _dw = _w1 - _w0
            # height delta
            _dh = _h1 - _h0
            # size changed?
            if _dw or _dh:
                # update box size
                self.box_resize(box=_box, width=_w1, height=_h1)
                # notify changes
                self.label_size_changed(width=_w1, height=_h1)
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
            _align = self.text_options.get("align") or "left"
            print("align:", _align, "text options:", self.text_options)
            x0, y0, x1, y1 = kw.get("box") or self.box_coords()
            xb0, yb0, xb1, yb1 = self.LABEL_BOX
            # should center text?
            if _align == "center":
                # get central point coords
                x, y = self.box_center(x0, y0, x1, y1)
                _anchor = "center"
            # align right hand?
            elif _align == "right":
                # get bottom right point coords
                x, y = (x1 - xb1, y1 - yb1)
                _anchor = "se"
            # align left hand by default
            else:
                # get top left point coords
                x, y = (x0 - xb0 + 1, y0 - yb0)
                _anchor = "nw"
            # end if
            # update text position
            self.canvas.coords(self.id_text, x, y)
            # update anchorage
            self.canvas.itemconfigure(self.id_text, anchor=_anchor)
        # end if
    # end def

# end class DBViewLabel
