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
import copy
from tkinter import font
from tkinter import colorchooser
import tkRAD.widgets.rad_dialog as DLG
import tkRAD.core.async as ASYNC


class ScenarioElementsEditorDialog (DLG.RADButtonsDialog):
    """
        Scenario Elements Editor dialog;
    """

    # class constant defs
    BUTTONS = ("OK", "Reset to defaults", "Cancel")


    def _slot_button_resettodefaults (self, event=None, *args, **kw):
        """
            event handler: dialog button 'Reset to defaults';
        """
        # which tab is it?
        _index = self.get_current_tab_index()
        # reset to defaults for selected tab
        self.settings[_index] = {
            "element": copy.deepcopy(self.w_text.ELEMENT_DEFAULTS),
            "current_selected": 0,
        }
        # update form data
        self.slot_tab_changed()
    # end def


    def bind_events (self, **kw):
        """
            event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Dialog:Color:Choose": self.slot_choose_color,
                "Dialog:Text:Align": self.slot_store_looknfeel,
            }
        )
        # tkinter widget event bindings
        self.bind("<Escape>", self._slot_button_cancel)
        # NOTEBOOK section
        self.NOTEBOOK.bind(
            "<<NotebookTabChanged>>", self.slot_tab_changed
        )
        # CURRENT SELECTED section
        self.w.combo_current_element.bind(
            "<<ComboboxSelected>>", self.slot_current_element_changed
        )
        # CHAININGS section
        for _w in self.CHAINING_COMBOS:
            _w.bind("<<ComboboxSelected>>", self.slot_store_chainings)
        # end for
        # LOOK'N'FEEL section
        for _w in self.FONT_COMBOS + self.MARGIN_COMBOS:
            _w.bind(
                "<<ComboboxSelected>>", self.slot_store_looknfeel
            )
        # end for
        # PREVIEW section
        self.w.text_preview.bind(
            "<ButtonRelease-1>", self.slot_preview_clicked
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


    def get_chaining_combos (self):
        """
            retrieves list of create/switch element chaining combos;
        """
        # inits
        _list = []
        for _name in self.get_chaining_names():
            _list.append(
                getattr(self.w, "combo_{}".format(_name))
            )
        # end for
        return _list
    # end def


    def get_chaining_names (self):
        """
            retrieves list of create/switch element chaining names;
        """
        # inits
        _list = []
        for _key in ("tab", "return", "ctrl_return"):
            for _t in ("switch", "create"):
                _list.append("{}_{}".format(_key, _t))
            # end for
        # end for
        return _list
    # end def


    def get_current_element (self):
        """
            retrieves dict() of current selected element settings;
        """
        return self.current_settings["element"]\
                                    [self.get_current_element_tag()]
    # end def


    def get_current_element_tag (self):
        """
            retrieves tag name of current selected element;
        """
        return self.element_names[self.w.combo_current_element.get()]
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


    def get_font_attrs (self, str_font):
        """
            retrieves font attributes from a formatted @str_font font
            string; returns tuple (family, size, style);
        """
        # inits
        _font = font.Font(font=str_font or "monospace 12")
        _family = _font.cget("family")
        _size = _font.cget("size")
        _weight = _font.cget("weight").replace("normal", "")
        _slant = _font.cget("slant").replace("roman", "")
        _style = "{} {}".format(_weight, _slant).strip()
        _style = _style or "normal"
        # return results
        return (_family, _size, _style)
    # end def


    def get_formatted_margin (self, cvar_entry, combo):
        """
            retrieves a tkinter-formatted margin dimension string;
        """
        # inits
        _value = int(self.w.get_stringvar(cvar_entry).get() or 0)
        # tkinter dimension units compliance
        _units = combo.get()[0] if combo.current() else ""
        # return formatted string
        return "{}{}".format(_value, _units).strip().lower()
    # end def


    def get_label (self, element_tag):
        """
            retrieves label for given @element_tag;
        """
        # inits
        _e = self.current_settings["element"].get(element_tag) or dict()
        return _e.get("label") or ""
    # end def


    def get_rc_section (self):
        """
            retrieves RC file section name for this class;
        """
        return self.classname().lower()
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
        self.async = ASYNC.get_async_manager()
        self.w_text = kw.get("w_text")
        self.settings = [
            # global settings
            {
                "element":
                    copy.deepcopy(self.w_text.get_options_element()),
                "current_selected": 0,
            },
            # project settings
            {
                "element": copy.deepcopy(self.w_text.ELEMENT),
                "current_selected": 0,
            },
        ]
        self.current_settings = self.settings[0]
        self.element_names = self.get_element_names(
            self.current_settings["element"]
        )
        _names = sorted(self.element_names)
        _readonly = ["readonly"]
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
        # set choice names to all switch/create combos
        self.CHAINING_NAMES = self.get_chaining_names()
        self.CHAINING_COMBOS = self.get_chaining_combos()
        self.CHAININGS = tuple(
            zip(self.CHAINING_COMBOS, self.CHAINING_NAMES)
        )
        for _w in self.CHAINING_COMBOS:
            _w.configure(values=_names, state=_readonly)
            _w.current(0)
        # end for
        # FONT section
        self.w.combo_font_family.configure(
            values=['monospace', 'sans', 'serif', 'tkdefaultfont'] +
            sorted(font.families())
        )
        self.FONT_COMBOS = (
            self.w.combo_font_family,
            self.w.combo_font_size,
            self.w.combo_font_style
        )
        # MARGIN section
        _filter = self.register(self.key_filter_digits)
        self.w.entry_lmargin.configure(
            validate="key", validatecommand=(_filter, "%S")
        )
        self.w.entry_rmargin.configure(
            validate="key", validatecommand=(_filter, "%S")
        )
        self.MARGIN_COMBOS = (
            self.w.combo_lmargin_units, self.w.combo_rmargin_units
        )
        # init all combos at once
        for _w in self.FONT_COMBOS + self.MARGIN_COMBOS:
            _w.state(_readonly)
            _w.current(0)
        # end if
        # PREVIEW section
        self.w.text_preview.configure(
            # use only the following attrs from w_text
            font=self.w_text.cget("font"),
            background=self.w_text.cget("background"),
            foreground=self.w_text.cget("foreground"),
            width=1, height=10, wrap="word",
        )
        # event bindings
        self.bind_events(**kw)
        # reset tab along with user option
        self.NOTEBOOK.select(
            self.options.get(
                self.get_rc_section(), "startup_tab_index", fallback=1
            )
        )
    # end def


    def key_filter_digits (self, input_char):
        """
            returns True if @input_char is a digit, False otherwise;
        """
        # defer task
        self.async.run_after(200, self.slot_store_looknfeel)
        return bool(input_char in "0123456789")
    # end def


    def reformat_line (self, contents, tag):
        """
            reformats text line @contents along with @tag constraints;
            returns tuple (contents, tag);
        """
        # inits
        _text, _adjust = self.w_text.switch_to_method(
            "reformat_line_{}".format(tag), contents
        )
        # return results
        return (_text + "\n", tag)
    # end def


    def reset_margin (self, cvar_entry, combo, value=None):
        """
            resets entry value + units combo value along with given
            @value parameter value;
        """
        # param controls
        if value is None:
            # reset value
            value = self.get_formatted_margin(cvar_entry, combo)
        # end if
        # inits
        value = str(value or 0).strip()
        _units = "px"
        # search for units in value
        _match = re.search(r"(\d+)\s*(\w*)", value)
        # got matchup?
        if _match:
            # inits
            value = _match.group(1)
            _unit = _match.group(2)
            # got units?
            if _unit:
                # tkinter standard dimension parsing
                _units = {
                    "c": "cm", "i": "in", "m": "mm", "p": "pt",
                }.get(_unit[0]) or "px"
            # end if
        # end if
        # reset widgets
        self.w.get_stringvar(cvar_entry).set(value)
        combo.set(_units)
    # end def


    def set_color_label (self, *widgets):
        """
            resets text option along with widget's background color;
        """
        # browse widgets
        for _w in widgets:
            # init standard color
            _color = "#{:02X}{:02X}{:02X}".format(
                *map(
                    lambda x: x//256,
                    _w.winfo_rgb(_w.cget("background"))
                )
            )
            # reset text label
            _w.configure(text=_color)
        # end for
    # end def


    def set_preview_contents (self, *args, **kw):
        """
            sets preview text widget contents;
        """
        # inits
        _text = self.w.text_preview
        # enable text preview
        self.enable_widget(_text, True)
        # reset contents
        _text.delete("1.0", "end")
        _action = self.reformat_line(
            _("This is an 'ACTION' line."), "action"
        )
        _character = self.reformat_line(
            _("'CHARACTER' name"), "character"
        )
        _dialogue = self.reformat_line(
            _("This is a 'DIALOGUE' line."), "dialogue"
        )
        _parenthetical = self.reformat_line(
            _("this is a 'PARENTHETICAL' line"), "parenthetical"
        )
        _scene = self.reformat_line(
            _("ext - day - this is a 'SCENE' line"), "scene"
        )
        _transition = self.reformat_line(
            _("'TRANSITION' line."), "transition"
        )
        _text.insert(
            "1.0",
            *(
                _scene + _action + _character + _parenthetical +
                _dialogue + _character + _dialogue + _action +
                _transition + _scene + _transition + _action
            )
        )
        # disable text preview
        self.enable_widget(_text, False)
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
            widget.configure(background=_color)
            # reset widget's text label
            self.set_color_label(widget)
            # store new data in look'n'feel settings
            self.slot_store_looknfeel()
        # end if
    # end def


    def slot_current_element_changed (self, event=None, *args, **kw):
        """
            event handler: new element selected in combobox;
        """
        # update pointer
        self.current_settings["current_selected"] = (
            self.w.combo_current_element.current()
        )
        # update linked combos + look'n'feel
        self.slot_update_linked_items()
    # end def


    def slot_preview_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse click on preview text widget;
        """
        # inits
        _tags = self.w.text_preview.tag_names("current")
        # got tags?
        if _tags:
            # inits
            _label = self.get_label(_tags[0])
            # label does exist?
            if _label in self.element_names:
                # update current selected element
                self.w.combo_current_element.set(_label)
                # update linked combos + look'n'feel
                self.slot_current_element_changed()
            # end if
        # end if
    # end def


    def slot_store_chainings (self, event=None, *args, **kw):
        """
            event handler: stores create/switch combo data in settings;
        """
        # inits
        _element = self.get_current_element()
        # browse items
        for _widget, _name in self.CHAININGS:
            # reset settings
            _element["on_{}".format(_name)] = (
                self.element_names.get(_widget.get()) or ""
            )
        # end for
    # end def


    def slot_store_looknfeel (self, event=None, *args, **kw):
        """
            event handler: stores look'n'feel data in settings;
        """
        # inits
        _element = self.get_current_element()
        _config = _element.setdefault("config", dict())
        # COLOR config
        _config["background"] = self.w.btn_choose_bg.cget("background")
        _config["foreground"] = self.w.btn_choose_fg.cget("background")
        # FONT config
        _config["font"] = (
            "{{{family}}} {size} {style}"
            .format(
                family=self.w.combo_font_family.get(),
                size=self.w.combo_font_size.get(),
                style=self.w.combo_font_style.get(),
            ).strip().lower()
        )
        # ALIGN config
        _config["justify"] = (
            self.w.get_stringvar("options_text_align").get()
        )
        # MARGIN config
        self.reset_margin(
            "entry_margin_left", self.w.combo_lmargin_units
        )
        _config["lmargin1"] = _config["lmargin2"] = (
            self.get_formatted_margin(
                "entry_margin_left", self.w.combo_lmargin_units
            )
        )
        self.reset_margin(
            "entry_margin_right", self.w.combo_rmargin_units
        )
        _config["rmargin"] = (
            self.get_formatted_margin(
                "entry_margin_right", self.w.combo_rmargin_units
            )
        )
        # update preview text widget
        self.slot_update_preview()
    # end def


    def slot_tab_changed (self, event=None, *args, **kw):
        """
            event handler: a notebook tab has been selected;
        """
        # which tab is it?
        _index = self.get_current_tab_index()
        # change current settings
        self.current_settings = self.settings[_index]
        # update current selected element
        self.slot_update_current_selected()
    # end def


    def slot_update_current_selected (self, *args, **kw):
        """
            event handler: updates all data in form;
        """
        # update current element
        self.w.combo_current_element.current(
            self.current_settings["current_selected"]
        )
        # update chaining combos + look'n'feel
        self.slot_update_linked_items()
    # end def


    def slot_update_linked_items (self, *args, **kw):
        """
            event handler: updates all linked items along current
            selected element;
        """
        # inits
        _element = self.get_current_element()
        # reset combos
        for _widget, _name in self.CHAININGS:
            _widget.set(
                self.get_label(_element.get("on_{}".format(_name)))
            )
        # end for
        # reset look'n'feel
        _config = _element.setdefault("config", dict())
        _face, _size, _style = self.get_font_attrs(_config.get("font"))
        # font attributes
        self.w.combo_font_family.set(_face)
        self.w.combo_font_size.set(_size)
        self.w.combo_font_style.set(_style)
        # background/foreground colors
        _bg = _config.get("background") or "white"
        _fg = _config.get("foreground") or "black"
        self.w.btn_choose_bg.configure(background=_bg)
        self.w.btn_choose_fg.configure(background=_fg)
        self.set_color_label(
            self.w.btn_choose_bg, self.w.btn_choose_fg
        )
        # text alignment
        self.w.get_stringvar("options_text_align").set(
            _config.get("justify") or "left"
        )
        # left margin
        _lmargin = (
            _config.get("lmargin1") or _config.get("lmargin2") or 0
        )
        self.reset_margin(
            "entry_margin_left", self.w.combo_lmargin_units, _lmargin
        )
        # right margin
        _rmargin = _config.get("rmargin") or 0
        self.reset_margin(
            "entry_margin_right", self.w.combo_rmargin_units, _rmargin
        )
        # update preview contents
        self.slot_update_preview()
    # end def


    def slot_update_preview (self, *args, **kw):
        """
            updates preview text widget's look'n'feel;
        """
        # inits
        _text = self.w.text_preview
        # reset preview text tags configuration
        for _tag, _element in self.current_settings["element"].items():
            # get configuration
            _config = _element.get("config")
            # got configuration?
            if _config:
                # reset preview tag configuration
                _text.tag_delete(_tag)
                _text.tag_configure(_tag, **_config)
            # end if
        # end for
        # always raise selection tag upon any other
        _text.tag_raise("sel")
        # update text contents
        self.set_preview_contents()
        # show concerned line
        _text.see(_text.tag_ranges(self.get_current_element_tag())[0])
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
        # inits
        _global, _project = self.settings
        # notify app
        self.events.raise_event(
            "Scenario:Settings:Update",
            settings={
                "global": _global["element"],
                "project": _project["element"],
            }
        )
        # validate
        return True
    # end def


    def widget_enabled (self, widget):
        """
            returns True if tkinter.Widget is enabled, False otherwise;
        """
        return bool(widget.cget("state").lower() == "normal")
    # end def

# end class ScenarioElementsEditorDialog
