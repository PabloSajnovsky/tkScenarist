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
import tkRAD.core.asyn as ASYNC
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
        "current_width": None,
    }

    CONFIG_HEADERS = {
        "font": "monospace 11",
        "max_width": None,
        "current_width": None,
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
        # tkinter event bindings
        #~ self.bind("<Configure>", self.update_canvas)
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
            text=kw.get("text") or "label",
            font=kw.get("font"),
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


    def header_add (self, name, **options):
        """
            adds a field header label on canvas;
        """
        # retrieve previous header labels
        _bbox = self.bbox(self.TAG_HEADERS)
        left_x, top_y = (0, 0)
        # got previous?
        if _bbox:
            # inits
            x0, y0, x1, y1 = _bbox
            left_x, top_y = (x1, y0)
        # end if
        # create label
        self.create_label(left_x, top_y, text=name, **options)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.async = ASYNC.get_async_manager()
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
            sets field's new @options along with its @name;
        """
        # inits
        _options = self.fields.get(name) or self.CONFIG_HEADERS.copy()
        _options.update(options)
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
        # browse names
        for _index, _name in enumerate(names):
            # inits
            options.update(name=_name, index=_index)
            # set field options
            _opts = self.set_field_options(_name, **options)
            # add field label on canvas
            self.header_add(_name, **_opts)
        # end for
    # end def


    def size_xy (self):
        """
            returns (width, height) coordinates;
        """
        # get coordinates
        return (self.winfo_reqwidth(), self.winfo_reqheight())
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


    def viewport_center_xy (self):
        """
            returns (x, y) coordinates of viewport's center point;
        """
        # inits
        x, y = self.center_xy()
        # viewport's center point
        return (int(self.canvasx(x)), int(self.canvasy(y)))
    # end def

# end class DBViewCanvas
