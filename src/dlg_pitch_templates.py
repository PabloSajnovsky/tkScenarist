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
import os
import os.path as OP
import glob
from tkinter import filedialog as FD
from tkinter import messagebox as MB
import tkRAD.core.path as P
import tkRAD.core.async as ASYNC
import tkRAD.widgets.rad_dialog as DLG


class PitchTemplatesDialog (DLG.RADButtonsDialog):
    """
        Pitch templates management dialog;
    """

    # class constant defs
    DEFAULT_DIR = "^/data/templates/pitch/"
    FILE_EXT = ".txt"
    FILE_PATTERN = "*" + FILE_EXT
    FILE_TYPES = [
        (_("Text files"), FILE_PATTERN),
        (_("All files"), "*.*"),
    ]


    def auto_save (self, *args, **kw):
        """
            event handler;
            automatically saves current edited template, if any;
        """
        # got something to save?
        if OP.isfile(self.current_fpath):
            # inits
            _text = self.container.text_template_preview
            # save file
            with open(self.current_fpath, "w") as _file:
                # write text contents
                _file.write(_text.get("1.0", "end").rstrip())
            # end with
        # end if
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Template:Browse": self.slot_template_browse,
                "Dialog:Template:Delete": self.slot_template_delete,
                "Dialog:Template:New": self.slot_template_new,
                "Dialog:Template:ResetDir": self.slot_template_reset_dir,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
        _lb = self.container.listbox_templates_list
        _lb.bind("<ButtonRelease-1>", self.slot_on_listbox_click)
        _lb.bind("<KeyRelease-Up>", self.slot_on_listbox_click)
        _lb.bind("<KeyRelease-Down>", self.slot_on_listbox_click)
        self.container.text_template_preview.bind(
            "<KeyRelease>", self.slot_on_text_keypress
        )
    # end def


    def clean_name (self, fpath):
        """
            returns filename without file extension;
        """
        return OP.splitext(OP.basename(fpath))[0]
    # end def


    def clear_preview (self, lock=False):
        """
            clears up template preview frame widgets;
        """
        # inits
        _text = self.container.text_template_preview
        # backup state
        _flag = self.widget_enabled(_text) and not lock
        # enable
        self.enable_widget(_text, True)
        # clear
        _text.delete("1.0", "end")
        # restore previous state
        self.enable_widget(_text, _flag)
        # clear up template name
        self.set_template_name("")
    # end def


    @property
    def current_dir (self):
        """
            project's current working directory;
            normalized to comply with tkRAD.path.support;
        """
        return self.__current_dir
    # end def

    @current_dir.setter
    def current_dir (self, value):
        # inits
        value = P.normalize(value)
        # param controls
        if OP.isdir(value):
            # inits
            self.__current_dir = value
            # auto-update options
            self.options["dirs"]["pitch_template_dir"] = value
            # update info
            self.container.get_stringvar("current_dir")\
                .set(P.shorten_path(value, limit=70))
        else:
            raise NotADirectoryError("not a directory.")
        # end if
    # end def

    @current_dir.deleter
    def current_dir (self):
        del self.__current_dir
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


    def get_listbox_fpath (self):
        """
            retrieves filepath from current listbox selection;
        """
        # inits
        _lb = self.container.listbox_templates_list
        _cursel = _lb.curselection()
        # got selection?
        if _cursel:
            # index
            _index = _cursel[0]
            # show off selected
            _lb.see(_index)
            # get selected text
            _text = _lb.get(_index)
            # rebuild filepath
            _fpath = OP.join(self.current_dir, _text + self.FILE_EXT)
            # ensure filepath still OK
            if OP.isfile(_fpath):
                # ok, let's go
                return _fpath
            # end if
        # end if
        # no path by there
        return ""
    # end def


    def get_template_name (self):
        """
            retrieves template name;
        """
        return self.container.get_stringvar("template_name").get()
    # end def


    def init_widget (self, **kw):
        r"""
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_pitch_templates.xml
            xml="dlg_pitch_templates",
        )
        # member inits
        self.DEFAULT_DIR = P.normalize(_(self.DEFAULT_DIR))
        self.current_fpath = ""
        self.async = ASYNC.get_async_manager()
        self.update_current_dir(
            self.options.get(
                "dirs",
                "pitch_templates_dir",
                fallback=self.DEFAULT_DIR
            )
        )
        # event bindings
        self.bind_events()
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


    def set_template_name (self, value):
        """
            sets template name along @value;
        """
        # inits
        self.container.get_stringvar("template_name")\
            .set(self.clean_name(value))
    # end def


    def slot_on_listbox_click (self, event=None, *args, **kw):
        """
            event handler: mouse click on listbox;
        """
        # inits
        _fpath = self.get_listbox_fpath()
        # new selection?
        if _fpath != self.current_fpath:
            # update preview
            self.update_preview(_fpath)
        # end if
    # end def


    def slot_on_text_keypress (self, event=None, *args, **kw):
        """
            event handler: keyboard keypress for text preview;
        """
        # schedule auto-save for later
        self.async.run_after(5000, self.auto_save)
    # end def


    def slot_template_browse (self, *args, **kw):
        """
            event handler;
        """
        # get dirpath
        _dpath = FD.askdirectory(
            title=_("Please, select a directory"),
            initialdir=self.current_dir,
            mustexist=True,
            parent=self,
        )
        # got a path?
        if _dpath:
            # update current directory
            self.update_current_dir(_dpath)
        # end if
    # end def


    def slot_template_delete (self, *args, **kw):
        """
            event handler;
        """
        # get selected filepath
        _fpath = self.get_listbox_fpath()
        # got file to delete?
        if _fpath and self.user_confirm():
            # update preview to 'no more file'
            self.update_preview("")
            # remove file
            os.remove(_fpath)
            # update file list
            self.update_listbox()
        # end if
    # end def


    def slot_template_new (self, *args, **kw):
        """
            event handler;
        """
        # get filepath
        _fpath = FD.asksaveasfilename(
            title=_("New template"),
            defaultextension=self.FILE_EXT,
            filetypes=self.FILE_TYPES,
            initialdir=self.current_dir,
            confirmoverwrite=True,
            parent=self,
        )
        # got a path?
        if _fpath:
            # create new file
            open(_fpath, "w").close()
            # CAUTION:
            # directory may have changed /!\
            self.update_current_dir(OP.dirname(_fpath))
            # update preview only after dir updates
            self.update_preview(_fpath)
            # new template: go directly to edit mode
            self.container.text_template_preview.focus_set()
        # end if
    # end def


    def slot_template_reset_dir (self, *args, **kw):
        """
            event handler;
        """
        # got a difference?
        if self.current_dir != self.DEFAULT_DIR:
            # reset to default dir
            self.update_current_dir(self.DEFAULT_DIR)
        # end if
    # end def


    def update_current_dir (self, new_dir):
        """
            updates current working directory, listbox and so on;
        """
        # reset preview first
        self.update_preview("")
        # inits
        self.current_dir = new_dir
        # update listbox along directory path
        self.update_listbox(new_dir)
    # end def


    def update_listbox (self, *args, new_dir=None, **kw):
        """
            event handler;
            updates listbox along @new_dir if given, with
            self.current_dir otherwise;
        """
        # inits
        new_dir = P.normalize(new_dir) or self.current_dir
        # param controls
        if OP.isdir(new_dir):
            # init listbox
            _lb = self.container.listbox_templates_list
            # clear listbox
            _lb.delete(0, "end")
            # file list
            _flist = sorted(
                map(
                    self.clean_name,
                    glob.glob(OP.join(new_dir, self.FILE_PATTERN))
                )
            )
            # feed listbox
            _lb.insert("end", *_flist)
            # empty list?
            if not _flist:
                # clear and lock preview text
                self.clear_preview(lock=True)
            # end if
            # disable delete button
            self.enable_widget(self.container.btn_delete, False)
        # end if
    # end def


    def update_preview (self, fpath):
        """
            update template preview along @fpath filepath;
        """
        # force task right now
        self.save_now()
        # inits
        fpath = P.normalize(fpath)
        self.current_fpath = ""
        # clear preview frame widgets
        self.clear_preview(lock=True)
        # disable delete button
        self.enable_widget(self.container.btn_delete, False)
        # params controls
        if OP.isfile(fpath):
            # keep track
            self.current_fpath = fpath
            # set info
            self.set_template_name(fpath)
            # inits
            _text = self.container.text_template_preview
            # enable preview text
            self.enable_widget(_text, True)
            # get file contents
            with open(fpath, "r") as _file:
                # get text
                _data = _file.read().rstrip()
                if _data: _data += "\n"
                # insert text
                _text.insert("1.0", _data)
            # end with
            # enable delete button
            self.enable_widget(self.container.btn_delete, True)
        # end if
    # end def


    def user_confirm (self):
        """
            user confirmation dialog;
        """
        return MB.askyesno(
            title=_("Question"),
            message=_("Are you sure?"),
            parent=self,
        )
    # end def


    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;
            this is a hook called by '_slot_button_ok()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # put here your own code in subclass
        # succeeded
        return True
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class PitchTemplatesDialog