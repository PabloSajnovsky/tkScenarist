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
from tkinter import font
from tkinter import colorchooser
import tkRAD.widgets.rad_dialog as DLG


class ScenarioElementsEditorDialog (DLG.RADButtonsDialog):
    """
        Scenario Elements Editor dialog;
    """

    # class constant defs
    BUTTONS = ("OK", "Cancel")


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Color:Choose": self.slot_choose_color,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
        self.NOTEBOOK.bind(
            "<<NotebookTabChanged>>", self.slot_tab_changed
        )
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


    def get_current_tab_index (self):
        """
            retrieves notebook's current selected tab numeric index;
        """
        return self.NOTEBOOK.index("current")
    # end def


    def get_element_names (self, elt_dict):
        """
            retrieves dictionary of (label: tag) key/value pairs;
        """
        # inits
        return dict(
            zip(
                [elt["label"] for elt in elt_dict.values()],
                elt_dict.keys()
            )
        )
    # end def


    def init_widget (self, **kw):
        r"""
            widget main inits;
        """
        # super class inits
        super().init_widget(
            # looks for ^/xml/widget/dlg_scenario_elements_editor.xml
            xml="dlg_scenario_elements_editor",
        )
        # inits
        self.default_settings = kw.get("default_settings")
        self.default_element = kw.get("default_element")
        self.element_names = self.get_element_names(self.default_settings)
        _names = sorted(self.element_names)
        _readonly = ['readonly']
        self.w = self.container
        # NOTEBOOK section
        self.NOTEBOOK = self.w.notebook_see_prefs
        # ELEMENT CHAINING section
        self.w.combo_current_element.configure(
            values=_names, state=_readonly
        )
        self.w.combo_current_element.current(0)
        # update element names for choice selection
        _names.insert(0, "")
        for _key in ("tab", "return", "ctrl_return"):
            for _t in ("switch", "create"):
                _w = getattr(self.w, "combo_{}_{}".format(_key, _t))
                _w.configure(values=_names, state=_readonly)
                _w.current(0)
            # end for
        # end for
        # FONT section
        self.w.combo_font_family.configure(
            values=['monospace', 'sans', 'serif', 'tkdefaultfont'] +
            sorted(font.families())
        )
        self.w.combo_font_family.current(0)
        self.w.combo_font_size.current(4)
        self.w.combo_font_style.state(_readonly)
        self.w.combo_font_style.current(0)
        # MARGIN section
        self.w.combo_lmargin_units.state(_readonly)
        self.w.combo_lmargin_units.current(0)
        self.w.combo_rmargin_units.state(_readonly)
        self.w.combo_rmargin_units.current(0)
        # PREVIEW section
        _text = self.w.text_preview
        _text.delete("1.0", "end")
        _text.insert(
            "end",
            *(
                _("ext - day - this is a 'SCENE' line\n"), "scene",
                _("This is an 'ACTION' line.\n"), "action",
                _("'CHARACTER' name\n"), "character",
                _("this is a 'PARENTHETICAL' line.\n"), "parenthetical",
                _("This is a 'DIALOGUE' line.\n"), "dialogue",
                _("'CHARACTER' name\n"), "character",
                _("This is a 'DIALOGUE' line.\n"), "dialogue",
                _("This is an 'ACTION' line.\n"), "action",
                _("Transition e.g. cut, fade in, fade out\n"), "transition",
                _("ext - day - this is a 'SCENE' line\n"), "scene",
                _("Transition e.g. cut, fade in, fade out\n"), "transition",
                _("This is an 'ACTION' line.\n"), "action",
            )
        )
        _text.configure(
            width=1, height=5, wrap="word", state="disabled"
        )
        # event bindings
        self.bind_events(**kw)
        # reset to 'global settings' tab
        self.NOTEBOOK.select(0)
    # end def


    def slot_choose_color (self, *args, widget=None, **kw):
        """
            event handler: opens tkinter.colorchooser dialog and asks
            user to choose a color;
        """
        # param controls
        if widget:
            # inits
            _bg = widget.cget("background")
            # ask color
            _color = colorchooser.askcolor(
                color=_bg,
                title=_("Please, choose a color"),
                parent=self,
            )[-1] or _bg
            # reset widget's background color
            widget.configure(background=_color, text=_color.upper())
        # end if
    # end def


    def slot_tab_changed (self, event=None, *args, **kw):
        """
            event handler: a notebook tab has been selected;
        """
        print("slot_tab_changed")
        # FIXME
        # what about data loss between tabs ?
        # should manage two mappings?
        # which tab is it?
        _index = self.get_current_tab_index()
        # GLOBAL settings
        if not _index:
            print("global settings")
        # PROJECT settings
        else:
            print("project settings")
        # end def
        # update all data
        self.update_data()
    # end def


    def update_data (self, *args, **kw):
        """
            updates all data in form;
        """
        print("update_data")
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
        # get current tab numeric index
        _tab = self.get_current_tab_index()
        # TODO
        """
            if tab is 'global': ask if should apply to current project?
        """
        # failed
        return False
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class ScenarioElementsEditorDialog
