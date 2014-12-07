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
                "Scenario:Text:FocusedIn": self.slot_text_focused_in,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
        # tkinter event bindings
        self.bind("<Expose>", self.slot_on_expose)
        self.COMBO.bind(
            "<<ComboboxSelected>>", self.slot_combo_item_selected
        )
        self.LISTBOX.bind(
            "<<ListboxSelect>>", self.slot_listbox_item_selected
        )
        self.TEXT.bind("<FocusOut>", self.slot_on_focus_out, "+")
        # multiple event inits
        _events = {
            "<Key>": self.slot_popup_keypress,
            "<KeyRelease>": self.slot_popup_keyrelease,
            "<Button-1>": self.slot_popup_clicked,
            "<Double-Button-1>": self.slot_popup_double_clicked,
            "<<ListboxSelect>>": self.slot_popup_item_selected,
        }
        for _seq, _slot in _events.items():
            self.POPUP_LBOX.bind(_seq, _slot)
        # end for
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
        # stop pending popup openings
        self.async.stop(self.slot_autocomplete)
        # hide popup list
        self.POPUP.withdraw()
        self.POPUP.start_index = None
        self.POPUP_LBOX.current_index = 0
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


    def popup_is_active (self):
        """
            returns True if popup window is detected as active (showing
            up);
        """
        return bool(self.POPUP.state() == "normal")
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
        # ensure no tkinter.messagebox is up there
        try:
            if self.grab_current(): return self.hide_popup_list()
        except:
            return self.hide_popup_list()
        # end try
        # stop pending tasks
        self.async.stop(self.hide_popup_list, self.slot_autocomplete)
        # inits
        choices = kw.get("choices")
        start_index = kw.get("start_index") or "insert"
        self.POPUP.start_index = start_index
        # param controls
        if choices:
            _lb = self.POPUP_LBOX
            _lb.delete(0, "end")
            _lb.insert(0, *choices)
            try:
                _lb.selection_set(_lb.current_index)
                _lb.see(_lb.current_index)
            except:
                _lb.selection_set(0)
                _lb.see(0)
                _lb.current_index = 0
            # end try
            _lb.configure(
                height=min(5, len(choices)),
                width=min(40, max(map(len, choices))),
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


    def slot_on_expose (self, event=None, *args, **kw):
        """
            event handler: tab widget becomes visible;
        """
        # go to text widget
        self.TEXT.focus_set()
    # end def


    def slot_on_focus_out (self, event=None, *args, **kw):
        """
            event handler: widget has lost focus;
        """
        self.async.run_after_idle(self.hide_popup_list)
    # end def


    def slot_popup_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse click on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # stop pending tasks
            self.after_idle(
                self.async.stop,
                self.hide_popup_list,
                self.slot_autocomplete
            )
        # end if
    # end def


    def slot_popup_double_clicked (self, event=None, *args, **kw):
        """
            event handler: mouse double click on popup;
        """
        # do insert text completion
        return self.slot_popup_insert()
    # end def


    def slot_popup_insert (self, event=None, *args, **kw):
        """
            event handler: tab/return keypress on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _lb = self.POPUP_LBOX
            _name = _lb.get(_lb.curselection()[0])
            # replace text
            self.TEXT.replace_text(
                _name, self.POPUP.start_index, smart_delete=True
            )
            # reset focus
            self.after_idle(self.TEXT.focus_set)
            # break tkevent chain
            return "break"
        # end if
    # end def


    def slot_popup_item_selected (self, event=None, *args, **kw):
        """
            event handler: item selected on popup;
        """
        # update current index
        self.POPUP_LBOX.current_index = self.POPUP_LBOX.curselection()[0]
        # break tkevent chain
        return "break"
    # end def


    def slot_popup_key_arrows (self, event=None, *args, **kw):
        """
            event handler: up/down keypress on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _key = event.keysym.lower()
            _lb = self.POPUP_LBOX
            _ci = _lb.current_index
            # update index
            _ci += int(_key == "down") - int(_key == "up")
            # rebind index
            _ci = max(0, min(_ci, _lb.size() - 1))
            # reset selection
            _lb.current_index = _ci
            _lb.selection_clear(0, "end")
            _lb.selection_set(_ci)
            _lb.see(_ci)
            # break tkevent chain
            return "break"
        # end if
    # end def


    def slot_popup_keypress (self, event=None, *args, **kw):
        """
            event handler: any keypress on popup;
        """
        # ensure popup is shown up
        if self.popup_is_active():
            # inits
            _key = event.keysym
            # specific keystrokes
            if _key in ("Escape",):
                # hide popup (transferred to slot_popup_keyrelease)
                pass
            # up/down arrow keys
            elif _key in ("Up", "Down"):
                # manage into popup
                return self.slot_popup_key_arrows(event, *args, **kw)
            # tab/return keystrokes
            elif _key in ("Tab", "Return"):
                # manage into popup
                return self.slot_popup_insert(event, *args, **kw)
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
        if self.popup_is_active():
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
        # new project
        self.events.raise_event("Project:Modified", flag=False)
    # end def


    def slot_text_clicked (self, event=None, *args, **kw):
        """
            event handler: text widget has been clicked;
        """
        # hide popup list
        self.hide_popup_list()
    # end def


    def slot_text_focused_in (self, event=None, *args, **kw):
        """
            event handler: text widget gets focused again;
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
        # update hints
        self.async.run_after(1000, self.update_hints)
        # update stats
        self.async.run_after(500, self.update_stats)
        # update scene browser
        self.async.run_after(200, self.update_scene_browser)
        # update character log
        self.async.run_after(100, self.update_character_log)
    # end def


    def update_character_log (self, *args, **kw):
        """
            event handler: updates character's log info, if any;
        """
        # inits
        _tc = self.tab_characters
        _line = self.TEXT.get_line_contents()
        _name, _start_index = _tc.find_nearest_name(
            _line, self.TEXT.get_column_index()
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
            # name not in good format?
            if _name not in _line:
                # update name into text contents
                _index = "{0}+{{}}c".format(self.TEXT.INS_LINE[0])
                self.TEXT.replace_text(
                    _name,
                    _index.format(_start_index),
                    _index.format(_start_index + len(_name)),
                    keep_cursor=True,
                )
            # end if
            # no need to autocomplete
            self.hide_popup_list()
        # unknown
        else:
            # clear info
            self.LBL_CHAR_NAME.set("")
            self.text_clear_contents(self.TXT_CHAR_LOG)
            # look out for autocompletion
            self.async.run_after_idle(self.slot_autocomplete)
        # end if
        # disable widget
        self.TXT_CHAR_LOG.configure(state="disabled")
    # end def


    def update_hints (self):
        """
            shows off hints text according to current line tag value;
            displays default hints otherwise;
        """
        # inits
        _tag = self.TEXT.get_line_tag()
        _hints = (
            self.INFO_HINTS.get(_tag)
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
        self.LISTBOX.selection_clear(0, "end")
        # insertion cursor is on a scene line?
        if _cursor in _lines:
            # init
            all_is_clear = not (
                self.TEXT.line_selected(float(_cursor))
                or self.popup_is_active()
            )
            # all is clear?
            if all_is_clear:
                # inits
                _index = _lines.index(_cursor)
                # select item
                self.LISTBOX.selection_set(_index)
                # show item
                self.LISTBOX.see(_index)
            # end if
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
