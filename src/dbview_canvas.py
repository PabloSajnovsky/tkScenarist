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

    CONFIG_FIELD = {

        "body": {
            "font": "sans 10",
        },

        "header": {
            "font": "sans 11 bold",
        },
    }


    def _do_set_field_options(self, section, name, **options):
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
        # test
        self.async.run_after_idle(self.test_session)
    # end def


    def insert_label (self, frame, **kw):
        """
            inserts a ttk.Label widget into @frame along with grid
            internal (self.row_index, self.column_index) indices;
        """
        # inits
        _label = ttk.Label(
            frame,
            anchor=kw.get("anchor"),
            background=kw.get("background") or "white",
            borderwidth=kw.get("borderwidth") or 1,
            class_=kw.get("class_"),
            compound=kw.get("compound"),
            cursor=kw.get("cursor"),
            font=kw.get("font") or "sans 10",
            foreground=kw.get("foreground") or "black",
            image=kw.get("image"),
            justify=kw.get("justify"),
            padding=kw.get("padding") or "2px",
            relief=kw.get("relief") or "solid",
            style=kw.get("style"),
            takefocus=kw.get("takefocus"),
            text=_(kw.get("text") or "label"),          # i18n support
            textvariable=kw.get("textvariable"),
            underline=kw.get("underline"),
            width=kw.get("width"),
            wraplength=kw.get("wraplength"),
        )
        # insert into frame
        _label.grid(
            row=kw.get("row") or self.row_index,
            column=kw.get("column") or self.column_index,
            sticky=kw.get("sticky") or "nwse",
        )
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
            _opts = self.set_field_options("all", _name, **options)
            # set header label
            self.insert_label(
                self.frame_header, text=_name, **_opts["header"][_name]
            )
        # end for
        # reset column index
        self.column_index = 0
        # reset body frame position on canvas
        self.coords(
            self.id_body, 0, self.frame_header.winfo_reqheight()
        )
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


    def test_session (self, *args, **kw):
        """
            event handler for testing session;
        """
        self.set_field_names(
            "Name", "Male", "Female", "Origin", "Description"
        )
        for i in range(10):
            self.insert_row(
                dict(
                    Name="toto",
                    Male="M",
                    Origin="unknown",
                    Description="bla bla bla qmlskdj "
                        "mlq kjsdfm sf qls dmlf jqsdmlf jqmls "
                        "dfjml sjdlfm jqmlsdj fmlqjsdk fml sf",
                )
            )
        # end for
    # end def


    def update_canvas (self, *args, **kw):
        """
            event handler for canvas contents updating;
        """
        # defer task
        self.async.run_after_idle(self._do_update_canvas)
    # end def

# end class DBViewCanvas
