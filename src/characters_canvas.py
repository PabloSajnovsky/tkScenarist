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
import tkRAD.widgets.rad_canvas as RC


class CharactersCanvas (RC.RADCanvas):
    """
        Characters relations canvas class;
    """

    # class constant defs
    CONFIG = {
        "bg": "grey80",
        "highlightbackground": "grey20",
        "highlightthickness": "1",
    } # end of CONFIG

    DRAG_MODE_TEXT = 0x10
    DRAG_MODE_LINK = 0x20

    ITEM_BOX = (-10, -10, +10, +10)
    ITEM_COLOR1 = "royal blue"
    ITEM_COLOR2 = "grey90"
    ITEM_COLOR3 = "grey10"
    ITEM_FONT = "sans 10 bold"


    def add_name (self, name):
        """
            adds a new character name into canvas widget;
        """
        # inits
        _tag = self.get_new_tag()
        _x, _y = self.viewport_center_xy()
        # create item on canvas
        _id1 = self.create_text(
            _x, _y,
            text=name,
            font=self.ITEM_FONT,
            fill=self.ITEM_COLOR1,
            tags=_tag,
        )
        # surrounding frame
        _box = self.bbox_add(self.bbox(_id1), self.ITEM_BOX)
        _id2 = self.create_rectangle(
            _box,
            outline=self.ITEM_COLOR3,
            fill=self.ITEM_COLOR2,
            width=1,
            tags=_tag,
        )
        # set below text
        self.tag_lower(_id2, _id1)
        # set name
        self.items[name] = dict(tag=_tag, text=_id1, frame=_id2)
        # update canvas contents
        self.update_canvas()
    # end def


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
        self.bind("<Button-1>", self.slot_start_drag)
        self.bind("<Shift-Button-1>", self.slot_start_link)
        self.bind("<Motion>", self.slot_drag_pending)
        self.bind("<ButtonRelease-1>", self.slot_drop)
    # end def


    def center_x (self):
        """
            returns x coordinates for canvas' center point;
        """
        # return center point x coordinates
        return self.winfo_reqwidth() / 2
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
        return self.winfo_reqheight() / 2
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


    def delete_name (self, name):
        """
            deletes a character name from canvas widget;
        """
        # inits
        _dict = self.items.get(name)
        # got item?
        if _dict:
            # delete items by group tag
            self.delete(_dict.get("tag"))
            # remove from list
            self.items.pop(name, None)
            # update canvas contents
            self.update_canvas()
        # end if
    # end def


    def get_new_tag (self):
        """
            returns a new canvas tag name indexed with
            self.items_counter;
        """
        # update counter
        self.items_counter += 1
        # return new tag name
        return "item#{}".format(self.items_counter)
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.drag_mode = 0
        self.items_counter = 0
        self.items = dict()
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


    def rename_name (self, old_name, new_name):
        """
            renames character name into canvas widget;
        """
        # inits
        _dict = self.items.get(old_name)
        # got item?
        if _dict:
            # rename text
            _id1 = _dict["text"]
            _id2 = _dict["frame"]
            self.itemconfigure(_id1, text=new_name)
            # update surrounding frame
            _box = self.bbox_add(self.bbox(_id1), self.ITEM_BOX)
            self.coords(_id2, _box)
            # set new name
            self.items[new_name] = _dict
            # remove old name from list
            self.items.pop(old_name, None)
            # update canvas contents
            self.update_canvas()
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


    def slot_drag_pending (self, event=None, *args, **kw):
        """
            event handler for pending D'n'D on mouse motion;
        """
        # inits
        if self.drag_mode:
            print("Pending D'n'D", event.x, event.y)
            if self.drag_mode == self.DRAG_MODE_TEXT:
                print("Dragging character's name")
            elif self.drag_mode == self.DRAG_MODE_LINK:
                print("Creating relations link")
            # end if
        # end if
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        pass
    # end def


    def slot_drop (self, event=None, *args, **kw):
        """
            event handler for D'n'D dropping on mouse release;
        """
        # inits
        print("D'n'D: Dropped!", event.x, event.y)
        # reset drag mode
        self.drag_mode = 0
    # end def


    def slot_start_drag (self, event=None, *args, **kw):
        """
            event handler for name frame D'n'D;
        """
        # inits
        self.drag_mode = 0
        # got mouse event?
        if event:
            # init mouse position
            x, y = (event.x, event.y)
            # TODO: find tag @(x,y)                                         # FIXME
            print("Starting character's name D'n'D", (x, y))
            # set drag mode
            self.drag_mode = self.DRAG_MODE_TEXT
        # end if
    # end def


    def slot_start_link (self, event=None, *args, **kw):
        """
            event handler for relation linkings;
        """
        # inits
        self.drag_mode = 0
        # got mouse event?
        if event:
            # init mouse position
            x, y = (event.x, event.y)
            # TODO: find tag @(x,y)                                         # FIXME
            print("Starting creation of relations link", (x, y))
            # set drag mode
            self.drag_mode = self.DRAG_MODE_LINK
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
            x0, y0 = (min(0, x0), min(0, y0))
            x1, y1 = (max(x1, _cw), max(y1, _ch))
            # reset scroll region size
            self.configure(scrollregion=(x0, y0, x1, y1))
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
        return (self.canvasx(x), self.canvasy(y))
    # end def

# end class CharactersCanvas
