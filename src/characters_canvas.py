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
import tkinter.messagebox as MB
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
    ITEM_COLOR4 = "grey30"
    ITEM_FONT1 = "sans 10 bold"
    ITEM_FONT2 = "sans 8 italic"


    def add_name (self, name):
        """
            adds a new character name into canvas widget;
        """
        # set name and create item on canvas
        self.items[name] = self.create_label(
            "name",
            self.viewport_center_xy(),
            text=name,
            font=self.ITEM_FONT1,
            color=self.ITEM_COLOR1,
            background=self.ITEM_COLOR2,
            outline=self.ITEM_COLOR3,
            width=1,
        )
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
        self.bind("<Configure>", self.update_canvas)
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


    def create_label (self, tag_radix, xy, **kw):
        """
            creates a text label with surrounding frame on canvas;
        """
        # inits
        _tag = self.get_new_tag(tag_radix)
        x, y = xy
        # text item
        _id1 = self.create_text(
            x, y,
            text=kw.get("text") or "label",
            anchor=kw.get("anchor"),
            font=kw.get("font"),
            fill=kw.get("color"),
            tags=_tag,
        )
        # surrounding frame
        _box = self.bbox_add(self.bbox(_id1), self.ITEM_BOX)
        _id2 = self.create_rectangle(
            _box,
            outline=kw.get("outline"),
            fill=kw.get("background"),
            width=kw.get("width"),
            tags=_tag,
        )
        # set frame below text
        self.tag_lower(_id2, _id1)
        # return dict of items
        return dict(tag=_tag, text=_id1, frame=_id2)
    # end def


    def delete_name (self, name):
        """
            deletes a character name from canvas widget;
        """
        # inits
        _group = self.items.get(name)
        # got item?
        if _group:
            # delete items by group tag
            self.delete(_group.get("tag"))
            # remove from list
            self.items.pop(name, None)
            # update canvas contents
            self.update_canvas()
        # end if
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


    def do_create_link (self, x, y):
        """
            effective procedure for creating chars relations link;
        """
        # got data?
        if self.drag_mode:
            # inits
            _tag1 = self.drag_tag
            _ids = self.find_overlapping(x, y, x, y)
            # got ids?
            if _ids:
                # inits
                _tag2 = self.get_group_tag(_ids)
                # not already linked?
                if not self.tags_linked(_tag1, _tag2):
                    # get center coords
                    _center1 = self.get_bbox_center(_tag1)
                    _center2 = self.get_bbox_center(_tag2)
                    # draw line
                    _line = self.create_line(
                        _center1 + _center2,
                        fill=self.ITEM_COLOR3,
                        width=1,
                    )
                    # put line under items
                    self.tag_lower(_line, _tag1)
                    self.tag_lower(_line, _tag2)
                    # set relation text
                    _dict = self.create_label(
                        "link",
                        self.get_segment_center(_center1, _center2),
                        text=_("Relation"),
                        color=self.ITEM_COLOR2,
                        background=self.ITEM_COLOR4,
                        width=0,
                    )
                    # register new link
                    #~ self.register_link(_tag1, _tag2, _line, _dict)
                # already linked
                else:
                    # warn user
                    MB.showwarning(
                        title=_("Attention"),
                        message=_(
                            "These two character names "
                            "are *ALREADY LINKED* together."
                        ),
                        parent=self,
                    )
                # end if
            # end if
        # end if
    # end def


    def do_start_drag (self, event, drag_mode):
        """
            effective procedure for starting Drag'n'Drop feature;
        """
        # inits
        self.dnd_reset()
        # got mouse event?
        if event:
            # automatic scrolling feature
            self.scan_mark(event.x, event.y)
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            # looking for items
            _ids = self.find_overlapping(x, y, x, y)
            # got items?
            if _ids:
                # store mouse starting point
                self.drag_start_xy = (x, y)
                # store mouse last position
                self.drag_last_pos = (x, y)
                # store group tag
                self.drag_tag = self.get_group_tag(_ids)
                # raise group above all others
                self.tag_raise(self.drag_tag, "all")
                # set drag mode
                self.drag_mode = drag_mode
            # auto-scrolling mode
            else:
                self.auto_scroll = True
            # end if
        # end if
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


    def get_new_tag (self, tag_radix=None):
        """
            returns a new canvas tag name indexed with
            self.items_counter;
        """
        # inits
        tag_radix = tag_radix or "group"
        # update counter
        self.items_counter += 1
        # return new tag name
        return "{}#{}".format(tag_radix, self.items_counter)
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


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.items_counter = 0
        self.items = dict()
        self.links = dict()
        # Drag'n'Drop feature
        self.dnd_reset()
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


    def register_link (self, tag1, tag2):
        """
            registers a link between two tags;
        """
        # put tag2 into tag1's list
        _tags = self.links.setdefault(tag1, set())
        _tags.add(tag2)
        # put tag1 into tag2's list
        _tags = self.links.setdefault(tag2, set())
        _tags.add(tag1)
    # end def


    def rename_name (self, old_name, new_name):
        """
            renames character name into canvas widget;
        """
        # inits
        _group = self.items.get(old_name)
        # got item?
        if _group:
            # rename text
            _id1 = _group["text"]
            _id2 = _group["frame"]
            self.itemconfigure(_id1, text=new_name)
            # update surrounding frame
            _box = self.bbox_add(self.bbox(_id1), self.ITEM_BOX)
            self.coords(_id2, _box)
            # set new name
            self.items[new_name] = _group
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
                # dragging text items
                if self.drag_mode == self.DRAG_MODE_TEXT:
                    # move items along their group tag
                    self.move(self.drag_tag, dx, dy)
                # dragging relations link
                elif self.drag_mode == self.DRAG_MODE_LINK:
                    # update link's line representation
                    self.coords(
                        self.drag_link_id, self.drag_start_xy + (x, y)
                    )
                # end if
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
        # param controls
        if self.drag_mode and event:
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            # character relations link creation?
            if self.drag_mode == self.DRAG_MODE_LINK:
                # delete virtual link
                self.delete(self.drag_link_id)
                # create real link with items and registering
                self.do_create_link(x, y)
            # end if
        # end if
        # reset D'n'D mode
        self.dnd_reset()
        # update canvas
        self.update_canvas()
    # end def


    def slot_start_drag (self, event=None, *args, **kw):
        """
            event handler for name frame D'n'D;
        """
        # start D'n'D for text items
        self.do_start_drag(event, self.DRAG_MODE_TEXT)
    # end def


    def slot_start_link (self, event=None, *args, **kw):
        """
            event handler for relation linkings;
        """
        # start D'n'D for relations link creation
        self.do_start_drag(event, self.DRAG_MODE_LINK)
        # started dragging?
        if self.drag_mode:
            # create link
            self.drag_link_id = self.create_line(self.drag_start_xy * 2)
            # set it under text items
            self.tag_lower(self.drag_link_id, self.drag_tag)
        # end if
    # end def


    def tags_linked (self, tag1, tag2):
        """
            determines if tags are linked together;
            returns True if linked, False otherwise;
        """
        # inits
        _tags = self.links.setdefault(tag1, set())
        # get boolean
        return bool(tag2 in _tags)
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
