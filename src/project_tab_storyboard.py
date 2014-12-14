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
import tkRAD


class ProjectTabStoryboard (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
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
        # end for
    # end def


    def clear_text (self, *widgets):
        """
            clears contents for text widget(s);
        """
        # browse widgets
        for _w in widgets:
            # clear widget
            self.text_clear_contents(_w)
        # end for
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


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # inits
        fcontents = ""                                                      # FIXME
        #~ fcontents = self.text_get_contents(self.text_storyboard)
        # always return a dict
        return {fname: fcontents}
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
        # looks for ^/xml/widget/tab_storyboard.xml
        self.xml_build("tab_storyboard")
        # widget inits
        self.LBOX_SCENE = self.listbox_scene_browser
        self.LBOX_SHOT = self.listbox_shot_browser
        self.BTN_ADD = self.btn_add_shot
        self.BTN_DEL = self.btn_del_shot
        self.BTN_RENAME = self.btn_rename_shot
        self.TEXT_SCENE = self.text_scene_preview
        self.TEXT_SHOT = self.text_shot_editor
        self.ENT_SHOT = self.entry_shot_title
        self.LBL_SHOT = self.get_stringvar("lbl_shot_number")
        # update buttons state
        self.slot_update_buttons()
        # event bindings
        self.bind_events(**kw)
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # set text widget contents
        #~ self.text_set_contents(self.text_storyboard, fname)
        pass
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # reset status
        #~ self.text_storyboard.edit_modified(flag)
        pass
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        print("slot_tab_reset")
        # reset listboxes
        self.clear_listbox(self.LBOX_SCENE, self.LBOX_SHOT)
        # reset Text widgets
        self.clear_text(self.TEXT_SCENE, self.TEXT_SHOT)
        # reset entry + labels
        self.clear_entry(self.ENT_SHOT)
        self.LBL_SHOT.set("")
        # update buttons state
        self.slot_update_buttons()
    # end def


    def slot_update_buttons (self, *args, **kw):
        """
            event handler: updates buttons state;
        """
        # inits
        self.enable_widget(self.BTN_ADD, self.LBOX_SCENE.curselection())
        self.enable_widget(self.BTN_DEL, self.LBOX_SHOT.size())
        self.enable_widget(self.BTN_RENAME, self.LBOX_SHOT.curselection())
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class ProjectTabStoryboard
