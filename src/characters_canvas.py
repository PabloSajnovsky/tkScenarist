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
import tkinter.simpledialog as SD
import tkRAD.widgets.rad_canvas as RC


class CharactersCanvas (RC.RADCanvas):
    """
        Characters relations canvas class;
    """

    # class constant defs
    CONFIG = {
        "bg": "grey80",
        "highlightbackground": "grey20",
        "highlightthickness": 1,
    } # end of CONFIG

    CONFIG_LINK = {
        "font": "sans 8 italic",
        "anchor": "center",
        "color": "grey90",
        "background": "grey30",
        "outline": "grey10",
        "box": (-5, -5, +5, +5),
        "label_width": 150,
        "width": 0,
    }

    CONFIG_NAME = {
        "font": "sans 10 bold",
        "anchor": "center",
        "color": "royal blue",
        "background": "grey90",
        "outline": "grey10",
        "box": (-10, -10, +10, +10),
        "label_width": 200,
        "width": 1,
    }

    DRAG_MODE_LINK = 0x10
    DRAG_MODE_TEXT = 0x20

    ITEM_BOX = (-10, -10, +10, +10)

    TAG_RADIX_NAME = "name"
    TAG_RADIX_LINK = "link"


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
        self.bind("<Control-ButtonRelease-1>", self.slot_remove_item)
        self.bind("<Double-Button-1>", self.slot_double_clicked)
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


    def character_name_add (self, name, **kw):
        """
            adds a new character name into canvas widget;
        """
        # param inits
        xy = kw.get("xy") or self.viewport_center_xy()
        # set name and create item on canvas
        self.character_names[name] = self.create_label(
            self.TAG_RADIX_NAME, xy, text=name, **self.CONFIG_NAME
        )
        # update canvas contents
        self.update_canvas()
    # end def


    def character_name_remove (self, name):
        """
            deletes a character name from canvas widget;
        """
        # inits
        _group = self.character_names.get(name)
        # got item?
        if _group:
            # inits
            _tag = _group.get("tag")
            # delete items by group tag
            self.delete(_tag)
            # delete links
            self.remove_links(_tag)
            # remove group
            self.canvas_groups.pop(_tag, None)
            # remove from list
            self.character_names.pop(name, None)
            # update canvas contents
            self.update_canvas()
        # end if
    # end def


    def character_name_rename (self, old_name, new_name):
        """
            renames character name into canvas widget;
        """
        # inits
        _group = self.character_names.get(old_name)
        # got item?
        if _group:
            # rename text
            self.update_label(_group, text=new_name)
            # set new name
            self.character_names[new_name] = _group
            # remove old name from list
            self.character_names.pop(old_name, None)
            # update canvas contents
            self.update_canvas()
        # end if
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
        _ibox = kw.get("box") or self.ITEM_BOX
        x, y = xy
        # text item
        _id1 = self.create_text(
            x, y,
            text=kw.get("text") or "label",
            anchor=kw.get("anchor"),
            font=kw.get("font"),
            fill=kw.get("color"),
            width=kw.get("label_width"),
            tags=_tag,
        )
        # surrounding frame
        _box = self.bbox_add(self.bbox(_id1), _ibox)
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
        return self.group_add(
            _tag, tag=_tag, text=_id1, frame=_id2, box=_ibox
        )
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
            _tag2 = self.get_group_tag(
                self.find_overlapping(x, y, x, y)
            )
            # got name items?
            if self.TAG_RADIX_NAME in _tag2:
                # not already linked?
                if not self.tags_linked(_tag1, _tag2):
                    # get center coords
                    _center1 = self.get_bbox_center(_tag1)
                    _center2 = self.get_bbox_center(_tag2)
                    # draw line
                    _line = self.create_line(
                        _center1 + _center2,
                        fill=self.CONFIG_LINK.get("outline"),
                        width=1,
                    )
                    # put line under items
                    self.tag_lower(_line, _tag1)
                    self.tag_lower(_line, _tag2)
                    # set relation text
                    _dict = self.create_label(
                        self.TAG_RADIX_LINK,
                        self.get_segment_center(_center1, _center2),
                        text=_("Relation"),
                        **self.CONFIG_LINK
                    )
                    # update dict
                    _dict.update(line=_line, tag0=_tag1, tag1=_tag2)
                    # register new link
                    self.register_link(_tag1, _tag2, _dict)
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


    def do_edit_link (self, tag):
        """
            effective procedure for editing a relation link label;
        """
        # param controls
        if self.TAG_RADIX_LINK in tag:
            # inits
            _group = self.canvas_groups[tag]
            _text_id = _group["text"]
            _name0 = self.get_name_from_tag(_group["tag0"])
            _name1 = self.get_name_from_tag(_group["tag1"])
            # get new text
            _new_text = SD.askstring(
                _("Characters relation"),
                _("Relation '{from_name}' <---> '{to_name}'")
                .format(from_name=_name0, to_name=_name1),
                initialvalue=self.itemcget(_text_id, "text"),
                parent=self,
            )
            # got something?
            if _new_text:
                # update label
                self.update_label(_group, text=_new_text)
                # update canvas
                self.update_canvas()
            # end if
        # end if
    # end def


    def do_remove_link (self, tag):
        """
            effective procedure for removing a relation link label;
        """
        # param controls
        if self.TAG_RADIX_LINK in tag:
            # inits
            _group = self.canvas_groups[tag]
            _name0 = self.get_name_from_tag(_group["tag0"])
            _name1 = self.get_name_from_tag(_group["tag1"])
            # ask for user confirmation
            _confirm = MB.askyesno(
                title=_("Attention"),
                message=_(
                    "Relation: '{from_name}' <---> '{to_name}'.\n"
                    "Do you really want to remove this relation link?"
                ).format(from_name=_name0, to_name=_name1),
                parent=self,
            )
            # user confirmed
            if _confirm:
                # remove link from lists
                _tags = self.relation_links.get(_group["tag0"]) or dict()
                _tags.pop(_group["tag1"], None)
                _tags = self.relation_links.get(_group["tag1"]) or dict()
                _tags.pop(_group["tag0"], None)
                # remove link from canvas
                self.remove_group_link(_group)
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
            _tag = self.get_group_tag(
                self.find_overlapping(x, y, x, y)
            )
            # got name items?
            if self.TAG_RADIX_NAME in _tag:
                # store mouse starting point
                self.drag_start_xy = (x, y)
                # store mouse last position
                self.drag_last_pos = (x, y)
                # store group tag
                self.drag_tag = _tag
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


    def get_name_from_tag (self, tag):
        """
            returns character name along with @tag value;
        """
        # browse items
        for _name, _group in self.character_names.items():
            # got tag?
            if _group and _group["tag"] == tag:
                # return name
                return _name
            # end if
        # end for
        # failed
        return ""
    # end def


    def get_new_tag (self, tag_radix=None):
        """
            returns a new canvas tag name indexed with
            self.instance_counter;
        """
        # inits
        tag_radix = tag_radix or "group"
        # update counter
        self.instance_counter += 1
        # return new tag name
        return "{}#{}".format(tag_radix, self.instance_counter)
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


    def group_add (self, name, **kw):
        """
            adds a new canvas group;
        """
        # param controls
        if name:
            # already exists?
            if name in self.canvas_groups:
                raise KeyError(
                    _("canvas group name '{gname}' already exists.")
                    .format(gname=name)
                )
            # new to list
            else:
                # add new group
                self.canvas_groups[name] = kw
                # return group
                return kw
            # end if
        # end if
        # failed
        return None
    # end def


    def init_members (self, **kw):
        """
            class members only inits;
        """
        # members only inits
        self.instance_counter = 0
        self.character_names = dict()
        self.relation_links = dict()
        self.canvas_groups = dict()
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


    def register_link (self, tag1, tag2, group):
        """
            registers a link between two tags;
        """
        # put tag2 into tag1's list
        _tags = self.relation_links.setdefault(tag1, dict())
        _tags[tag2] = group
        # put tag1 into tag2's list
        _tags = self.relation_links.setdefault(tag2, dict())
        _tags[tag1] = group
    # end def


    def remove_group_link (self, group):
        """
            removes only one relation link by its group structure;
        """
        # param controls
        if group:
            # delete line from canvas
            self.delete(group["line"])
            # delete label items by tag
            self.delete(group["tag"])
            # remove group from list
            self.canvas_groups.pop(group["tag"], None)
        # end if
    # end def


    def remove_links (self, tag):
        """
            removes all relation links referred to by @tag;
        """
        # inits
        _tags = self.relation_links.setdefault(tag, dict())
        # browse tag groups
        for _group in _tags.values():
            # remove link by its group
            self.remove_group_link(_group)
        # end for
        # browse all tags linked to tag
        for _tags in self.relation_links.values():
            # remove linked tag
            _tags.pop(tag, None)
        # end for
        # remove tag itself
        self.relation_links.pop(tag, None)
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


    def slot_double_clicked (self, event=None, *args, **kw):
        """
            event handler for mouse double-clicking;
        """
        # param controls
        if event:
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            # looking for items
            _tag = self.get_group_tag(
                self.find_overlapping(x, y, x, y)
            )
            # got relation link items?
            if self.TAG_RADIX_LINK in _tag:
                # edit relation label
                self.do_edit_link(_tag)
            # got character name label?
            elif self.TAG_RADIX_NAME in _tag:
                # rename character
                self.events.raise_event(
                    "Characters:List:Rename", xy=(x, y)
                )
            # nothing out there?
            elif not _tag:
                # add new character name
                self.events.raise_event(
                    "Characters:List:Add", xy=(x, y)
                )
            # end if
        # end if
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
                    # update all tag's link positions
                    self.update_links(self.drag_tag)
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


    def slot_drop (self, event=None, *args, **kw):
        """
            event handler for D'n'D dropping on mouse release;
        """
        # param controls
        if event and self.drag_mode:
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            # character name label drop down
            if self.drag_mode == self.DRAG_MODE_TEXT:
                # get name
                _name = self.get_name_from_tag(self.drag_tag)
                # notify selected name
                self.events.raise_event(
                    "Characters:Name:Selected", name=_name
                )
            # character relations link creation?
            elif self.drag_mode == self.DRAG_MODE_LINK:
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


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        pass
    # end def


    def slot_remove_item (self, event=None, *args, **kw):
        """
            event handler for Ctrl+Click;
        """
        # param controls
        if event:
            # inits
            x, y = self.get_real_pos(event.x, event.y)
            # looking for items
            _tag = self.get_group_tag(
                self.find_overlapping(x, y, x, y)
            )
            # got relation link items?
            if self.TAG_RADIX_LINK in _tag:
                # remove relation link
                self.do_remove_link(_tag)
            # got character name label?
            elif self.TAG_RADIX_NAME in _tag:
                # get name
                _name = self.get_name_from_tag(_tag)
                # notify selected name
                self.events.raise_event(
                    "Characters:Name:Selected", name=_name
                )
                # remove character
                self.events.raise_event("Characters:List:Delete")
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
            # recalculate anchorage position
            self.drag_start_xy = self.get_bbox_center(self.drag_tag)
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
        _tags = self.relation_links.get(tag1) or dict()
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
            # project has been modified
            self.events.raise_event("Project:Modified")
        # no items
        else:
            # better clean up everything
            self.reset()
        # end if
    # end def


    def update_label (self, group, **kw):
        """
            updates label (text + frame) in @group;
        """
        # update text
        self.itemconfigure(group["text"], **kw)
        # update surrounding frame
        _box = self.bbox_add(self.bbox(group["text"]), group["box"])
        self.coords(group["frame"], _box)
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def update_links (self, tag):
        """
            updates positions for all links of @tag;
        """
        # inits
        _tags = self.relation_links.get(tag) or dict()
        _start_xy = self.get_bbox_center(tag)
        # browse items
        for _tag, _group in _tags.items():
            # inits
            _end_xy = self.get_bbox_center(_tag)
            # update line pos
            self.coords(_group["line"], _start_xy + _end_xy)
            # update label pos
            self.coords(
                _group["text"],
                self.get_segment_center(_start_xy, _end_xy)
            )
            self.update_label(_group)
        # end for
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

# end class CharactersCanvas
