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
import tkinter.constants as TK
import tkinter.filedialog as FD
import tkinter.messagebox as MB
import tkRAD.core.path as P
import tkRAD.core.async as ASYNC
import tkRAD.widgets.rad_dialog as DLG


class PitchTemplatesDialog (DLG.RADButtonsDialog):
    """
        Pitch templates management dialog;
    """

    # class constant defs
    BUTTONS = ("OK", "Cancel")
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
        print("auto_save")
        # got something to save?
        if OP.isfile(self.current_fpath) and self.TEXT.edit_modified():
            # try out
            try:
                # save file
                with open(self.current_fpath, "w", encoding=ENCODING) \
                                                               as _file:
                    # write text contents
                    _file.write(self.get_preview_text().rstrip())
                # end with
                # reset modified
                self.TEXT.edit_modified(False)
            # file access denied
            except Exception as e:
                # notify user
                MB.showerror(
                    title=_("Attention"),
                    message=_(
                        "An error has occurred:\n"
                        "[{ecn}] {err}\n"
                        "Could *NOT* save text contents."
                    ).format(ecn=e.__class__.__name__, err=e),
                    parent=self,
                )
            # end try
        else:
            print("nothing to save.")
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
        self.LISTBOX.bind(
            "<<ListboxSelect>>", self.slot_listbox_item_selected
        )
        self.TEXT.bind(
            "<Control-a>", self.slot_edit_select_all
        )
        self.TEXT.bind(
            "<KeyRelease>", self.slot_on_text_keypress
        )
    # end def


    def cancel_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog cancellation method;
            this is a hook called by '_slot_button_cancel()';
            this *MUST* be overridden in subclass;
            returns True on success, False otherwise;
        """
        # put here your own code in subclass
        self.save_now()
        # succeeded
        return True
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
        _text = self.TEXT
        # backup state
        _flag = self.widget_enabled(_text) and not lock
        # enable
        self.enable_widget(_text, True)
        # clear
        _text.delete("1.0", TK.END)
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
            self.LBL_CUR_DIR.set(P.shorten_path(value, limit=70))
        else:
            raise NotADirectoryError("not a directory.")
        # end if
    # end def

    @current_dir.deleter
    def current_dir (self):
        del self.__current_dir
    # end def


    def get_chk_option (self, cvarname):
        """
            returns True if checkbox linked to @cvarname is checked,
            False otherwise;
        """
        return bool(self.container.get_stringvar(cvarname).get() == "1")
    # end def


    def get_listbox_fpath (self):
        """
            retrieves filepath from current listbox selection;
        """
        # inits
        _lb = self.LISTBOX
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


    def get_preview_text (self):
        """
            returns all preview Text widget contents;
        """
        return self.TEXT.get("1.0", TK.END)
    # end def


    def get_template_name (self):
        """
            retrieves template name;
        """
        return self.LBL_TPL_NAME.get()
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
        # widget inits
        _w = self.container
        self.LISTBOX = _w.listbox_templates_list
        self.TEXT = _w.text_template_preview
        self.LBL_TPL_NAME = _w.get_stringvar("template_name")
        self.LBL_CUR_DIR = _w.get_stringvar("current_dir")
        self.BTN_DELETE = _w.btn_delete
        # configure selection tag
        self.TEXT.tag_configure(
            TK.SEL, background="grey30", foreground="white"
        )
        # member inits
        self.DEFAULT_DIR = P.normalize(_(self.DEFAULT_DIR))
        self.async = ASYNC.get_async_manager()
        self.current_fpath = ""
        self.update_current_dir(
            self.options.get(
                "dirs",
                "pitch_templates_dir",
                fallback=self.DEFAULT_DIR
            )
        )
        # event bindings
        self.bind_events(**kw)
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
        self.LBL_TPL_NAME.set(self.clean_name(value))
    # end def


    def slot_edit_select_all (self, event=None, *args, **kw):
        """
            event handler: <Ctrl+A> select all in Text widget;
        """
        # select all
        try:
            # select all text
            event.widget.tag_add(TK.SEL, "1.0", TK.END)
            # this disables tkinter chain of internal bindings
            # thanks to Brian Oakley's cool explanation
            return "break"
        except:
            pass
        # end try
    # end def


    def slot_listbox_item_selected (self, event=None, *args, **kw):
        """
            event handler: item selected in listbox;
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
        # try out
        try:
            # undo/redo stack
            if event.keysym == "space":
                event.widget.edit_separator()
            # end if
        except:
            pass
        # end try
        # schedule auto-save for later
        self.async.run_after(3000, self.auto_save)
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
            self.TEXT.focus_set()
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
        try:
            self.current_dir = new_dir
        except:
            self.current_dir = "~"
        # end try
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
            _lb = self.LISTBOX
            # clear listbox
            _lb.delete(0, TK.END)
            # file list
            _flist = sorted(
                map(
                    self.clean_name,
                    glob.glob(OP.join(new_dir, self.FILE_PATTERN))
                )
            )
            # feed listbox
            _lb.insert(TK.END, *_flist)
            # empty list?
            if not _flist:
                # clear and lock preview text
                self.clear_preview(lock=True)
            # end if
            # disable delete button
            self.enable_widget(self.BTN_DELETE, False)
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
        self.enable_widget(self.BTN_DELETE, False)
        # params controls
        if OP.isfile(fpath):
            # keep track
            self.current_fpath = fpath
            # set info
            self.set_template_name(fpath)
            # inits
            _text = self.TEXT
            # enable preview text
            self.enable_widget(_text, True)
            # try out (file access)
            try:
                # get file contents
                with open(fpath, "r", encoding=ENCODING) as _file:
                    # get text
                    _data = _file.read().rstrip()
                    if _data: _data += "\n"
                    # insert text
                    _text.insert("1.0", _data)
                # end with
            # access denied
            except Exception as e:
                # notify user
                MB.showerror(
                    title=_("Attention"),
                    message=_(
                        "An error has occurred:\n"
                        "[{ecn}] {err}\n"
                        "Could *NOT* load text contents."
                    ).format(ecn=e.__class__.__name__, err=e),
                    parent=self,
                )
            # keep on trying
            else:
                # reset undo/redo stack
                _text.edit_reset()
                # reset modified
                _text.edit_modified(False)
            # end try
            # enable delete button
            self.enable_widget(self.BTN_DELETE, True)
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
        if OP.isfile(self.current_fpath):
            # force task right now
            self.save_now()
            # inits
            _pitch = _notes = ""
            _text = self.get_preview_text()
            _chk_pitch = self.get_chk_option("chk_copy_to_pitch")
            _chk_notes = self.get_chk_option("chk_copy_to_notes")
            # set copy along user option
            if _chk_pitch:
                _pitch = _text
            # end if
            # set copy along user option
            if _chk_notes:
                _notes = _text
            # end if
            # got something to send?
            if _pitch or _notes:
                # notify application
                self.events.raise_event(
                    "Pitch:Template:Insert", pitch=_pitch, notes=_notes
                )
                # succeeded
                return True
            # end if
        # end if
        # failed
        return False
    # end def

# end class PitchTemplatesDialog
