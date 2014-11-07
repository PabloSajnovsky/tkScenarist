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
import zipfile
import tkinter.messagebox as MB
import tkinter.filedialog as FD
from tkRAD.core import tools
from tkRAD.core import path as P


class ProjectFileManagement:
    """
        application's project file management class;
    """

    # class constant defs
    ARCHIVE_FILES = {
        "tab_title": "title_data.txt",
        "tab_notes": "draft_notes.txt",
        "tab_pitch": "pitch_concept.txt",
        "tab_characters": {
            "names": "characters_names.txt",
            "logs": "characters_logs.txt",
            "relations": "characters_relations.txt",
        },
        "tab_scenario": "scenario.txt",
        "tab_storyboard": "storyboard.txt",
        "tab_resources": "resources.txt",
    }
    FILE_EXT = "scn"


    def __init__ (self, tk_owner):
        """
            class constructor;
        """
        # member inits
        self.tk_owner = tk_owner
        self.mainframe = tk_owner.mainframe
        self.get_cvar_text = tk_owner.get_cvar_text
        self.FILE_EXT = self.normalize_file_ext(self.FILE_EXT)
        self.project_path = ""
        self.project_modified = False
    # end def


    def do_reset_project (self):
        """
            resets project to new;
        """
        # member resets
        self.project_path = ""
        self.slot_project_modified(flag=False)
        # GUI resets
        for _cvar in self.mainframe.get_stringvars().values():
            # reset values
            _cvar.set("")
        # end for
        # Text widgets
        # Listbox widgets
        # other resets
    # end def


    def do_save_project (self, fpath):
        """
            effective procedure for saving project;
        """
        # param inits
        fpath = P.normalize(fpath)
        # param controls
        if tools.is_pstr(fpath):
            # open zip archive
            with zipfile.ZipFile(fpath, 'w') as _archive:
                # browse archive files
                for tab_id, fname in self.ARCHIVE_FILES.items():
                    # get multiple files and contents
                    _contents = self.get_files_contents(tab_id, fname)
                    # browse contents
                    for _fname, _fcontents in _contents.items():
                        # put files and contents into zip archive
                        _archive.writestr(_fname, bytes(_fcontents, "UTF-8"))
                    # end for
                # end for
            # end with
            # we can update project's filepath by now
            self.project_path = fpath
            # project is now ready for new changes
            self.slot_project_modified(flag=False)
            # notify application
            self.notify(_("project file saved OK."))
        # could not save file
        else:
            # show error
            MB.showerror(
                title=_("Error"),
                message=_(
                    "Could not save project. Incorrect file path."
                ),
                parent=self.tk_owner,
            )
        # end if
    # end def


    def get_fc_tab_characters (self, fname):
        """
            specific file contents extractor;
        """
        # multiple files and contents
        _dict = dict()
        # list of character names
        _fname = fname["names"]
        _fcontents = "\n".join(
            self.mainframe.listbox_characters_list.get(0, "end")
        )
        _dict[_fname] = _fcontents
        # character logs
        _fname = fname["logs"]
        _fcontents = ""                                                     # FIXME
        _dict[_fname] = _fcontents
        # character relations
        _fname = fname["relations"]
        _fcontents = ""                                                     # FIXME
        _dict[_fname] = _fcontents
        # always return a dict
        return _dict
    # end def


    def get_fc_tab_notes (self, fname):
        """
            specific file contents extractor;
        """
        # inits
        fcontents = self.mainframe.text_draft_notes.get("1.0", "end")
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_fc_tab_pitch (self, fname):
        """
            specific file contents extractor;
        """
        # inits
        fcontents = self.mainframe.text_pitch_concept.get("1.0", "end")
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_fc_tab_resources (self, fname):
        """
            specific file contents extractor;
        """
        # coming soon
        fcontents = ""                                                      # FIXME
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_fc_tab_scenario (self, fname):
        """
            specific file contents extractor;
        """
        # inits
        fcontents = self.mainframe.text_scenario.get("1.0", "end")
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_fc_tab_storyboard (self, fname):
        """
            specific file contents extractor;
        """
        # coming soon
        fcontents = ""                                                      # FIXME
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_fc_tab_title (self, fname):
        """
            specific file contents extractor;
        """
        # inits
        fcontents = (
            "title: {}\n"
            "author: {}\n"
            "email: {}\n"
            "phone: {}\n"
            .format(
                self.get_cvar_text("project_title"),
                self.get_cvar_text("project_author"),
                self.get_cvar_text("project_author_email"),
                self.get_cvar_text("project_author_phone"),
            )
        )
        # always return a dict
        return {fname: fcontents}
    # end def


    def get_files_contents (self, tab_id, fname):
        """
            generic file contents dispatcher;
        """
        # init attribute
        _method = getattr(self, "get_fc_{}".format(tab_id), None)
        # redirect to specific task
        if callable(_method):
            # return dict of {fname:fcontents, ...} items
            return _method(fname)
        # end if
    # end def


    def normalize_file_ext (self, file_ext):
        """
            resets file extension to match a correct format;
        """
        # canonize file extension
        return ".{}".format(tools.normalize_id(file_ext) or "zip").lower()
    # end def


    def notify (self, message):
        """
            notifies @message to application;
        """
        self.tk_owner.statusbar.notify(message)
    # end def


    def slot_project_export_pdf (self, *args, **kw):
        """
            event handler for menu Project > Export PDF;
        """
        print("Menu:Project:Export PDF")
    # end def


    def slot_project_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        self.project_modified = bool(flag)
        # update visual indicator
        _title = self.tk_owner.title().rstrip("*")
        if flag:
            _title += "*"
        # end if
        self.tk_owner.title(_title)
    # end def


    def slot_project_refresh_info (self, *args, **kw):
        """
            event handler for tab Title/Data, button 'Refresh';
        """
        print("Tab:Title/Data:Information:Refresh")
    # end def


    def slot_project_new (self, *args, **kw):
        """
            event handler for menu Project > New;
        """
        # inits
        cancelled = False
        # got to save first?
        if self.project_modified:
            # ask for saving
            response = MB.askyesnocancel(
                _("Question"),
                _("Project has been modified. Save it?")
            )
            cancelled = response is None
            # answered yes
            if response:
                # save project
                self.slot_project_save()
            # end if
        # end if
        # cancelled?
        if cancelled:
            # notify application
            self.notify(_("Project > New: cancelled."))
        # okay, let's go!
        else:
            # reset project to new
            self.do_reset_project()
        # end if
    # end def


    def slot_project_open (self, *args, **kw):
        """
            event handler for menu Project > Open;
        """
        print("Menu:Project:Open")
    # end def


    def slot_project_save (self, *args, **kw):
        """
            event handler for menu Project > Save;
        """
        # unsaved project?
        if not zipfile.is_zipfile(self.project_path):
            # rather save as...
            self.slot_project_save_as()
        # okay, save by now
        else:
            # use current project's filepath
            self.do_save_project(self.project_path)
        # end if
    # end def


    def slot_project_save_as (self, *args, **kw):
        """
            event handler for menu Project > Save as...;
        """
        # 'save as' procedure
        _fpath = FD.asksaveasfilename(
            title=_("Save as..."),
            defaultextension=self.FILE_EXT,
            filetypes=[
                ("tkScenarist files", "*{}".format(self.FILE_EXT)),
                ("zip files", "*.zip"),
            ],
            initialdir=".",                     # FIXME: user prefs?
            confirmoverwrite=True,
            parent=self.tk_owner,
        )
        # not cancelled?
        if _fpath:
            # do save project
            self.do_save_project(_fpath)
        # cancelled
        else:
            # notify application
            self.notify(_("Project > Save as...: cancelled."))
        # end if
    # end def

# end class ProjectFileManagement
