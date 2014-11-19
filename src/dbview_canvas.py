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
from tkinter import ttk
import tkRAD.core.async as ASYNC
import tkRAD.widgets.rad_canvas as RC


class DBViewCanvas (RC.RADCanvas):
    """
        Database Query View canvas class;
    """

    # class constant defs
    CONFIG = {
        "bg": "white",
        "highlightbackground": "grey80",
        "highlightthickness": 1,
    } # end of CONFIG

    CONFIG_BODY = {
        "font": "monospace 10",
    }

    CONFIG_HEADER = {
        "font": "monospace 11",
    }


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        #~ self.events.connect_dict(
            #~ {
                #~ "Project:Modified": self.slot_project_modified,
            #~ }
        #~ )
        pass
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


    def ensure_visible_header (self, *args, **kw):
        """
            event handler: ensures header frame is always visible while
            scrolling canvas;
        """
        # reset pos
        self.coords(self.id_header, 0, self.canvasy(0))
        # set to foreground
        self.tag_raise(self.id_header, "all")
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.async = ASYNC.get_async_manager()
        self.field_sequence = None
        self.fields = dict()
        self.column_index = 0
        self.row_index = 0
        # widget inits
        self.frame_body = ttk.Frame(self)
        self.frame_header = ttk.Frame(self)
        self.id_body = self.create_window(
            0, 0, window=self.frame_body
        )
        self.id_header = self.create_window(
            0, 0, window=self.frame_header
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
        # test
        self.set_field_names("Name", "Male", "Female", "Origin", "Description")
    # end def


    def insert_label (self, frame, **kw):
        """
            inserts a ttk.Label widget into @frame along with grid
            internal (self.row_index, self.column_index) indices;
        """
        # inits
        _label = ttk.Label(
            frame,
            text=_(kw.get("text") or "label"),          # i18n support
            font=kw.get("font") or "monospace 10",
            background=kw.get("background") or "white",
            foreground=kw.get("foreground") or "black",
        )
        # insert into frame
        _label.grid(row=self.row_index, column=self.column_index)
        # next column
        self.column_index += 1
        # update canvas
        self.update_canvas()
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
            # set field options
            _opts = self.set_field_options(_name, **options)
            # set header label
            self.insert_label(self.frame_header, text=_name, **_opts)
        # end for
        # reset column index
        self.column_index = 0
    # end def


    def set_field_options (self, name, **options):
        """
            sets @options for a given field @name;
        """
        # inits
        _options = self.fields.get(name) or self.CONFIG_HEADER.copy()
        _options.update(options)
        # last but not least
        _options.update(name=name)
        # set field options
        self.fields[name] = _options
        # return new options
        return _options
    # end def


    def update_canvas (self, *args, **kw):
        """
            event handler for canvas contents updating;
        """
        print("dbview_canvas.update_canvas()")
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

# end class DBViewCanvas
