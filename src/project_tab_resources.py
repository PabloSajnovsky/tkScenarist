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
import copy
import json
import tkinter.simpledialog as SD
import tkinter.messagebox as MB
import tkRAD
import tkRAD.core.async as ASYNC
from tkRAD.core import tools


class ProjectTabResources (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    def auto_save (self, *args, **kw):
        """
            event handler;
            automatically saves data, if any;
        """
        # inits
        _lb = self.LBOX_ITEM
        _index = _lb.last_selected
        # got selected?
        if _index >= 0:
            # inits
            _dict = dict()
            for _key, _w in self.ENTRIES.items():
                _dict[_key] = _w.get()
            # end for
            _dict.update(
                notes=self.text_get_contents(self.TEXT).strip(),
            )
            # got data to save?
            if any(_dict.values()):
                # foreign key inits
                _dict.update(
                    fk_type=self.get_fk_type(),
                )
                # update record in database
                self.database.res_update_item(**_dict)
            # end if
            self.database.dump_tables("resource_items")
        # end if
    # end def


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Resources:Item:Add":
                    self.slot_res_item_add,
                "Resources:Item:Delete":
                    self.slot_res_item_delete,
                "Resources:Item:Rename":
                    self.slot_res_item_rename,

                "Resources:Section:Add":
                    self.slot_res_section_add,
                "Resources:Section:Delete":
                    self.slot_res_section_delete,
                "Resources:Section:Rename":
                    self.slot_res_section_rename,

                "Resources:Type:Add":
                    self.slot_res_type_add,
                "Resources:Type:Delete":
                    self.slot_res_type_delete,
                "Resources:Type:Rename":
                    self.slot_res_type_rename,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        self.CBO_TYPE.bind(
            "<<ComboboxSelected>>", self.slot_combo_type_selected
        )
        self.CBO_SECTION.bind(
            "<<ComboboxSelected>>", self.slot_combo_section_selected
        )
        self.LBOX_ITEM.bind(
            "<<ListboxSelect>>", self.slot_listbox_item_selected
        )
        self.TEXT.bind("<KeyRelease>", self.slot_on_text_keypress)
        for _w in self.ENTRIES.values():
            _w.bind("<KeyRelease>", self.slot_on_text_keypress)
        # end for
    # end def


    def clear_combo (self, *widgets):
        """
            clears contents for combobox widget(s);
        """
        # browse widgets
        for _w in widgets:
            # clear widget
            _w.delete(0, "end")
            # clear selection
            _w.selection_clear()
            # clear items
            _w.items = dict()
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
            # clear items
            _w.items = dict()
            # reset last selected
            _w.last_selected = -1
        # end for
    # end def


    def combo_delete_item (self, combo):
        """
            generic procedure for deleting an item from a combobox;
        """
        print("combo_delete_item")
        # inits
        _index = combo.current()
        # got selection?
        if _index >= 0:
            # inits
            _label = combo.get()
            # user confirmed?
            if self.user_confirm_deletion(_label):
                # remove from items dict
                _rowid = combo.items.pop(_label)
                # remove from database
                self.database.res_del_type(_rowid)
                # clear listbox
                self.clear_listbox(self.LBOX_ITEM)
                self.slot_update_inputs()
                # remove from widget
                _items = list(combo.cget("values"))
                _items.pop(_index)
                combo.configure(values=_items)
                # update selection
                _index = max(-1, min(len(_items) - 1, _index))
                combo.current(_index)
                combo.event_generate("<<ComboboxSelected>>")
                # notify app
                self.events.raise_event("Project:Modified")
            # end if
        # end if
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


    def get_current_selected (self):
        """
            returns index of current selection or None, otherwise;
        """
        # inits
        _lb = self.LBOX_ITEM
        _sel = _lb.curselection()
        # got selected?
        if _sel:
            # update pointer value
            _lb.last_selected = _sel[0]
        # empty listbox?
        elif not _lb.size():
            # force clear-ups
            self.clear_listbox(_lb)
        # end if
        # return result
        return _lb.last_selected
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # inits
        fcontents = ""                                                      # FIXME
        #~ fcontents = self.text_get_contents(self.text_resources)
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_fk_type (self):
        """
            returns items listbox current selected fk_type id;
        """
        return self.LBOX_ITEM.items[
            self.LBOX_ITEM.get(self.LBOX_ITEM.last_selected)
        ]
    # end def


    def get_res_items (self):
        """
            retrieves resource items along with current resources type
            and section selected in combos;
        """
        return self.database.res_get_types(
            fk_parent=self.CBO_SECTION.items[self.CBO_SECTION.get()]
        )
    # end def


    def get_res_section (self):
        """
            retrieves resources section along with current resources
            type selected in combo;
        """
        return self.database.res_get_types(
            fk_parent=self.CBO_TYPE.items[self.CBO_TYPE.get()]
        )
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.mainwindow = self.winfo_toplevel()
        self.mainframe = self.mainwindow.mainframe
        self.database = self.mainwindow.database
        self.text_clear_contents = self.mainwindow.text_clear_contents
        self.text_get_contents = self.mainwindow.text_get_contents
        self.text_set_contents = self.mainwindow.text_set_contents
        self.async = ASYNC.get_async_manager()
        # looks for ^/xml/widget/tab_resources.xml
        self.xml_build("tab_resources")
        # widget inits
        _readonly = ["readonly"]
        self.CBO_TYPE = self.combo_res_type
        self.CBO_TYPE.state(_readonly)
        self.CBO_SECTION = self.combo_res_section
        self.CBO_SECTION.state(_readonly)
        self.LBOX_ITEM = self.listbox_res_item
        self.ENTRIES = {
            "name": self.entry_res_name,
            "role": self.entry_res_role,
            "contact": self.entry_res_contact,
            "phone": self.entry_res_phone,
            "email": self.entry_res_email,
        }
        self.TEXT = self.text_notes
        # event bindings
        self.bind_events(**kw)
        # reset once
        self.slot_tab_reset()
    # end def


    def reset_resources (self):
        """
            resets all resources (DB, combos, listbox);
        """
        # clear in DB
        self.database.res_reset()
        # reset combos + listbox
        self.clear_combo(self.CBO_TYPE, self.CBO_SECTION)
        self.clear_listbox(self.LBOX_ITEM)
        # fill types
        _dict = self.database.res_get_types()
        self.CBO_TYPE.configure(values=sorted(_dict.keys()))
        self.CBO_TYPE.items = _dict
        # got selection?
        if _dict:
            self.CBO_TYPE.current(0)
            self.slot_combo_type_selected()
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
        # set text widget contents
        #~ self.text_set_contents(self.text_resources, fname)
        pass
    # end def


    def slot_combo_section_selected (self, event=None, *args, **kw):
        """
            event handler: item has been selected in combobox;
        """
        # save last item
        self.save_now()
        # inits
        _dict = self.get_res_items()
        # clear listbox
        self.clear_listbox(self.LBOX_ITEM)
        # fill values
        self.LBOX_ITEM.insert(0, *sorted(_dict.keys()))
        self.LBOX_ITEM.items = _dict
        # update widgets state
        self.slot_update_inputs()
    # end def


    def slot_combo_type_selected (self, event=None, *args, **kw):
        """
            event handler: item has been selected in combobox;
        """
        # save last item
        self.save_now()
        # inits
        _dict = self.get_res_section()
        # clear listbox
        self.clear_listbox(self.LBOX_ITEM)
        # reset combo
        self.clear_combo(self.CBO_SECTION)
        # fill values
        self.CBO_SECTION.configure(values=sorted(_dict.keys()))
        self.CBO_SECTION.items = _dict
        # got selection?
        if _dict:
            # select first
            self.CBO_SECTION.current(0)
            self.slot_combo_section_selected()
        # end if
    # end def


    def slot_listbox_item_selected (self, event=None, *args, **kw):
        """
            event handler: item has been selected in listbox;
        """
        # save last item
        self.save_now()
        # update inputs state
        self.slot_update_inputs()
        # inits
        _index = self.get_current_selected()
        # got real selection?
        if _index >= 0:
            # inits
            _row = self.database.res_get_item(self.get_fk_type())
            # browse ttk entries
            for _key, _w in self.ENTRIES.items():
                _w.insert(0, _row.get(_key) or "")
            # end for
            # update text notes
            self.text_set_contents(self.TEXT, _row.get("notes") or "")
            # set focus on first entry
            self.after_idle(self.ENTRIES["name"].focus_set)
        # end if
    # end def


    def slot_on_text_keypress (self, event=None, *args, **kw):
        """
            event handler: keyboard keypress for text widget;
        """
        # no modifiers?
        if not (event.state & STATE_MASK):
            # schedule auto-save for later
            self.async.run_after(3000, self.auto_save)
            # notify app
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def slot_res_item_add (self, event=None, *args, **kw):
        """
            event handler: button 'add' clicked;
        """
        print("slot_res_item_add")
    # end def


    def slot_res_item_delete (self, event=None, *args, **kw):
        """
            event handler: button 'delete' clicked;
        """
        # inits
        _index = self.get_current_selected()
        # got selection?
        if _index >= 0:
            # inits
            _lb = self.LBOX_ITEM
            _label = _lb.get(_index)
            # user confirmed?
            if self.user_confirm_deletion(_label):
                # remove from items dict
                _rowid = _lb.items.pop(_label)
                # remove from database
                self.database.res_del_type(_rowid)
                # remove from widget
                _lb.delete(_index)
                # do some clean-ups
                self.slot_update_inputs()
                # rebind index
                _index = max(-1, min(_lb.size() - 1, _index))
                # can select again?
                if _index >= 0:
                    _lb.see(_index)
                    _lb.selection_set(_index)
                    self.slot_listbox_item_selected()
                # end if
                # notify app
                self.events.raise_event("Project:Modified")
            # end if
        # end if
    # end def


    def slot_res_item_rename (self, event=None, *args, **kw):
        """
            event handler: button 'rename' clicked;
        """
        print("slot_res_item_rename")
    # end def


    def slot_res_section_add (self, event=None, *args, **kw):
        """
            event handler: button 'add' clicked;
        """
        print("slot_res_section_add")
    # end def


    def slot_res_section_delete (self, event=None, *args, **kw):
        """
            event handler: button 'delete' clicked;
        """
        # delegate to generic procedure
        self.combo_delete_item(self.CBO_SECTION)
    # end def


    def slot_res_section_rename (self, event=None, *args, **kw):
        """
            event handler: button 'rename' clicked;
        """
        print("slot_res_section_rename")
    # end def


    def slot_res_type_add (self, event=None, *args, **kw):
        """
            event handler: button 'add' clicked;
        """
        print("slot_res_type_add")
    # end def


    def slot_res_type_delete (self, event=None, *args, **kw):
        """
            event handler: button 'delete' clicked;
        """
        # delegate to generic procedure
        self.combo_delete_item(self.CBO_TYPE)
    # end def


    def slot_res_type_rename (self, event=None, *args, **kw):
        """
            event handler: button 'rename' clicked;
        """
        print("slot_res_type_rename")
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # reset DB, combos and so on
        self.reset_resources()
    # end def


    def slot_update_inputs (self, *args, **kw):
        """
            event handler: updates all input widgets;
        """
        # inits
        _sel = self.get_current_selected() + 1
        # update buttons
        self.enable_widget(self.btn_delete_item, _sel)
        self.enable_widget(self.btn_rename_item, _sel)
        # browse ttkentry widgets
        for _w in self.ENTRIES.values():
            # enable widget
            self.enable_widget(_w, True)
            # clear widget
            _w.delete(0, "end")
            # disable widget if not selected
            self.enable_widget(_w, _sel)
        # end for
        # enable text notes
        self.enable_widget(self.TEXT, True)
        # clear text
        self.text_clear_contents(self.TEXT)
        # disable text notes if not selected
        self.enable_widget(self.TEXT, _sel)
    # end def


    def user_confirm_deletion (self, label):
        """
            shows user confirmation dialog for deletion procedure;
            returns True on confirmation, False otherwise;
        """
        return MB.askyesno(
            title=_("Attention"),
            message=_(
                "Do you really want to delete\n'{item}'?"
            ).format(item=label),
            parent=self,
        )
    # end def

# end class ProjectTabResources
