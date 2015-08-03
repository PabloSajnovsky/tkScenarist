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
import locale
import tkinter.constants as TK
import tkRAD
import tkRAD.core.async as ASYNC
from . import project_file_management as PFM


# app-wide inits (super global)
__builtins__["ENCODING"] = "UTF-8"
__builtins__["STATE_MASK"] = (
    {"nt": 0x20084, "posix": 0x8c}.get(os.name, 0x00)
)
__builtins__["WIN32"] = bool(os.name == "nt")

# i18n locale setup
locale.setlocale(locale.LC_ALL, "")



class MainWindow (tkRAD.RADXMLWindow):
    """
        Application's main window (GUI - Graphical User Interface);
    """

    # class constant defs
    # CAUTION: keep i18n for localized web pages
    MAILING_LIST_URL = _("https://mail.python.org/mailman/listinfo/tkscenarist-help")
    OFFLINE_DOC_URL = _("^/html/en/index.html")
    ONLINE_DOC_URL = _("https://github.com/tarball69/tkScenarist/wiki")


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Edit:Redo":
                    self.slot_edit_redo,
                "Edit:Select:All":
                    self.slot_edit_select_all,
                "Edit:Undo":
                    self.slot_edit_undo,

                "Entry:Key:Pressed":
                    self.slot_entry_key_pressed,

                "Help:About":
                    self.slot_help_about,
                "Help:Mailing:List":
                    self.slot_help_mailing_list,
                "Help:Offline:Documentation":
                    self.slot_help_offline_documentation,
                "Help:Online:Documentation":
                    self.slot_help_online_documentation,

                "Project:Export:PDF":
                    self.project_fm.slot_export_pdf,
                "Project:Modified":
                    self.project_fm.slot_modified,
                "Project:New":
                    self.project_fm.slot_new,
                "Project:Open":
                    self.project_fm.slot_open,
                "Project:Path:Update":
                    self.project_fm.slot_update_path,
                "Project:Save:As":
                    self.project_fm.slot_save_as,
                "Project:Save":
                    self.project_fm.slot_save,

                "Text:Key:Pressed":
                    self.slot_text_key_pressed,

                "Tools:NameDatabase":
                    self.slot_tools_name_db,
                "Tools:Pitch:Templates":
                    self.slot_tools_pitch_templates,
                "Tools:Scenario:Elements:Editor":
                    self.slot_tools_scenario_elements_editor,
            }
        )
        # tkinter event bindings
        self.bind_all("<Control-Q>", self._slot_quit_app)
        # disable unwanted internal bindings
        self.bind_class(
            "TEntry", "<Expose>", self.disable_ttkentry_expose
        )
        self.bind_class(
            "TCombobox", "<<ComboboxSelected>>",
            self.slot_combo_selected,
        )
        for _char in "akoyz":
            self.unbind_class(
                "Text", "<Control-{}>".format(_char.lower())
            )
            self.unbind_class(
                "Text", "<Control-{}>".format(_char.upper())
            )
        # end for
        # close splash screen
        self.after(1000, self.app.hide_splash_screen)
    # end def


    def confirm_quit (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            put here user confirmation dialog for quitting app;
        """
        # user confirmation dialog (accept anything but cancelled)
        return bool(
            self.project_fm.ensure_saved() != self.project_fm.CANCEL
        )
    # end def


    def cvar_get_text (self, cvarname):
        """
            retrieves text from a tk.StringVar() control variable;
        """
        return self.mainframe.get_stringvar(cvarname).get()
    # end def


    def cvar_set_text (self, cvarname, contents):
        """
            set text to a tk.StringVar() control variable;
        """
        self.mainframe.get_stringvar(cvarname).set(contents)
    # end def


    def disable_ttkentry_expose (self, event=None, *args, **kw):
        """
            event handler for disabling unwanted tkinter autoselection
            on ttkEntry widgets;
        """
        try:
            event.widget.selection_clear()
        except:
            pass
        # end try
    # end def


    def init_deferred (self):
        """
            deferred widget inits;
        """
        # lib imports
        from . import app_database as DB
        # this may take a while
        self.database = DB.get_database()
        # looks for ^/xml/widget/mainwindow.xml
        self.xml_build()
        # event bindings
        self.after_idle(self.bind_events)
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # ensure under splash screen (MS-Win fixups)
        self.app.keep_under_splash_screen(self)
        # set root window's title (for dialogs entitling)
        self.app.root.title = self.title
        # member inits
        self.async = ASYNC.get_async_manager()
        self.project_fm = PFM.ProjectFileManagement(self)
        # register as app-wide service
        # PFM: Project File Management
        self.services.register_service("PFM", self.project_fm)
        self.services.register_service("mainwindow", self)
        # looks for ^/xml/menu/topmenu.xml
        self.topmenu.xml_build()
        # toggle statusbar through menu
        self.connect_statusbar("show_statusbar")
        # deferred inits
        self.after_idle(self.init_deferred)
    # end def


    def launch_web_browser (self, url):
        """
            launches web browser with @url URL (online/offline);
        """
        # param controls
        if url:
            # lib imports
            import webbrowser
            import tkinter.messagebox as MB
            # launching web browser
            webbrowser.open(url)
            # warning message
            MB.showwarning(
                title=_("Attention"),
                message=_("Launching web browser, please wait."),
                parent=self,
            )
        # end if
    # end def


    def on_quit_app (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # do it safely
        try:
            # make some terminations
            self.async.clear_all()
            self.database.close_database()
            self.options.save()
            # uncomment the following to get easy
            # i18n translation file template (POT file)
            # i.e. ^/locale/template.pot
            #~ tkRAD.i18n.dump_pot_file()
        except:
            pass
        # end try
    # end def


    def slot_combo_selected (self, event=None, *args, **kw):
        """
            event handler: on combobox item selected;
        """
        # strip that ugly autoselection
        self.after_idle(event.widget.selection_clear)
    # end def


    def slot_edit_redo (self, event=None, *args, **kw):
        """
            event handler: menu Edit > Redo;
        """
        # param controls - MS-Windows workaround
        if not event or WIN32:
            # redo cancelled
            try:
                self.focus_lastfor().edit_redo()
            except:
                pass
            # end try
        # end if
    # end def


    def slot_edit_select_all (self, event=None, *args, **kw):
        """
            event handler: menu Edit > Select all;
        """
        # select all
        try:
            # get last focused widget
            w = self.focus_lastfor()
            # Text widget?
            if hasattr(w, "tag_add"):
                # configure selection tag
                w.tag_configure(
                    TK.SEL, background="grey30", foreground="white"
                )
                # select all text
                w.tag_add(TK.SEL, "1.0", TK.END)
                # this disables tkinter chain of internal bindings
                # thanks to Brian Oakley's cool explanation
                return "break"
            # ttk/Entry widget?
            elif hasattr(w, "select_range"):
                # select all text
                w.select_range(0, TK.END)
            # end if
        except:
            pass
        # end try
    # end def


    def slot_edit_undo (self, event=None, *args, **kw):
        """
            event handler: menu Edit > Undo;
        """
        # param controls
        if not event:
            # undo last
            try:
                self.focus_lastfor().edit_undo()
            except:
                pass
            # end try
        # end if
    # end def


    def slot_entry_key_pressed (self, event=None, *args, **kw):
        """
            event handler: ttkentry key press;
        """
        # notify something has changed
        self.events.raise_event("Project:Modified")
        # validate entry keystrokes
        return True
    # end def


    def slot_help_about (self, *args, **kw):
        """
            event handler: menu Help > About;
        """
        # lib imports
        import tkinter.messagebox as MB
        MB.showinfo(
            title=_("About..."),
            message=_(
                "{title}\n{description}\n{copyright}"
                "\nCurrent version: {version}"
                "\n\nAuthor: {author}"
                "\nCurrent maintainer: {maintainer}"
                "\nPDF toolkit: {pdflib}"
                "\nBy: {pdflib_author}"
                ).format(**self.app.APP),
            parent=self,
        )
    # end def


    def slot_help_mailing_list (self, *args, **kw):
        """
            event handler: menu Help > Get help on mailing list;
        """
        # launch online mailing list website
        self.launch_web_browser(kw.get("url") or self.MAILING_LIST_URL)
    # end def


    def slot_help_offline_documentation (self, *args, **kw):
        """
            event handler: menu Help > Offline documentation;
        """
        # launch offline documentation
        self.launch_web_browser(
            # local file (offline)
            "file://{}".format(
                PFM.P.normalize(kw.get("file") or self.OFFLINE_DOC_URL)
            )
        )
    # end def


    def slot_help_online_documentation (self, *args, **kw):
        """
            event handler: menu Help > Online Documentation;
        """
        # launch online documentation
        self.launch_web_browser(kw.get("url") or self.ONLINE_DOC_URL)
    # end def


    def slot_text_key_pressed (self, event=None, *args, **kw):
        """
            event handler: text widget key press;
        """
        # inits
        _ok = True
        # param controls
        if event:
            # inits
            _w = event.widget
            _ok = bool(_w.edit_modified())
            # undo/redo stack
            if event.keysym == "space":
                _w.edit_separator()
            # end if
        # end if
        # all correct?
        if _ok:
            # notify something has changed
            self.events.raise_event("Project:Modified")
        # end if
    # end def


    def slot_tools_name_db (self, *args, **kw):
        """
            event handler: menu Tools > Name database;
        """
        # lib imports
        from . import dlg_name_database as DND
        # show name database dialog (modal)
        DND.NameDatabaseDialog(self).show()
    # end def


    def slot_tools_pitch_templates (self, *args, **kw):
        """
            event handler: menu Tools > Pitch templates;
        """
        # lib imports
        from . import dlg_pitch_templates as DPT
        # show story/pitch templates dialog (modal)
        DPT.PitchTemplatesDialog(self).show()
    # end def


    def slot_tools_scenario_elements_editor (self, *args, **kw):
        """
            event handler: menu Tools > Scenario Elements Editor (SEE);
        """
        # lib imports
        from . import dlg_scenario_elements_editor as DSEE
        # show tool dialog (modal)
        DSEE.ScenarioElementsEditorDialog(
            self, w_text=self.mainframe.tab_scenario.TEXT
        ).show()
    # end def


    def text_clear_contents (self, tk_text):
        """
            clears text contents for a tkinter.Text widget;
        """
        # clear text widget
        tk_text.delete("1.0", TK.END)
        # reset flags
        tk_text.edit_modified(False)
        tk_text.edit_reset()
    # end def


    def text_get_contents (self, tk_text):
        """
            gets text contents from a tkinter.Text widget;
        """
        return tk_text.get("1.0", TK.END).rstrip() + "\n"
    # end def


    def text_is_empty (self, tk_text):
        """
            returns True if no text contents in a tkinter.Text widget,
            False otherwise;
        """
        return not tk_text.get("1.0").rstrip()
    # end def


    def text_set_contents (self, tk_text, contents=""):
        """
            resets text contents for a tkinter.Text widget;
        """
        # inits
        contents = str(contents).rstrip()
        if contents:
            contents += "\n"
        # end if
        # clear text widget
        tk_text.delete("1.0", TK.END)
        # set contents
        tk_text.insert("1.0", contents)
        # reset flags
        tk_text.edit_modified(False)
        tk_text.edit_reset()
    # end def

# end class MainWindow
