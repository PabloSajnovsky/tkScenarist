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
import json
import random
import tkRAD
import tkRAD.core.async as ASYNC
import tkRAD.core.path as P


class ProjectTabScenario (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    # class constant defs
    DEAD_KEYS = (
        "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L",
        "Alt_R", "Caps_Lock",
    )

    DEFAULT_HINT = _(
        "ONE PAGE of script is roughly equal to ONE MINUTE of movie."
    )

    # use i18n support to redefine filepath
    # according to locale language
    INFO_HINTS_FPATH = _("^/data/json/info_hints.en.json")

    # average nb of lines per page (estimation)
    LINES_PER_PAGE = 42


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        # app-wide event bindings
        self.events.connect_dict(
            {
                "Project:Modified": self.slot_project_modified,

                "Scenario:Current:Element:Update":
                    self.slot_update_current_element,
                "Scenario:Elements:Init": self.slot_elements_init,
                "Scenario:Text:Clicked": self.slot_text_clicked,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        self.COMBO.bind(
            "<<ComboboxSelected>>", self.slot_combo_item_selected
        )
        self.LISTBOX.bind(
            "<<ListboxSelect>>", self.slot_listbox_item_selected
        )
        self.POPUP_LBOX.bind("<Key>", self.slot_popup_keypress)
        self.POPUP_LBOX.bind("<KeyRelease>", self.slot_popup_keyrelease)
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # always return a dict
        return self.TEXT.get_file_contents(fname)
    # end def


    def hide_popup_list (self, *args, **kw):
        """
            event handler: hides autocompletion popup list;
        """
        # hide popup list
        self.POPUP.withdraw()
        self.POPUP.start_index = None
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # member inits
        self.mainwindow = self.winfo_toplevel()
        self.mainframe = self.mainwindow.mainframe
        self.tab_characters = self.mainframe.tab_characters
        self.text_clear_contents = self.mainwindow.text_clear_contents
        self.text_get_contents = self.mainwindow.text_get_contents
        self.text_set_contents = self.mainwindow.text_set_contents
        self.async = ASYNC.get_async_manager()
        # looks for ^/xml/widget/tab_scenario.xml
        self.xml_build("tab_scenario")
        # widget inits
        # scenario zone
        self.TEXT = self.text_scenario
        self.COMBO = self.combo_elements
        self.COMBO.state(["readonly"])
        self.COMBO.current_selected = ""
        self.COMBO.elements = dict()
        self.CBO_CUR_ELT = self.get_stringvar("combo_current_element")
        self.LBL_TAB = self.get_stringvar("lbl_on_tab")
        self.LBL_RET = self.get_stringvar("lbl_on_return")
        self.LBL_CTRL_RET = self.get_stringvar("lbl_on_ctrl_return")
        # navigation zone
        self.LISTBOX = self.listbox_scene_browser
        # information zone
        self.LBL_HINT = self.get_stringvar("lbl_info_hint")
        self.LBL_CHAR_NAME = self.get_stringvar("lbl_character_name")
        self.TXT_CHAR_LOG = self.text_characters_log
        self.LBL_PAGE_COUNT = self.get_stringvar("lbl_page_count")
        self.LBL_MOVIE_DURATION = self.get_stringvar("lbl_movie_duration")
        # popup list
        self.POPUP = self.toplevel_popup_list
        self.POPUP.transient(self.TEXT)
        self.POPUP.overrideredirect(True)
        self.POPUP_LBOX = self.listbox_popup_list
        # (re)route events (POPUP_LBOX has priority on TEXT)
        self.route_events(self.POPUP_LBOX, self.TEXT)
        # reset listbox
        self.reset_scene_browser()
        # get hints data
        self.reset_hints()
        # hide popup list
        self.hide_popup_list()
        # event bindings
        self.bind_events(**kw)
    # end def


    def reset_hints (self, fpath=None):
        """
            resets self.INFO_HINTS class member along with @fpath JSON
            file contents;
        """
        # param inits
        fpath = P.normalize(fpath or self.INFO_HINTS_FPATH)
        # get data
        with open(fpath) as _file:
            # reset member
            self.INFO_HINTS = json.load(_file)
        # end with
    # end def


    def reset_scene_browser (self, *args, **kw):
        """
            event handler: resets navigation listbox (scene browser);
        """
        # inits
        self.LISTBOX.current_lines = []
        self.LISTBOX.delete(0, "end")
    # end def


    def route_events (self, tk_master, tk_slave):
        """
            (re)routes event chain so that @tk_master has priority on
            @tk_slave in event handling;
        """
        # inits
        _tags = list(tk_slave.bindtags())
        # route events
        _tags.insert(0, tk_master)
        # reset event chain
        tk_slave.bindtags(tuple(_tags))
    # end def


    def set_combo_text (self, text):
        """
            sets combobox' entry text;
        """
        # param controls
        if text in self.COMBO.elements and \
                                    text != self.COMBO.current_selected:
            # update current selected
            self.update_selected(text)
            # set text
            self.CBO_CUR_ELT.set(text)
        # end if
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
        """
        # set text widget contents
        self.TEXT.file_setup(fname, archive)
    # end def


    def show_popup_list (self, *args, **kw):
        """
            event handler: shows autocompletion popup list;
        """
        # inits
        choices = kw.get("choices")
        start_index = kw.get("start_index") or "insert"
        self.POPUP.start_index = start_index
        # param controls
        if choices:
            _lb = self.POPUP_LBOX
            _lb.delete(0, "end")
            _lb.insert(0, *choices)
            _lb.selection_set(0)
            _lb.configure(
                height=min(7, len(choices)),
                width=min(49, max(map(len, choices))),
            )
        # end if
        # recalc pos
        _x, _y, _w, _h = self.TEXT.bbox(start_index)
        _xi, _yi, _wi, _hi = self.TEXT.bbox("insert")
        _x += self.TEXT.winfo_rootx()
        _y = self.TEXT.winfo_rooty() + _h + max(_y, _yi)
        # reset popup window pos
        self.POPUP.geometry("+{}+{}".format(_x, _y))
        # show popup list
        self.POPUP.deiconify()
    # end def


    def slot_autocomplete (self, *args, **kw):
        """
            event handler: a word has been detected in scenario text
            widget while buffering keystrokes;
        """
        # inits
        _word = self.TEXT.get_word()
        _si = _word["start_index"]
        # look for matching names
        _names = self.tab_characters.get_matching_names(_word["word"])
        # no matching names for word?
        if not _names:
            # try out full line
            _names = self.tab_characters.get_matching_names(
                self.TEXT.get_line_contents()
            )
            _si = "insert linestart"
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


    def slot_combo_item_selected (self, *args, **kw):
        """
            event handler: item has been selected in combobox;
        """
        # inits
        _text = self.CBO_CUR_ELT.get()
        # got something new?
        if _text != self.COMBO.current_selected:
            # update current selected
            self.update_selected(_text)
            # notify app
            self.events.raise_event(
                "Scenario:Switch:Line",
                new_tag=self.COMBO.elements[_text]
            )
            # keep text focused
            self.after_idle(self.TEXT.focus_set)
        # end if
    # end def


    def slot_insert_completion (self, event=None, *args, **kw):
        """
            event handler: inserts popup list completion text;
        """
        print("slot_insert_completion")
        return "break"
    # end def


    def slot_listbox_item_selected (self, *args, **kw):
        """
            event handler: item has been selected in listbox;
        """
        # inits
        _sel = self.LISTBOX.curselection()
        # got selected?
        if _sel:
            # inits
            _index = float(self.LISTBOX.current_lines[_sel[0]])
            # show line in text widget
            self.TEXT.see(_index)
            self.TEXT.move_cursor("{} lineend".format(_index))
            self.after_idle(self.TEXT.focus_set)
        # end if
    # end def


    def slot_elements_init (self, *args, elements=None, **kw):
        """
            event handler: elements have been init'ed;
        """
        # param controls
        if elements:
            # inits
            self.COMBO.current_selected = ""
            self.COMBO.elements = dict()
            # browse elements
            for _element in elements:
                # reset values
                self.COMBO.elements[
                    self.TEXT.get_label(_element)
                    ] = _element
            # end for
            # reset combobox contents
            self.COMBO.configure(values=sorted(self.COMBO.elements))
        # end if
    # end def


    def slot_popup_insert (self, event=None, *args, **kw):
        """
            event handler: tab/return keypress on popup;
        """
        print("slot_popup_insert")
    # end def


    def slot_popup_key_arrows (self, event=None, *args, **kw):
        """
            event handler: up/down keypress on popup;
        """
        print("slot_popup_key_arrows")
    # end def


    def slot_popup_keypress (self, event=None, *args, **kw):
        """
            event handler: any keypress on popup;
        """
        # ensure popup is shown up
        if self.POPUP.state() == "normal":
            # inits
            _key = event.keysym
            # specific keystrokes
            if _key in ("Escape",):
                # hide popup (transferred to slot_popup_keyrelease)
                pass
            # up/down arrow keys
            elif _key in ("Up", "Down"):
                # manage into popup
                self.slot_popup_key_arrows(event, *args, **kw)
            # tab/return keystrokes
            elif _key in ("Tab", "Return"):
                # manage into popup
                self.slot_popup_insert(event, *args, **kw)
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
        if self.POPUP.state() == "normal":
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
        self.TEXT.edit_modified(flag)
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # reset Text widget
        self.TEXT.reset()
        # reset listbox
        self.reset_scene_browser()
        # reset hints
        self.reset_hints()
    # end def


    def slot_text_clicked (self, event=None, *args, **kw):
        """
            event handler: text widget has been clicked;
        """
        # hide popup list
        self.hide_popup_list()
    # end def


    def slot_update_current_element (self, *args, **kw):
        """
            event handler: updates current element info;
        """
        # inits
        _label = lambda n: self.TEXT.get_label(n)
        _map = self.TEXT.get_element_mappings()
        _tag = _map["tag"]
        # reset widgets
        self.set_combo_text(_label(_tag))
        self.LBL_TAB.set(_label(_map["tab"] or _map["tab_switch"]))
        self.LBL_RET.set(_label(_map["return"]))
        self.LBL_CTRL_RET.set(
            _label(_map["ctrl_return"] or _map["ctrl_switch"])
        )
        # update scene browser
        self.async.run_after(300, self.update_scene_browser)
        # update character log
        self.async.run_after(200, self.update_character_log)
        # update hints
        self.async.run_after(700, self.update_hints, _tag)
        # update stats
        self.async.run_after(1000, self.update_stats)
    # end def


    def update_character_log (self, *args, **kw):
        """
            event handler: updates character's log info, if any;
        """
        # inits
        _tc = self.tab_characters
        _name = _tc.find_nearest_name(
            self.TEXT.get_line_contents(),
            self.TEXT.get_column_index()
        )
        # enable widget
        self.TXT_CHAR_LOG.configure(state="normal")
        # known character name?
        if _tc.is_registered(_name):
            # update info
            self.LBL_CHAR_NAME.set(_name)
            self.text_set_contents(
                self.TXT_CHAR_LOG,
                _tc.get_character_log(_name)
            )
            # no need to autocomplete
            self.hide_popup_list()
        # unknown
        else:
            # clear info
            self.LBL_CHAR_NAME.set("")
            self.text_clear_contents(self.TXT_CHAR_LOG)
            # look out for autocompletion
            self.after_idle(self.slot_autocomplete)
        # end if
        # disable widget
        self.TXT_CHAR_LOG.configure(state="disabled")
    # end def


    def update_hints (self, element_tag):
        """
            shows off hints text according to @element_tag value;
            displays default hints otherwise;
        """
        # inits
        _hints = (
            self.INFO_HINTS.get(element_tag)
            or self.INFO_HINTS.get("default")
            or [self.DEFAULT_HINT]
        )
        # ensure to show default hint sometimes
        if random.randint(1, 10) == 7:
            # force default
            _hints = [self.DEFAULT_HINT]
        # end if
        # update hints text
        self.LBL_HINT.set(str(random.choice(_hints)))
    # end def


    def update_scene_browser (self):
        """
            updates navigation listbox (scene browser);
        """
        # inits
        _dict = self.TEXT.get_lines("scene")
        _cursor = _dict["current"]
        _lines = self.LISTBOX.current_lines = _dict["lines"]
        # reset listbox
        self.LISTBOX.delete(0, "end")
        self.LISTBOX.insert(0, *_dict["texts"])
        # insertion cursor is on a scene line?
        if _cursor in _lines and \
                            not self.TEXT.line_selected(float(_cursor)):
            # inits
            _index = _lines.index(_cursor)
            # select item
            self.LISTBOX.selection_set(_index)
            # show item
            self.LISTBOX.see(_index)
        # end if
    # end def


    def update_selected (self, text):
        """
            updates current selected value;
        """
        # reset current selected
        self.COMBO.current_selected = text
        # reset selection
        self.COMBO.selection_clear()
    # end def


    def update_stats (self, *args, **kw):
        """
            event handler: updates scenario stats;
        """
        # inits
        _lpp = self.LINES_PER_PAGE
        _lines = self.TEXT.get_nb_of_lines()
        _nb_pages = _lines // _lpp + 1
        _cur_page = self.TEXT.get_line_number() // _lpp + 1
        _mduration = int(0.9 * (_lines / _lpp + 1))
        # show info
        self.LBL_PAGE_COUNT.set(
            _("{page} of {total}")
            .format(page=_cur_page, total=_nb_pages)
        )
        # time format
        if _mduration < 1:
            _time_fmt = _("< 1 minute")
        else:
            _time_fmt = _(
                "{hours:02d} h {minutes:02d} min"
            ).format(
                hours=(_mduration // 60),
                minutes=(_mduration % 60)
            )
        # end if
        self.LBL_MOVIE_DURATION.set(_time_fmt)
        # notify app
        self.events.raise_event(
            "Scenario:Stats:Updated",
            nb_of_lines=_lines,
            total_pages=_nb_pages,
            current_page=_cur_page,
            movie_duration=_mduration,
            movie_duration_label=_time_fmt,
        )
    # end def

# end class ProjectTabScenario
