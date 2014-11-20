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


    def _do_resync_body_header (self, column, width):
        """
            protected method def for internal use;
        """
        # inits
        _name = self.field_sequence[column]
        _width = max(
            width,
            self.get_field_options("header", _name).get("width") or 0
        )
        # update column widths
        self.frame_body.columnconfigure(column, minsize=_width)
        self.frame_header.columnconfigure(column, minsize=_width)
        # update header option
        self.set_field_options("header", _name, width=_width)
        # update canvas
        self.update_canvas()
    # end def


    def _do_set_field_options (self, section, name, **options):
        """
            protected method def for internal use;
        """
        # param controls
        if section in self.field_options:
            # inits
            _options = self.field_options[section].get(name) or \
                                    self.CONFIG_FIELD[section].copy()
            # override new options
            _options.update(options)
            # last but not least
            _options.update(name=name)
            # update field options
            self.field_options[section][name] = _options
        # end if
    # end def


    def _do_test (self):
        #~ print("do test")
        self.set_field_names(
            "Name", "Gender", "Origin", "Description",
            Gender=dict(align="center"),
        )
        for i in range(10):
            self.insert_row(
                dict(
                    Name="Aaron",
                    Gender="M",
                    Origin="Hebrew",
                    Description="bla",
                )
            )
            self.insert_row(
                dict(
                    Name="Beatrix",
                    Gender="F",
                    Origin="Latin",
                    Description="bla bla",
                )
            )
            self.insert_row(
                dict(
                    Name="Camille",
                    Gender="MF",
                    Origin="French",
                    Description="bla bla bla",
                )
            )
            self.insert_row(
                dict(
                    Name="Dooloo",
                    Gender="-",
                    Origin="Alien",
                    Description="bla bla bla bla",
                )
            )
        # end for
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
        self.events.connect_dict(
            {
                "DBView:Test": self.slot_test_session,
            }
        )
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
            self.coords(self.id_header, 0, self.canvasy(0))
            # set to foreground
            self.tag_raise(self.id_header, "all")
        except:
            pass
        # end try
    # end def


    def get_field_options (self, section, name):
        """
            retrieves field options for @section and field @name;
        """
        # section exists?
        if section in self.field_options:
            # return options by field name
            return self.field_options[section].get(name)
        # unsupported
        else:
            # no options
            return dict()
        # end if
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
        # widget inits
        self.frame_body = ttk.Frame(self)
        self.frame_header = ttk.Frame(self)
        self.id_body = self.create_window(
            0, 0, anchor="nw", window=self.frame_body
        )
        self.id_header = self.create_window(
            0, 0, anchor="nw", window=self.frame_header
        )
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


    def insert_label (self, frame, **kw):
        """
            inserts a ttk.Label widget into @frame along with grid
            internal (self.row_index, self.column_index) indices;
        """
        # inits
        _align = kw.get("align")
        # param override?
        if _align:
            # override anchor
            _anchor = kw.get(
                "anchor", self.FIELD_ALIGN.get(_align, "center")
            )
        # end if
        # inits
        _label = ttk.Label(
            frame,
            anchor=_anchor,
            background=kw.get("background") or "white",
            borderwidth=kw.get("borderwidth", 1),
            class_=kw.get("class_"),
            compound=kw.get("compound"),
            cursor=kw.get("cursor"),
            font=kw.get("font"),
            foreground=kw.get("foreground") or "black",
            image=kw.get("image"),
            justify=kw.get("justify"),
            padding=kw.get("padding") or "2px",
            relief=kw.get("relief") or "solid",
            style=kw.get("style"),
            takefocus=kw.get("takefocus"),
            text=_(kw.get("text", "label")),            # i18n support
            textvariable=kw.get("textvariable"),
            underline=kw.get("underline"),
            width=kw.get("width"),
            wraplength=kw.get("wraplength", 500),
        )
        # insert into frame
        _column = kw.get("column", self.column_index)
        _label.grid(
            row=kw.get("row", self.row_index),
            column=_column,
            sticky="nwse",
        )
        # resync body/header column widths
        self.resync_body_header(_column, _label.winfo_reqwidth())
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
                self.frame_body,
                row=row_index,
                column=_column,
                text=_data,
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
        # clear canvas
        self.clear_canvas(*args, **kw)
        # reset members
        self.init_members(**kw)
    # end def


    def resync_body_header (self, column, width):
        """
            resyncs body/header column width;
        """
        # deferred task
        # CAUTION:
        # this must *NOT* be cancelled, rescheduled or any other /!\
        self.after_idle(
            self._do_resync_body_header, column, width
        )
    # end def


    def resync_body_position (self):
        """
            resyncs body position along with header's line height;
        """
        # resync body position
        self.coords(
            self.id_body, 0, self.frame_header.winfo_reqheight()
        )
    # end def


    def set_field_names (self, *names, **options):
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
                self.frame_header, text=_name, **_opts["header"][_name]
            )
        # end for
        # reset column index
        self.column_index = 0
        # reset body frame position on canvas
        self.async.run_after_idle(self.resync_body_position)
    # end def


    def set_field_options (self, section, name, **options):
        """
            sets @options for a given field @name;
        """
        # param controls
        if name in self.field_sequence:
            # inits
            section = str(section).lower()
            # body options
            if section in ("body", "both", "all"):
                # set options for body field name
                self._do_set_field_options("body", name, **options)
            # end if
            # header options
            if section in ("header", "both", "all"):
                # set options for header field name
                self._do_set_field_options("header", name, **options)
            # end if
            # return all options
            return self.field_options
        # end if
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


    def slot_test_session (self, *args, **kw):
        """
            event handler for testing session;
        """
        # deferred task
        self.async.run_after(500, self._do_test)
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
