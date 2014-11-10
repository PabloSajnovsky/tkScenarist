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
import os.path as OP
import tkinter.filedialog as FD
import tkRAD.core.path as P
import tkRAD.widgets.rad_dialog as DLG


class PitchTemplatesDialog (DLG.RADButtonsDialog):
    """
        Pitch templates management dialog;
    """

    # class constant defs
    DEFAULT_DIR = "^/data/templates/pitch/"

    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Template:Browse": self.slot_template_browse,
                "Dialog:Template:Delete": self.slot_template_delete,
                "Dialog:Template:Modify": self.slot_template_modify,
                "Dialog:Template:New": self.slot_template_new,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
        self.container.text_template_preview.bind(
            "<KeyRelease>", self.slot_on_text_keypress
        )
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
        self.__current_dir = P.normalize(value)
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
                state={True: 'normal'}.get(bool(state), 'disabled')
            )
        # end if
    # end def


    def get_template_name (self):
        """
            retrieves template name;
        """
        return self.container.get_stringvar("template_name").get().strip()
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
        self.current_dir = self.options.get(
            "dirs", "pitch_templates_dir", fallback=_(self.DEFAULT_DIR)
        )
        # event bindings
        self.bind_events()
    # end def


    def set_template_name (self, value):
        """
            sets template name along @value;
        """
        self.container.get_stringvar("template_name").set(str(value).strip())
    # end def


    def slot_on_entry_keypress (self, event=None, *args, **kw):
        """
            event hanlder: keyboard keypress for text preview;
        """
        print("entry_template_name: key pressed")
        # inits
        self.enable_widget(
            self.container.btn_create, bool(self.entry_get_text())
        )
    # end def


    def slot_on_text_keypress (self, event=None, *args, **kw):
        """
            event hanlder: keyboard keypress for text preview;
        """
        print("text_template_preview: key pressed")
    # end def


    def slot_template_browse (self, *args, **kw):
        """
            event handler;
        """
        print("template browse")
    # end def


    def slot_template_delete (self, *args, **kw):
        """
            event handler;
        """
        print("template delete")
    # end def


    def slot_template_modify (self, *args, **kw):
        """
            event handler;
        """
        print("template modify")
    # end def


    def slot_template_new (self, *args, **kw):
        """
            event handler;
        """
        # init widgets
        self.enable_widget(self.container.text_template_preview, False)
        # get filepath
        _fpath = FD.asksaveasfilename(
            title=_("New template"),
            defaultextension=".txt",
            filetypes=[(_("Text files"), "*.txt")],
            initialdir=self.current_dir,
            confirmoverwrite=True,
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

# end class PitchTemplatesDialog
