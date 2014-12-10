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
        #~ self.events.connect_dict(
            #~ {
                #~ "Dialog:": self.slot_
            #~ }
        #~ )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
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
        self.w = self.container
        self.default_settings = kw.get("default_settings")
        self.default_element = kw.get("default_element")
        self.element_names = self.get_element_names(self.default_settings)
        _names = sorted(self.element_names)
        _readonly = ['readonly']
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
        self.w.combo_font_style.state(_readonly)
        # event bindings
        self.bind_events(**kw)
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
