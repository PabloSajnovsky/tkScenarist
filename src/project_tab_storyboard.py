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
import re
import json
import tkinter.messagebox as MB
import tkinter as TK
import tkRAD
import tkRAD.core.async as ASYNC
from tkRAD.core import tools


class ProjectTabStoryboard (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    def auto_save (self, *args, **kw):
        """
            event handler;
            automatically saves data, if any;
        """
        # inits
        _lb = self.LBOX_SHOT
        _index = _lb.last_selected
        # got selected?
        if _index >= 0:
            # inits
            _shot = self.LBL_SHOT.get()
            _title = self.ENT_SHOT.get()
            _item = self.get_formatted_shot_text(_shot, _title)
            _text = self.text_get_contents(self.TEXT_SHOT).strip()
            _scene_nr, _shot_nr = _shot.strip("#").split(".")
            # update listbox item
            self.update_listbox_item(_lb, _index, _item)
            # update record in database
            self.database.stb_update_shot(
                scene=int(_scene_nr),
                shot=int(_shot_nr),
                title=_title,
                text=_text,
            )
        # end if
    # end def


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Characters:List:Changed":
                    self.slot_update_characters_listbox,

                "Project:Modified": self.slot_project_modified,

                "Scenario:Scene:Browser:Changed":
                    self.slot_update_scene_listbox,

                "Storyboard:Shot:Add": self.slot_shot_add,
                "Storyboard:Shot:Delete": self.slot_shot_delete,
                "Storyboard:Shot:Purge": self.slot_shot_purge,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        self.bind("<Expose>", self.slot_on_tab_exposed)
        self.LBOX_SCENE.bind(
            "<<ListboxSelect>>", self.slot_scene_item_selected
        )
        self.LBOX_SHOT.bind(
            "<<ListboxSelect>>", self.slot_shot_item_selected
        )
        self.LBOX_CHARS.bind(
            "<<ListboxSelect>>", self.slot_characters_item_selected
        )
        self.TEXT_SHOT.bind("<KeyRelease>", self.slot_on_text_keypress)
        self.TEXT_SHOT.bind("<ButtonRelease>", self.slot_on_text_clicked)
        self.TEXT_SHOT.bind("<FocusOut>", self.slot_on_focus_out)
        # multiple event inits
        _events = {
            "<Key>": self.slot_popup_keypress,
            "<KeyRelease>": self.slot_popup_keyrelease,
            "<Button-1>": self.slot_popup_clicked,
            "<Double-Button-1>": self.slot_popup_double_clicked,
            "<<ListboxSelect>>": self.slot_popup_item_selected,
        }
        for _seq, _slot in _events.items():
            self.POPUP_LBOX.bind(_seq, _slot)
        # end for
    # end def


    def clear_entry (self, *widgets):
        """
            clears contents for entry widget(s);
        """
        # browse widgets
        for _w in widgets:
            # enable widget
            self.enable_widget(_w, True)
            # clear widget
            _w.delete(0, "end")
            # disable widget
            self.enable_widget(_w, False)
        # end for
    # end def


    def clear_listbox (self, *widgets):
        """
            clears contents for listbox widget(s);
        """
        # browse widgets
        for _w in widgets:
            # clear widget
            _w.delete(0, "end")
            # clear selection
            _w.selection_clear(0, "end")
            # reset last selected
            _w.last_selected = -1
        # end for
    # end def


    def clear_text (self, *widgets):
        """
            clears contents for text widget(s);
        """
        # browse widgets
        for _w in widgets:
            # enable widget
            self.enable_widget(_w, True)
            # clear widget
            self.text_clear_contents(_w)
            # disable widget
            self.enable_widget(_w, False)
        # end for
    # end def


    def enable_widget (self, widget, state):
        """
            enables/disables a tkinter widget along with @state value;
        """
        # reset state
        widget.configure(
            state={True: "normal"}.get(bool(state), "disabled")
        )
    # end def


    def get_column_index (self, index=None):
        """
            retrieves column index as integer for @index location;
        """
        # inits
        index = self.TEXT_SHOT.index(index or TK.INSERT)
        # return integer
        return tools.ensure_int(index.split(".")[-1])
    # end def


    def get_current_selected (self, listbox, force_index=-1):
        """
            returns dict (index, text) of current selection or None,
            otherwise;
        """
        # param controls
        if 0 <= force_index < listbox.size():
            # force pointer value
            listbox.last_selected = force_index
        else:
            # inits
            _sel = listbox.curselection()
            # got selected?
            if _sel:
                # update pointer value
                listbox.last_selected = _sel[0]
            # empty listbox?
            elif not listbox.size():
                # force clear-ups
                self.clear_listbox(listbox)
            # end if
        # end if
        # return result
        return listbox.last_selected
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # save last shot right now!
        self.save_now()
        # inits
        _rows = [dict(i) for i in self.database.stb_get_all_shots()]
        fcontents = json.dumps(_rows)
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_formatted_shot_text (self, shot_number, title=""):
        """
            returns formatted string for shot listbox insertion;
        """
        # return formatted string
        return "{} {}".format(shot_number, title)
    # end def


    def get_line_contents (self, index=None):
        """
            retrieves line text contents at @index or insertion cursor,
            if omitted;
        """
        # inits
        index = index or TK.INSERT
        # return contents
        return self.TEXT_SHOT.get(
            "{} linestart".format(index), "{} lineend".format(index)
        )
    # end def


    def get_scene_shot (self, index):
        """
            retrieves (scene, shot) numbers from shot listbox item
            located at @index;
        """
        # inits
        _shot, _title = self.get_shot_chunks(self.LBOX_SHOT.get(index))
        _scene, _shot = _shot.strip("#").split(".")
        return (_scene, _shot)
    # end def


    def get_shot_chunks (self, text):
        """
            tries to retrieve shot number + title from given @text;
            returns tuple of strings (number, title) when found, and
            None otherwise;
        """
        # param controls
        if text:
            # inits
            _found = re.match(r"(#\d+\.\d+) (.*)", text)
            # found?
            if _found:
                # return results
                return _found.groups()
            # end if
        # end if
        # failed
        return None
    # end def


    def get_shot_listbox_contents (self, scene):
        """
            retrieves shot listbox contents alongs with given @scene;
            returns empty tuple on failure;
        """
        # inits
        _contents = []
        # browse rows
        for _row in self.database.stb_get_shot_list(scene):
            # new shot item
            _contents.append(
                self.get_formatted_shot_text(
                    self.get_shot_number(scene, _row["shot"]),
                    _row["title"]
                )
            )
        # end for
        # return shot list
        return tuple(_contents)
    # end def


    def get_shot_number (self, scene, shot):
        """
            returns shot number as formatted string;
        """
        # return shot number
        return "#{}.{:02d}".format(scene, shot)
    # end def


    def get_word (self, index=None):
        """
            retrieves word located at or around @index, if any.
        """
        # inits
        index = index or TK.INSERT
        _start = "{} linestart".format(index)
        _end = "{} lineend".format(index)
        _word = ""
        # look backward
        _text = self.TEXT_SHOT.get(_start, index)
        _pos = _text.rfind(" ")
        # found?
        if _pos >= 0:
            # set first part of word
            _word += _text[_pos + 1:]
            # update start index
            _start = "{}+{}c".format(_start, _pos + 1)
        else:
            # take all
            _word += _text
        # end if
        # look forward
        _text = self.TEXT_SHOT.get(index, _end)
        _pos = _text.find(" ")
        # found?
        if _pos >= 0:
            # set last part of word
            _word += _text[:_pos]
            # update end index
            _end = "{}+{}c".format(_start, _pos)
        else:
            # take all
            _word += _text
        # end if
        # return result
        return {
            "word": _word.rstrip(" .:,;?!\"']})"),
            "start_index": _start,
            "end_index": _end,
        }
    # end def


    def hide_popup_list (self, *args, **kw):
        """
            event handler: hides autocompletion popup list;
        """
        # stop pending popup openings
        self.async.stop(self.slot_autocomplete)
        # hide popup list
        self.POPUP.withdraw()
        self.POPUP.start_index = None
        self.POPUP_LBOX.current_index = 0
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.mainwindow = self.winfo_toplevel()
        self.mainframe = self.mainwindow.mainframe
        self.database = self.mainwindow.database
        self.tab_characters = self.mainframe.tab_characters
        self.text_clear_contents = self.mainwindow.text_clear_contents
        self.text_get_contents = self.mainwindow.text_get_contents
        self.text_set_contents = self.mainwindow.text_set_contents
        self.async = ASYNC.get_async_manager()
        # looks for ^/xml/widget/tab_storyboard.xml
        self.xml_build("tab_storyboard")
        # widget inits
        self.LBOX_SCENE = self.listbox_scene_browser
        self.LBOX_SCENE.text_lines = []
        self.LBOX_SHOT = self.listbox_shot_browser
        self.LBOX_CHARS = self.listbox_character_names
        self.BTN_ADD = self.btn_add_shot
        self.BTN_DEL = self.btn_del_shot
        self.BTN_PURGE = self.btn_purge_shot
        self.TEXT_SCENE = self.text_scene_preview
        self.TEXT_SHOT = self.text_shot_editor
        self.TEXT_CHARLOG = self.text_characters_log
        self.ENT_SHOT = self.entry_shot_title
        self.LBL_SCENE = self.get_stringvar("lbl_scene_number")
        self.LBL_SHOT = self.get_stringvar("lbl_shot_number")
        self.LBL_CHARNAME = self.get_stringvar("lbl_character_name")
        # popup list
        self.POPUP = self.toplevel_popup_list
        self.POPUP.transient(self.TEXT_SHOT)
        self.POPUP.overrideredirect(True)
        self.POPUP_LBOX = self.listbox_popup_list
        # (re)route events (POPUP_LBOX has priority on TEXT_SHOT)
        self.mainframe.tab_scenario.route_events(
            self.POPUP_LBOX, self.TEXT_SHOT
        )
        # hide popup list
        self.hide_popup_list()
        # reset listboxes
        self.clear_listbox(
            self.LBOX_SCENE, self.LBOX_SHOT, self.LBOX_CHARS
        )
        # update widgets state
        self.slot_update_inputs()
        # event bindings
        self.bind_events(**kw)
    # end def


    def listbox_delete (self, listbox, index):
        """
            removes @listbox item located at given @index;
            reselects new item at @index or 'end';
            returns new rebound index;
        """
        # deselect future removed item
        listbox.last_selected = -1
        # remove item
        listbox.delete(index)
        listbox.selection_clear(0, "end")
        # reselect current index
        index = max(-1, min(listbox.size() - 1, index))
        # selectable index?
        if index >= 0:
            # show newly selected item
            listbox.see(index)
            listbox.selection_set(index)
            listbox.event_generate("<<ListboxSelect>>")
        # end if
        # notify app
        self.events.raise_event("Project:Modified")
        # return new index
        return index
    # end def


    def popup_is_active (self):
        """
            returns True if popup window is detected as active (showing
            up);
        """
        return bool(self.POPUP.state() == "normal")
    # end def


    def replace_text (self, text, start=None, end=None,
                                smart_delete=False, keep_cursor=False):
        """
            replaces text segment found between @start and @end by
            @text contents;
        """
        # inits
        start = start or TK.INSERT
        end = end or TK.INSERT
        # keep cursor
        _cursor = self.TEXT_SHOT.index(TK.INSERT)
        # asked for smart deletion?
        if smart_delete:
            # inits
            _endl = "{} lineend".format(end)
            _text = self.TEXT_SHOT.get(end, _endl)
            # search for a non-alphabetical char
            _found = re.search(r"[^\w\-]", _text)
            # found word separator?
            if _found:
                # update end index
                end = "{} +{}c".format(end, _found.start())
            # not found?
            else:
                # expand to line end
                end = _endl
            # end if
        # end if
        # remove old text
        self.TEXT_SHOT.delete(start, end)
        # insert new text
        self.TEXT_SHOT.insert(start, text)
        # asked to keep cursor?
        if keep_cursor:
            # reset cursor location
            self.TEXT_SHOT.mark_set(TK.INSERT, _cursor)
        # end if
    # end def


    def save_now (self):
        """
            ensures current template is saved before clearing;
        """
        # stop scheduled tasks
        self.async.stop(self.auto_save)
        # force task right now
        self.auto_save()
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # inits
        _rows = json.loads(fname or "[]")
        # update DB table
        self.database.stb_import_shots(_rows)
    # end def


    def show_popup_list (self, *args, **kw):
        """
            event handler: shows autocompletion popup list;
        """
        # ensure no tkinter.messagebox is up there
        try:
            if self.grab_current(): return self.hide_popup_list()
        except:
            return self.hide_popup_list()
        # end try
        # stop pending tasks
        self.async.stop(self.hide_popup_list, self.slot_autocomplete)
        # inits
        choices = kw.get("choices")
        start_index = kw.get("start_index") or TK.INSERT
        self.POPUP.start_index = start_index
        # param controls
        if choices:
            _lb = self.POPUP_LBOX
            _lb.delete(0, "end")
            _lb.insert(0, *choices)
            try:
                _lb.selection_set(_lb.current_index)
                _lb.see(_lb.current_index)
            except:
                _lb.selection_set(0)
                _lb.see(0)
                _lb.current_index = 0
            # end try
            _lb.configure(
                height=min(5, len(choices)),
                width=min(40, max(map(len, choices))),
            )
        # end if
        # recalc pos
        _wtext = self.TEXT_SHOT
        _x, _y, _w, _h = _wtext.bbox(start_index)
        _xi, _yi, _wi, _hi = _wtext.bbox(TK.INSERT)
        _x += _wtext.winfo_rootx()
        _y = _wtext.winfo_rooty() + _h + max(_y, _yi)
        # reset popup window pos
        self.POPUP.geometry("+{}+{}".format(_x, _y))
        # show popup list
        self.POPUP.deiconify()
    # end def


    def slot_autocomplete (self, *args, **kw):
        """
            event handler: a word has been detected in shot text widget
            while buffering keystrokes;
        """
        # inits
        _word = self.get_word(TK.INSERT)
        _si = _word["start_index"]
        # look for matching names
        _names = self.tab_characters.get_matching_names(_word["word"])
        # no matching names for word?
        if not _names:
            # try out full line
            _names = self.tab_characters.get_matching_names(
                self.get_line_contents(TK.INSERT)
            )
            _si = "{} linestart".format(TK.INSERT)
        # end if
        # got matching names?
        if _names:
            # show popup list
            self.show_popup_list(choices=_names, start_index=_si)
        else:
            # hide popup list
            self.hide_popup_list()
        # end if
    # end def


    def slot_characters_item_selected (self, event=None, *args, **kw):
        """
            event handler: listbox item has been selected;
        """
        # inits
        _lb = self.LBOX_CHARS
        _index = self.get_current_selected(_lb)
        # got selected?
        if _index >= 0:
            # inits
            _name = _lb.get(_index)
            # update character's log
            self.LBL_CHARNAME.set(_name)
            self.enable_widget(self.TEXT_CHARLOG, True)
            self.text_set_contents(
                self.TEXT_CHARLOG,
                self.mainframe.tab_characters.get_character_log(_name)
            )
            self.enable_widget(self.TEXT_CHARLOG, False)
        # end if
    # end def


    def slot_on_focus_out (self, event=None, *args, **kw):
        """
            event handler: widget has lost focus;
        """
        self.async.run_after_idle(self.hide_popup_list)
    # end def


    def slot_on_tab_exposed (self, event=None, *args, **kw):
        """
            event handler: tab is now visible;
        """
        # reset last selected scene
        self.slot_reset_selected_scene()
    # end def


    def slot_on_text_keypress (self, event=None, *args, **kw):
        """
            event handler: keyboard keypress for text widget;
        """
        # modified?
        if self.TEXT_SHOT.edit_modified():
            # manage character names
            self.update_character_name()
            # schedule auto-save for later
            self.async.run_after(3000, self.auto_save)
            # notify app
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def slot_on_text_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse click on text widget;
        """
        # widget enabled?
        if self.widget_enabled(self.TEXT_SHOT):
            # manage character names
            self.update_character_name()
        # end if
    # end def


    def slot_popup_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse click on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # stop pending tasks
            self.after_idle(
                self.async.stop,
                self.hide_popup_list,
                self.slot_autocomplete
            )
        # end if
    # end def


    def slot_popup_double_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse double click on popup;
        """
        # do insert text completion
        return self.slot_popup_insert()
    # end def


    def slot_popup_insert (self, event=None, *args, **kw):
        """
            event handler: tab/return keypress on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _lb = self.POPUP_LBOX
            _name = _lb.get(_lb.curselection()[0])
            # replace text
            self.replace_text(
                _name, self.POPUP.start_index, smart_delete=True
            )
            # reset focus
            self.after_idle(self.TEXT_SHOT.focus_set)
            # break tkevent chain
            return "break"
        # end if
    # end def


    def slot_popup_item_selected (self, event=None, *args, **kw):
        """
            event handler: item selected on popup;
        """
        # update current index
        self.POPUP_LBOX.current_index = self.POPUP_LBOX.curselection()[0]
        # break tkevent chain
        return "break"
    # end def


    def slot_popup_key_arrows (self, event=None, *args, **kw):
        """
            event handler: up/down keypress on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _key = event.keysym.lower()
            _lb = self.POPUP_LBOX
            _ci = _lb.current_index
            # update index
            _ci += int(_key == "down") - int(_key == "up")
            # rebind index
            _ci = max(0, min(_ci, _lb.size() - 1))
            # reset selection
            _lb.current_index = _ci
            _lb.selection_clear(0, "end")
            _lb.selection_set(_ci)
            _lb.see(_ci)
            # break tkevent chain
            return "break"
        # end if
    # end def


    def slot_popup_keypress (self, event=None, *args, **kw):
        """
            event handler: any keypress on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _key = event.keysym
            # specific keystrokes
            if _key in ("Escape",):
                # hide popup (transferred to slot_popup_keyrelease)
                pass
            # up/down arrow keys
            elif _key in ("Up", "Down"):
                # manage into popup
                return self.slot_popup_key_arrows(event, *args, **kw)
            # tab/return keystrokes
            elif _key in ("Tab", "Return"):
                # manage into popup
                return self.slot_popup_insert(event, *args, **kw)
            # unsupported keystrokes
            else:
                # delegate event chain
                return None
            # end if
            # break tkevent chain by default
            return "break"
        # end if
    # end def


    def slot_popup_keyrelease (self, event=None, *args, **kw):
        """
            event handler: any keyrelease on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _key = event.keysym
            # specific keystrokes
            if _key in ("Escape",):
                # hide popup
                self.hide_popup_list()
                # break tkevent chain
                return "break"
            # end if
        # end if
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # reset status
        self.TEXT_SHOT.edit_modified(flag)
    # end def


    def slot_reset_selected_scene (self, *args, force_index=None, **kw):
        """
            event handler: resets last selected scene, if any;
        """
        # inits
        _index = (
            force_index or self.get_current_selected(self.LBOX_SCENE)
        )
        # got selected?
        if _index >= 0:
            self.LBOX_SCENE.last_selected = -1
            self.LBOX_SCENE.see(_index)
            self.LBOX_SCENE.selection_set(_index)
            self.slot_scene_item_selected()
        # end if
    # end def


    def slot_scene_item_selected (self, event=None, *args, **kw):
        """
            event handler: listbox item has been selected;
        """
        # save previous shot right now!
        self.save_now()
        # update shot listbox contents along with new scene
        self.slot_update_shot_listbox()
        # update scene text preview
        self.slot_update_scene_preview()
        # update widgets state
        self.slot_update_inputs()
    # end def


    def slot_shot_add (self, *args, **kw):
        """
            event handler: adding new shot to listbox;
        """
        # inits
        _scene = self.get_current_selected(self.LBOX_SCENE) + 1
        # got selected scene?
        if _scene:
            # inits
            _lb = self.LBOX_SHOT
            # try out
            try:
                # get shot number of last item
                _num, _title = self.get_shot_chunks(_lb.get("end"))
                _shot = int(_num.split(".")[-1]) + 1
            except:
                _shot = _lb.size() + 1
            # end try
            _lb.insert(
                "end",
                self.get_formatted_shot_text(
                    self.get_shot_number(_scene, _shot)
                )
            )
            # show selected
            _lb.selection_clear(0, "end")
            _lb.selection_set("end")
            _lb.see("end")
            # update data
            self.slot_shot_item_selected()
            # notify app
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def slot_shot_delete (self, *args, **kw):
        """
            event handler: deleting selected shot from listbox;
        """
        # inits
        _lb = self.LBOX_SHOT
        _index = self.get_current_selected(_lb)
        # got selected?
        if _index >= 0:
            # condition
            _ok = (
                # empty shot text?
                not self.text_get_contents(self.TEXT_SHOT).strip()
                # user confirmed?
                or self.user_confirm_deletion()
            )
            # can delete?
            if _ok:
                # get scene + shot numbers
                _scene, _shot = self.get_scene_shot(_index)
                # remove from database
                self.database.stb_del_shot(_scene, _shot)
                # remove from listbox
                self.listbox_delete(_lb, _index)
            # end if
        # end if
        # update widgets state
        self.slot_update_inputs()
    # end def


    def slot_shot_item_selected (self, event=None, *args, **kw):
        """
            event handler: listbox item has been selected;
        """
        # save previous shot right now!
        self.save_now()
        # try out
        try:
            # inits
            _nb, _title = self.get_shot_chunks(
                self.LBOX_SHOT.get(
                    self.get_current_selected(self.LBOX_SHOT)
                )
            )
            _scene, _shot = _nb.strip("#").split(".")
            # get DB record
            _row = self.database.stb_get_shot(_scene, _shot)
            # reset widgets
            self.LBL_SHOT.set(_nb)
            self.enable_widget(self.ENT_SHOT, True)
            self.ENT_SHOT.delete(0, "end")
            self.ENT_SHOT.insert(0, _title)
            self.enable_widget(self.TEXT_SHOT, True)
            self.text_set_contents(self.TEXT_SHOT, _row["text"])
            # set focus on relevant widget
            if not _title:
                self.after_idle(self.ENT_SHOT.focus_set)
            else:
                self.after_idle(self.TEXT_SHOT.focus_set)
            # end if
        except:
            pass
        # end try
        # update widgets state
        self.slot_update_inputs()
    # end def


    def slot_shot_purge (self, *args, **kw):
        """
            event handler: purges shot listbox;
        """
        # user confirmed purge?
        if self.user_confirm_purge():
            # purge shots in DB
            self.database.stb_purge_shots(
                self.get_current_selected(self.LBOX_SCENE) + 1
            )
            # update shot listbox
            self.slot_update_shot_listbox()
        # end if
        # update widgets state
        self.slot_update_inputs()
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # clear shots in DB
        self.database.stb_clear_shots()
        # reset listboxes
        self.clear_listbox(
            self.LBOX_SCENE, self.LBOX_SHOT, self.LBOX_CHARS
        )
        # update widgets state
        self.slot_update_inputs()
    # end def


    def slot_update_characters_listbox (self, *args, **kw):
        """
            event handler: updates character names listbox;
        """
        # inits
        _lb = self.LBOX_CHARS
        _contents = kw.get("contents") or []
        # clear all
        self.clear_listbox(_lb)
        # reset contents
        _lb.insert(0, *_contents)
    # end def


    def slot_update_inputs (self, *args, **kw):
        """
            event handler: updates all inputs state;
        """
        # inits
        _cur_scene = bool(
            self.get_current_selected(self.LBOX_SCENE) + 1
        )
        _cur_shot = bool(
            self.get_current_selected(self.LBOX_SHOT) + 1
        )
        _cur_char = bool(
            self.get_current_selected(self.LBOX_CHARS) + 1
        )
        # buttons reset
        self.enable_widget(self.BTN_ADD, _cur_scene)
        self.enable_widget(self.BTN_DEL, _cur_shot)
        self.enable_widget(self.BTN_PURGE, bool(self.LBOX_SHOT.size()))
        # scene reset
        if not _cur_scene:
            # clear scene number
            self.LBL_SCENE.set("")
            # clear and disable
            self.clear_text(self.TEXT_SCENE)
        # end if
        # shot reset
        if _cur_shot:
            # enable widgets
            self.enable_widget(self.ENT_SHOT, True)
            self.enable_widget(self.TEXT_SHOT, True)
        else:
            # clear shot number
            self.LBL_SHOT.set("")
            # clear and disable
            self.clear_entry(self.ENT_SHOT)
            self.clear_text(self.TEXT_SHOT)
        # end if
        # characters reset
        if not _cur_char:
            # clear character's log
            self.LBL_CHARNAME.set("")
            self.clear_text(self.TEXT_CHARLOG)
        # end if
    # end def


    def slot_update_scene_listbox (self, *args, **kw):
        """
            event handler: updates scene listbox contents;
        """
        # get contents
        _lb = self.LBOX_SCENE
        _lb.text_lines = kw.get("lines") or list()
        _contents = kw.get("contents") or tuple()
        # reset listbox
        self.clear_listbox(_lb)
        _lb.insert(0, *_contents)
        self.get_current_selected(
            _lb, force_index=kw.get("current_selected")
        )
        # update selection
        self.slot_scene_item_selected()
        # CAUTION:
        """
            for a very strange reason, tkinter listboxes cannot show
            one selection per object;
            selection focus is grabbed from one to another;
            must manage this with mappings;
        """
        # currently mapped (visible)?
        if self.winfo_ismapped():
            # reset selection
            self.LBOX_SCENE.selection_set(
                self.get_current_selected(self.LBOX_SCENE)
            )
        # end if
    # end def


    def slot_update_scene_preview (self, *args, **kw):
        """
            event handler: updates scene preview text contents along
            with current scene selection;
        """
        # inits
        _lb = self.LBOX_SCENE
        _index = self.get_current_selected(_lb)
        # got selected?
        if _index >= 0:
            # update scene number
            self.LBL_SCENE.set("#{}".format(_index + 1))
            # inits
            _preview = self.TEXT_SCENE
            _scenario = self.mainframe.tab_scenario.TEXT
            _start = float(_lb.text_lines[_index])
            try:
                _end = "{}.0".format(_lb.text_lines[_index+1])
            except:
                _end = "end"
            # end try
            _contents = _scenario.get_tagged_text(_start, _end)
            # set text preview
            self.clear_text(_preview)
            self.enable_widget(_preview, True)
            _preview.insert("1.0", *_contents)
            self.enable_widget(_preview, False)
            # reset styles
            _scenario.copy_styles_into(_preview)
        # end if
    # end def


    def slot_update_shot_listbox (self, *args, **kw):
        """
            event handler: updates shot listbox contents along with
            current scene selection;
        """
        # get scene number
        _scene = self.get_current_selected(self.LBOX_SCENE) + 1
        # got selected?
        if _scene:
            # get shot listbox contents
            _contents = self.get_shot_listbox_contents(_scene)
            # update listbox contents
            self.clear_listbox(self.LBOX_SHOT)
            self.LBOX_SHOT.insert(0, *_contents)
        # end if
    # end def


    def update_character_name (self, *args, **kw):
        """
            event handler: updates character's name, if any;
        """
        # inits
        _line = self.get_line_contents(TK.INSERT)
        _name, _start_index = self.tab_characters.find_nearest_name(
            _line, self.get_column_index(TK.INSERT)
        )
        # known character name?
        if self.tab_characters.is_registered(_name):
            # name not in good format?
            if _name not in _line:
                # update name into text contents
                _index = "{} linestart+{{}}c".format(TK.INSERT)
                self.replace_text(
                    _name,
                    _index.format(_start_index),
                    _index.format(_start_index + len(_name)),
                    keep_cursor=True,
                )
            # end if
            # no need to autocomplete
            self.hide_popup_list()
        # unknown char name
        else:
            # look out for autocompletion
            self.async.run_after_idle(self.slot_autocomplete)
        # end if
    # end def


    def update_listbox_item (self, listbox, index, text):
        """
            updates @listbox item located at given @index with new
            @text contents;
        """
        # save current selection
        _sel = listbox.curselection()
        # update listbox item
        listbox.delete(index)
        listbox.insert(index, text)
        # reset current selection
        if _sel:
            # show item
            listbox.see(_sel[0])
            # select again
            listbox.selection_set(_sel[0])
        # end if
    # end def


    def user_confirm_deletion (self):
        """
            asks user for deletion confirmation;
        """
        return MB.askyesno(
            title=_("Attention"),
            message=_("Do you really want to delete selected shot?"),
            parent=self,
        )
    # end def


    def user_confirm_purge (self):
        """
            asks user for purge confirmation;
        """
        return MB.askyesno(
            title=_("Attention"),
            message=_(
                "Do you really want to remove *ALL* "
                "empty shots from list?"
            ),
            parent=self,
        )
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class ProjectTabStoryboard
