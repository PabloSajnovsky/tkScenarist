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
import tkinter.messagebox as MB
import tkinter.simpledialog as SD
import tkRAD
import tkRAD.core.async as ASYNC


class ProjectTabCharacters (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    def auto_save (self, *args, **kw):
        """
            event handler;
            automatically saves data, if any;
        """
        # get current name
        _name = self.get_current_name()
        # got something?
        if _name:
            # save character's log contents
            self.character_logs[_name] = \
                    self.text_get_contents(self.TEXT)
            # confirm
        # end if
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Characters:List:Add": self.slot_list_add,
                "Characters:List:Delete": self.slot_list_delete,
                "Characters:List:Purge": self.slot_list_purge,
                "Characters:List:Rename": self.slot_list_rename,
                "Characters:Name:Selected": self.slot_name_selected,

                "Project:Modified": self.slot_project_modified,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        _lb = self.LISTBOX
        _lb.bind("<ButtonRelease-1>", self.slot_on_listbox_click)
        _lb.bind("<KeyRelease-Up>", self.slot_on_listbox_click)
        _lb.bind("<KeyRelease-Down>", self.slot_on_listbox_click)
        self.TEXT.bind("<KeyRelease>", self.slot_on_text_keypress)
    # end def


    def canvas_add_name (self, name):
        """
            adds a new name into canvas widget;
        """
        # delegate to widget
        self.CANVAS.character_name_add(name)
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def canvas_delete_name (self, name):
        """
            deletes a name from canvas widget;
        """
        # delegate to widget
        self.CANVAS.character_name_remove(name)
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def canvas_rename (self, old_name, new_name):
        """
            renames an item into canvas widget;
        """
        # delegate to widget
        self.CANVAS.rename_name(old_name, new_name)
        # project has been modified
        self.events.raise_event("Project:Modified")
    # end def


    def do_add_character_name (self, name, show_error=False, **kw):
        """
            effective procedure for adding a new character;
        """
        # param inits
        name = self.format_name(name)
        # param controls
        if name:
            # name already exists?
            if name in self.character_logs:
                # must show error?
                if show_error:
                    # show error
                    self.error_already_exists(name)
                # use indexed names?
                else:
                    # CAUTION: *NOT* a good idea in practice /!\
                    pass
                # end if
            # new character name
            else:
                # set into listbox
                self.listbox_add_name(name)
                # set into canvas
                self.canvas_add_name(name)
            # end if
        # end if
    # end def


    def do_delete_character_name (self, name, show_error=False, **kw):
        """
            effective procedure for deleting a character name;
        """
        # param inits
        name = self.format_name(name)
        # param controls
        if name:
            # name exists?
            if name in self.character_logs:
                # remove from listbox
                self.listbox_delete_name(name)
                # remove from canvas
                self.canvas_delete_name(name)
            # not found
            elif show_error:
                # show error
                self.error_not_found(name)
            # end if
        # end if
    # end def


    def do_purge_character_names (self, show_error=False, **kw):
        """
            effective procedure for purging list of orphan names;
        """
        # inits
        text = self.get_scenario_text()
        names = tuple(self.character_logs.keys())
        # browse names
        for _name in names:
            # not mentioned in scenario?
            if not self.is_mentioned(_name, text):
                # delete name from list
                self.do_delete_character_name(_name)
            # end if
        # end for
    # end def


    def do_rename_character_name (self, old_name, new_name, show_error=False, **kw):
        """
            effective procedure for renaming a character;
        """
        # param inits
        old_name = self.format_name(old_name)
        new_name = self.format_name(new_name)
        # param controls
        if old_name and new_name and new_name != old_name:
            # new name already exists?
            if new_name in self.character_logs:
                # must show error?
                if show_error:
                    # show error
                    self.error_already_exists(new_name)
                # end if
            # rename character's name
            else:
                # set into listbox
                self.listbox_rename(old_name, new_name)
                # set into canvas
                self.canvas_rename(old_name, new_name)
            # end if
        # end if
    # end def


    def do_select_character_name (self, name=None):
        """
            effective procedure for selecting a character name into
            listbox;
        """
        # inits
        name = name or self.current_name
        # param controls
        if name in self.character_logs:
            # inits
            _index = sorted(self.character_logs).index(name)
            _lb = self.LISTBOX
            # do select name
            _lb.selection_clear(0, "end")
            _lb.selection_set(_index)
            _lb.see(_index)
            # update character's history log
            self.update_character_log()
        # end if
    # end def


    def enable_widget (self, widget, state):
        """
            enables/disables a tkinter widget along with @state value;
            if @state is None, widget keeps unchanged;
        """
        # param controls
        if state is not None:
            widget.configure(
                state={True: "normal"}.get(bool(state), "disabled")
            )
        # end if
    # end def


    def error_already_exists (self, name):
        """
            shows error dialog box;
        """
        # show error
        MB.showwarning(
            title=_("Attention"),
            message=_(
                "Character name '{name}' already exists."
            ).format(name=name),
            parent=self,
        )
    # end def


    def error_not_found (self, name):
        """
            shows error dialog box;
        """
        # show error
        MB.showwarning(
            title=_("Attention"),
            message=_(
                "Character name '{name}' has *NOT* "
                "been found in list."
            ).format(name=name),
            parent=self,
        )
    # end def


    def format_name (self, name):
        """
            returns formatted name along internal policy;
        """
        return str(name).strip().upper()
    # end def


    def get_current_name (self):
        """
            retrieves self.current_name if name list is *NOT* empty;
            resets self.current_name and returns empty string
            otherwise;
        """
        # name list is empty?
        if not self.character_logs:
            # reset current name
            self.current_name = ""
        # end if
        # return current name
        return self.current_name
    # end def



    def get_file_contents (self, fname):
        """
            returns formatted string as file contents;
        """
        # multiple files and contents
        _dict = dict()
        # list of character names
        _fname = fname["names"]
        _fcontents = "\n".join(self.LISTBOX.get(0, "end"))
        _dict[_fname] = _fcontents
        # character logs
        _fname = fname["logs"]
        _fcontents = ""                                                     # FIXME
        _dict[_fname] = _fcontents
        # character relations
        _fname = fname["relations"]
        _fcontents = ""                                                     # FIXME
        _dict[_fname] = _fcontents
        # always return a dict
        return _dict
    # end def


    def get_scenario_text (self):
        """
            retrieves tab_scenario.text_scenario text contents;
        """
        return self.text_get_contents(
                self.mainframe.tab_scenario.text_scenario
        )
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.mainwindow = self.winfo_toplevel()
        self.mainframe = self.mainwindow.mainframe
        self.text_clear_contents = self.mainwindow.text_clear_contents
        self.text_get_contents = self.mainwindow.text_get_contents
        self.text_set_contents = self.mainwindow.text_set_contents
        self.async = ASYNC.get_async_manager()
        self.character_logs = dict()
        self.current_name = ""
        # looks for ^/xml/widget/tab_characters.xml
        self.xml_build("tab_characters")
        # XML widget ALIAS inits
        self.CANVAS = self.canvas_characters_relations
        self.LISTBOX = self.listbox_characters_list
        self.TEXT = self.text_characters_log
        # event bindings
        self.bind_events(**kw)
        # reset tab
        self.after_idle(self.slot_tab_reset)
    # end def


    def is_mentioned (self, name, text=None):
        """
            returns True if @name is mentioned at least once in @text,
            False otherwise;
            uses scenario's text contents if @text is omitted;
        """
        # param inits
        text = text or self.get_scenario_text()
        # look if name is mentioned in text
        return bool(re.search(r"(?i)\b{}\b".format(name), text))
    # end def


    def listbox_add_name (self, name):
        """
            adds a new name into listbox widget;
        """
        # param controls
        if name:
            # set new name in logs
            self.character_logs[name] = _(
                "Put here some character's history"
            )
            # update listbox
            self.update_listbox(new_name=name)
            # project has been modified
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def listbox_delete_name (self, name, *args, **kw):
        """
            deletes a name from listbox widget;
        """
        # param controls
        if name:
            # set new name in logs
            self.character_logs.pop(name, None)
            # no more current name
            self.current_name = ""
            # update keywords
            kw.update(delete=True)
            # update listbox
            self.update_listbox(*args, **kw)
            # project has been modified
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def listbox_get_selected_name (self):
        """
            retrieves currently selected name, if any;
        """
        # inits
        _sel = self.LISTBOX.curselection()
        # got selection?
        if _sel:
            # get selected name
            return self.LISTBOX.get(_sel[0])
        # failed
        else:
            # maybe current unfocused name?
            return self.get_current_name()
        # end if
    # end def


    def listbox_rename (self, old_name, new_name):
        """
            renames an item into listbox widget;
        """
        # param controls
        if old_name and new_name and new_name != old_name:
            # rename name in logs
            self.character_logs[new_name] = self.character_logs[old_name]
            # remove old name from listbox
            self.listbox_delete_name(old_name, new_name=new_name)
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


    def slot_list_add (self, *args, **kw):
        """
            event handler for characters list;
        """
        # inits
        _name = SD.askstring(
            _("Please, insert"), _("Character name"), parent=self
        )
        # got something?
        if _name:
            # add a new character name
            self.do_add_character_name(_name, show_error=True)
        # end if
    # end def


    def slot_list_delete (self, *args, **kw):
        """
            event handler for characters list;
        """
        # get name from listbox
        _name = self.listbox_get_selected_name()
        # got something?
        if _name:
            # name mentioned in scenario text?
            if self.is_mentioned(_name):
                # not allowed
                MB.showwarning(
                    title=_("Attention"),
                    message=_(
                        "Cannot delete name '{name}'.\n"
                        "This character name is still "
                        "mentioned into scenario's text."
                    ).format(name=_name),
                    parent=self,
                )
            # ask for user confirmation
            elif self.user_confirm_deletion(_name):
                # delete character's name
                self.do_delete_character_name(_name)
            # end if
        # end if
    # end def


    def slot_list_purge (self, *args, **kw):
        """
            event handler for characters list;
        """
        # list not empty?
        if self.character_logs:
            # user confirmed?
            if self.user_confirm_purge():
                # force task right now
                self.save_now()
                # purge list from orphan names
                self.do_purge_character_names()
            # end if
        # end if
    # end def


    def slot_list_rename (self, *args, **kw):
        """
            event handler for characters list;
        """
        # get name from listbox
        _old_name = self.listbox_get_selected_name()
        # got something?
        if _old_name:
            # name mentioned in scenario text?
            if self.is_mentioned(_old_name):
                # not allowed
                MB.showwarning(
                    title=_("Attention"),
                    message=_(
                        "Cannot rename '{name}'.\n"
                        "This character name is still "
                        "mentioned into scenario's text."
                    ).format(name=_old_name),
                    parent=self,
                )
            # allowed to rename
            else:
                # inits
                _new_name = SD.askstring(
                    _("Please, insert"),
                    _("Renaming"),
                    initialvalue=_old_name,
                    parent=self,
                )
                # got something?
                if _new_name:
                    # force task right now
                    self.save_now()
                    # rename character name
                    self.do_rename_character_name(
                        _old_name, _new_name, show_error=True
                    )
                # end if
                # reselect name
                self.do_select_character_name()
            # end if
        # end if
    # end def


    def slot_name_selected (self, *args, name=None, **kw):
        """
            event handler: a character name has been selected
            somewhere;
        """
        # really select name
        self.do_select_character_name(name)
    # end def


    def slot_on_listbox_click (self, event=None, *args, **kw):
        """
            event handler: mouse click on listbox;
        """
        # get selected name
        _name = self.listbox_get_selected_name()
        # new selection?
        if _name != self.current_name:
            # update preview
            self.update_character_log()
        # end if
    # end def


    def slot_on_text_keypress (self, event=None, *args, **kw):
        """
            event handler: keyboard keypress for text widget;
        """
        # schedule auto-save for later
        self.async.run_after(5000, self.auto_save)
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # reset status
        self.TEXT.edit_modified(flag)
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # member inits
        self.character_logs.clear()
        # clear widgets
        self.update_listbox()
        self.CANVAS.reset()
    # end def


    def update_character_log (self, *args, new_name=None, **kw):
        """
            event handler for showing off selected character's log;
        """
        # force task right now
        self.save_now()
        # get selected name
        _name = new_name or self.listbox_get_selected_name()
        # other inits
        _info = self.get_stringvar("log_character_name")
        _text = self.TEXT
        # enable widget
        self.enable_widget(_text, True)
        # got selection?
        if _name:
            # update selected
            self.current_name = _name
            # update info
            _info.set(_name)
            # update text widget
            self.text_set_contents(_text, self.character_logs[_name])
            # new name?
            if new_name:
                # go to edit mode
                _text.focus_set()
            # end if
        # nothing selected
        else:
            # clear all
            self.current_name = ""
            _info.set("")
            self.text_clear_contents(_text)
            # disable widget
            self.enable_widget(_text, False)
        # end if
    # end def


    def update_listbox (self, *args, **kw):
        """
            event handler for updating listbox contents along with
            @self.character_logs;
        """
        # inits
        _lb = self.LISTBOX
        _names = sorted(self.character_logs)
        _flag = bool(_names)
        _new_name = kw.get("new_name")
        _index = 0
        # pending deletion?
        if kw.get("delete"):
            # keep index
            if _lb.curselection():
                # reset index
                _index = min(_lb.curselection()[0], len(_names) - 1)
            # end if
        # end if
        # clear listbox
        _lb.delete(0, "end")
        # got list?
        if _names:
            # fill listbox
            _lb.insert(0, *_names)
            # new name?
            if _new_name:
                # inits
                _index = _names.index(_new_name)
                # show selected
                _lb.selection_set(_index)
                _lb.see(_index)
            # return to home index
            else:
                # select last selected
                _lb.selection_set(_index)
                _lb.see(_index)
            # end if
        # end if
        # enable/disable widgets
        self.enable_widget(self.btn_delete, _flag)
        self.enable_widget(self.btn_rename, _flag)
        self.enable_widget(self.btn_purge, _flag)
        # update character's log preview
        self.update_character_log(*args, **kw)
    # end def


    def user_confirm_deletion (self, name):
        """
            user confirmation dialog;
        """
        return MB.askyesno(
            title=_("Question"),
            message=_(
                "Character '{name}' has *NOT* "
                "been found into scenario's text.\n"
                "Do you really want to delete "
                "this character?"
            ).format(name=name),
            parent=self,
        )
    # end def


    def user_confirm_purge (self):
        """
            user confirmation dialog;
        """
        return MB.askyesno(
            title=_("Question"),
            message=_(
                "Do you really want to delete *ALL* names "
                "that are *NOT* mentioned into scenario's text?"
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

# end class ProjectTabCharacters
