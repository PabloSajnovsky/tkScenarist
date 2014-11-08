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

    TAB_TITLE_CVARS = (
        "project_title",
        "project_author",
        "project_author_email",
        "project_author_phone"
    )


    def __init__ (self, tk_owner):
        """
            class constructor;
        """
        # member inits
        self.tk_owner = tk_owner
        self.mainframe = tk_owner.mainframe
        self.get_cvar_text = tk_owner.get_cvar_text
        self.set_cvar_text = tk_owner.set_cvar_text
        self.current_dir = "~"
        self.ALL_FILES = self.get_files_from_dict(self.ARCHIVE_FILES)
        self.FILE_EXT = self.normalize_file_ext(self.FILE_EXT)
        self.FILE_TYPES = [
            ("tkScenarist files", "*{}".format(self.FILE_EXT)),
            ("zip files", "*.zip"),
        ]
        # hook method
        self.init_members()
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


    def do_open_project (self, fpath):
        """
            effective procedure for opening project;
        """
        # param controls
        if self.is_good_file_format(fpath):
            # notify application
            self.notify(_("Opening project, please wait."))
            # reset to new
            self.do_reset_project()
            # open zip archive
            with zipfile.ZipFile(fpath, 'r') as _archive:
                # browse archive files
                for tab_id, fname in self.ARCHIVE_FILES.items():
                    # simple file contents
                    if tools.is_pstr(fname):
                        # set contents instead
                        fname = _archive.read(fname).decode("UTF-8").rstrip()
                        if fname:
                            fname += "\n"
                        # end if
                    # end if
                    # setup notebook tab
                    self.setup_tab(tab_id, fname, _archive)
                # end for
            # end with
            # we can update project's filepath by now
            self.set_project_path(fpath)
            # notify application
            self.notify(_("Project opened OK."))
            # succeeded
            return True
        # could not open file
        else:
            # show error
            MB.showerror(
                title=_("Error"),
                message=_(
                    "Could not open project. "
                    "Incorrect file path or file format."
                ),
                parent=self.tk_owner,
            )
            # failed
            return False
        # end if
    # end def


    def do_reset_project (self):
        """
            resets project to new;
        """
        # member resets
        self.init_members()
        # GUI resets
        for _cvar in self.mainframe.get_stringvars().values():
            # reset values
            _cvar.set("")
        # end for
        # Text widgets
        self.text_set_contents(self.mainframe.text_draft_notes, "")
        self.text_set_contents(self.mainframe.text_pitch_concept, "")
        self.text_set_contents(self.mainframe.text_characters_log, "")
        self.text_set_contents(self.mainframe.text_scenario, "")
        # Listbox widgets
        self.mainframe.listbox_characters_list.delete(0, "end")
        # Canvas widgets
        self.mainframe.canvas_characters_relations.delete("all")
        # other resets
        self.tk_owner.characters_logs.clear()
        self.slot_project_update_path()
    # end def


    def do_save_project (self, fpath):
        """
            effective procedure for saving project;
        """
        # param inits
        fpath = P.normalize(fpath)
        # param controls
        if tools.is_pstr(fpath):
            # notify application
            self.notify(_("Saving project, please wait."))
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
            self.set_project_path(fpath)
            # notify application
            self.notify(_("Project saved OK."))
            # succeeded
            return True
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
            # failed
            return False
        # end if
    # end def


    def ensure_saved (self):
        """
            ensures modified project will be saved before next step;
            returns True when all is OK, False if dialog has been
            cancelled or any other trouble fired up;
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
            # update flag
            cancelled = response is None
            # answered yes
            if response:
                # save project
                cancelled = not self.slot_project_save()
            # end if
        # end if
        # ensure saved
        return not cancelled
    # end def


    def get_current_dir (self):
        """
            retrieves last used directory for load/save procedure;
        """
        # inits
        _dir = self.current_dir
        # got some path?
        if self.project_path:
            # init dir
            _dir = OP.dirname(self.project_path)
        # end if
        # return normalized directory
        return P.normalize(_dir)
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
        fcontents = ""
        # browse fields
        for _cvarname in self.TAB_TITLE_CVARS:
            fcontents += (
                "{}: {}\n"
                .format(_cvarname, self.get_cvar_text(_cvarname))
            )
        # end for
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


    def get_files_from_dict (self, dict_object):
        """
            extracts filenames from an archive dictionnary;
        """
        # inits
        _flist = list()
        # browse dict items
        for _fname in dict_object.values():
            # got another dict?
            if tools.is_pdict(_fname):
                # extend list with other list
                _flist.extend(self.get_files_from_dict(_fname))
            # must be plain string
            elif tools.is_pstr(_fname):
                # append item
                _flist.append(_fname)
            # end if
        # end for
        # return list of filenames
        return _flist
    # end def


    def init_members (self):
        """
            class members init/reset;
        """
        # inits
        self.project_path = ""
        self.slot_project_modified(flag=False)
    # end def


    def is_good_file_format (self, fpath):
        """
            determines if @fpath has the correct zip archive internal
            structure;
        """
        # param inits
        fpath = P.normalize(fpath)
        # got a zip archive?
        if zipfile.is_zipfile(fpath):
            # examine archive contents
            with zipfile.ZipFile(fpath, "r") as _archive:
                # get all zip archive members
                _zfiles = _archive.namelist()
            # end with
            # compare contents
            return bool(set(self.ALL_FILES) == set(_zfiles))
        # end if
        # failure
        return False
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


    @property
    def project_path (self):
        """
            project's file path;
            normalized to comply with tkRAD.path.support;
        """
        return self.__project_path
    # end def

    @project_path.setter
    def project_path (self, value):
        # inits
        self.__project_path = P.normalize(value)
    # end def

    @project_path.deleter
    def project_path (self):
        del self.__project_path
    # end def


    def set_project_path (self, fpath):
        """
            sets project's path + app notifications;
        """
        # inits
        self.project_path = fpath
        # project is now ready for new changes
        self.slot_project_modified(flag=False)
        # notify application
        self.mainframe.events.raise_event(
            "Project:Path:Update", new_path=fpath
        )
    # end def


    def setup_tab (self, tab_id, fname, archive):
        """
            generic notebook tab initializer along @archive contents;
            dispatches tasks between specific @tab_id with @fname;
        """
        # init attribute
        _method = getattr(self, "setup_{}".format(tab_id), None)
        # redirect to specific task
        if callable(_method):
            # void methods
            _method(fname, archive)
        # end if
    # end def


    def setup_tab_characters (self, fname, archive):
        """
            specific tab initializer;
        """
        print("setup_tab:fname:", fname)
    # end def


    def setup_tab_notes (self, fname, archive):
        """
            specific tab initializer;
        """
        # set text widget contents
        self.text_set_contents(self.mainframe.text_draft_notes, fname)
    # end def


    def setup_tab_pitch (self, fname, archive):
        """
            specific tab initializer;
        """
        # set text widget contents
        self.text_set_contents(self.mainframe.text_pitch_concept, fname)
    # end def


    def setup_tab_resources (self, fname, archive):
        """
            specific tab initializer;
        """
        print("setup_tab:fname:", fname)
    # end def


    def setup_tab_scenario (self, fname, archive):
        """
            specific tab initializer;
        """
        # set text widget contents
        self.text_set_contents(self.mainframe.text_scenario, fname)
    # end def


    def setup_tab_storyboard (self, fname, archive):
        """
            specific tab initializer;
        """
        print("setup_tab:fname:", fname)
    # end def


    def setup_tab_title (self, fname, archive):
        """
            specific tab initializer;
        """
        # browse file lines
        for _line in fname.split("\n"):
            # inits
            _line = _line.strip()
            # got data?
            if ":" in _line:
                # get field_name: field_value
                _name, _value = _line.split(":")
                _name = _name.strip().lower()
                _value = _value.strip()
                # supported field name?
                if _name in self.TAB_TITLE_CVARS:
                    # update value
                    self.set_cvar_text(_name, _value)
                # end if
            # end if
        # end for
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
        # all is OK?
        if self.ensure_saved():
            # reset project to new
            self.do_reset_project()
        # cancelled
        else:
            # notify application
            self.notify(_("Project > New: cancelled."))
        # end if
    # end def


    def slot_project_open (self, *args, **kw):
        """
            event handler for menu Project > Open;
        """
        # 'open' procedure
        _fpath = FD.askopenfilename(
            title=_("Open project file..."),
            defaultextension=self.FILE_EXT,
            filetypes=self.FILE_TYPES,
            initialdir=self.get_current_dir(),
            multiple=False,
            parent=self.tk_owner,
        )
        # not cancelled?
        if _fpath:
            # do open project
            return self.do_open_project(_fpath)
        # cancelled
        else:
            # notify application
            self.notify(_("Project > Open: cancelled."))
            # failed
            return False
        # end if
    # end def


    def slot_project_save (self, *args, **kw):
        """
            event handler for menu Project > Save;
        """
        # unsaved project?
        if not self.is_good_file_format(self.project_path):
            # rather save as...
            return self.slot_project_save_as()
        # okay, save by now
        else:
            # use current project's filepath
            return self.do_save_project(self.project_path)
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
            filetypes=self.FILE_TYPES,
            initialdir=self.get_current_dir(),
            confirmoverwrite=True,
            parent=self.tk_owner,
        )
        # not cancelled?
        if _fpath:
            # do save project
            return self.do_save_project(_fpath)
        # cancelled
        else:
            # notify application
            self.notify(_("Project > Save as...: cancelled."))
            # failed
            return False
        # end if
    # end def


    def slot_project_update_path (self, *args, new_path=None, **kw):
        """
            event handler for GUI display updates;
        """
        # inits
        _path = P.normalize(new_path)
        # param controls
        if _path:
            # inits
            _fname = OP.basename(_path)
            _dir = OP.dirname(_path)
            # update members
            self.current_dir = _dir
            # update GUI
            self.mainframe.get_stringvar("project_filename").set(_fname)
            self.mainframe.get_stringvar("project_directory").set(_dir)
            self.tk_owner.title(
                "{} - {}"
                .format(self.tk_owner.app.APP["title"], _fname)
            )
        # empty path
        else:
            # reset window title
            self.tk_owner.title(self.tk_owner.app.APP["title"])
        # end if
    # end def


    def text_set_contents (self, tk_text, contents=""):
        """
            resets text contents for a tkinter.Text widget;
        """
        # inits
        tk_text.delete("1.0", "end")
        tk_text.insert("1.0", str(contents))
        tk_text.edit_modified(False)
        tk_text.edit_reset()
    # end def

# end class ProjectFileManagement
