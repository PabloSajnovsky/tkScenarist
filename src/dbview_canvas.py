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

    CONFIG_DATA = {
        "font": "monospace 10",
        "max_width": None,
    }

    CONFIG_HEADERS = {
        "font": "monospace 11",
        "max_width": None,
    }

    LABEL_BOX = (-5, -5, +5, +5)

    TAG_DATA = "data"
    TAG_HEADERS = "headers"


    def bbox_add (self, bbox1, bbox2):
        """
            returns coordinates sum of bounding boxes;
        """
        return tuple(map(lambda x: sum(x), zip(bbox1, bbox2)))
    # end def


    def bbox_size (self, tag_or_bbox):
        """
            returns (width, height) bbox size along tag or bbox;
        """
        # tag type?
        if not isinstance(tag_or_bbox, (tuple, list)):
            # search bbox
            tag_or_bbox = self.bbox(tag_or_bbox) or (0, 0, 0, 0)
        # end if
        # inits
        x0, y0, x1, y1 = tag_or_bbox
        # return bbox size (width, height)
        return (abs(x1 - x0), abs(y1 - y0))
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,
            }
        )
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


    def create_label (self, left_x, top_y, **kw):
        """
            creates a text label on canvas along with @kw keyword
            options;
        """
        # inits
        x0, y0, x1, y1 = self.LABEL_BOX
        x, y = (left_x - x0, top_y - y0)
        # create text
        _id1 = self.create_text(
            x, y,
            anchor="nw",
            text=_(kw.get("text") or "label"),
            font=kw.get("font") or "monospace 10",
            fill=kw.get("foreground") or "black",
            width=kw.get("max_width"),
            tags=kw.get("tags"),
        )
        # recalc bbox for surrounding frame box
        _bbox = self.bbox_add(self.bbox(_id1), self.LABEL_BOX)
        # init surrounding frame
        _id2 = self.create_rectangle(
            _bbox,
            fill=kw.get("background") or "white",
            outline=kw.get("outline") or "black",
            width=kw.get("outline_width") or 1,
            tags=kw.get("tags"),
        )
        # set frame under text
        self.tag_lower(_id2, _id1)
        # update canvas by now
        self.update_canvas()
    # end def


    def header_add (self, name, **options):
        """
            adds a field header label on canvas;
        """
        # retrieve previous header labels
        _tag = self.TAG_HEADERS
        _bbox = self.bbox(_tag)
        x, y = (0, 0)
        # got previous?
        if _bbox:
            # inits
            x0, y0, x1, y1 = _bbox
            x, y = (x1, y0)
        # end if
        # create label
        self.create_label(x, y, text=name, tags=_tag, **options)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.async = ASYNC.get_async_manager()
        self.field_sequence = None
        self.fields = dict()
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


    def reset (self, *args, **kw):
        """
            event handler: resets all in widget;
        """
        # reset members
        self.init_members(**kw)
        # clear canvas
        self.clear_canvas(*args, **kw)
    # end def


    def set_field_options (self, name, **options):
        """
            sets field's new @options along with its field @name;
        """
        # inits
        _options = self.fields.get(name) or self.CONFIG_HEADERS.copy()
        _options.update(options)
        # last but not least
        _options.update(name=name)
        # set new options
        self.fields[name] = _options
        # return new options
        return _options
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
            # add field label on canvas
            self.header_add(_name, **_opts)
        # end for
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        pass
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