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
        "tab_title_data": "title_data.txt",
        "tab_draft_notes": "draft_notes.txt",
        "tab_pitch_concept": "pitch_concept.txt",
        "tab_characters": {
            "names": "characters_names.txt",
            "logs": "characters_logs.txt",
            "relations": "characters_relations.txt",
        },
        "tab_scenario": {
            "text": "scenario_text.txt",
            "tags": "scenario_tags.txt",
            "elements": "scenario_elements.txt",
        },
        "tab_storyboard": "storyboard.txt",
        "tab_resources": "resources.txt",
    }

    FILE_EXT = "scn"


    def __init__ (self, tk_owner):
        """
            class constructor;
        """
        # member inits
        self.mainwindow = tk_owner
        self.mainframe = tk_owner.mainframe
        self.notify = tk_owner.statusbar.notify
        self.current_dir = tk_owner.options.get(
            "dirs", "pfm_preferred_dir", fallback="~"
        )
        self.ALL_FILES = self.get_files_from_dict(self.ARCHIVE_FILES)
        self.FILE_EXT = self.normalize_file_ext(self.FILE_EXT)
        self.FILE_TYPES = [
            (_("tkScenarist files"), "*{}".format(self.FILE_EXT)),
            (_("zip files"), "*.zip"),
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
                        fname = _archive.read(fname).decode(ENCODING)
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
                parent=self.mainwindow,
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
        self.mainwindow.events.raise_event("Tab:Reset")
        # other resets
        self.slot_update_path()
        # project is reset to new
        self.slot_modified(flag=False)
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
                    _contents = self.get_fc_tab(tab_id, fname)
                    # browse contents
                    for _fname, _fcontents in _contents.items():
                        # put files and contents into zip archive
                        _archive.writestr(
                            _fname, bytes(_fcontents, ENCODING)
                        )
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
                parent=self.mainwindow,
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
                cancelled = not self.slot_save()
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


    def get_fc_tab (self, tab_id, fname):
        """
            generic file contents dispatcher;
        """
        # init attribute
        _method = getattr(
            getattr(self.mainframe, tab_id), "get_file_contents", None
        )
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
        self.slot_modified(flag=False)
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
        fpath = P.normalize(fpath)
        _fname = OP.basename(fpath)
        _dir = OP.dirname(fpath)
        # member inits
        self.project_path = fpath
        # project is now ready for new changes
        self.mainwindow.events.raise_event(
            "Project:Modified", flag=False
        )
        # notify application
        self.mainwindow.events.raise_event(
            "Project:Path:Update",
            new_path=fpath, filename=_fname, directory=_dir,
        )
    # end def


    def setup_tab (self, tab_id, fname, archive):
        """
            generic notebook tab initializer along @archive contents;
            dispatches tasks between specific @tab_id with @fname;
        """
        # init attribute
        _method = getattr(
            getattr(self.mainframe, tab_id), "setup_tab", None
        )
        # redirect to specific task
        if callable(_method):
            # void methods
            _method(fname, archive)
        # end if
    # end def


    def slot_export_pdf (self, *args, **kw):
        """
            event handler for menu Project > Export PDF;
        """
        print("Menu:Project:Export PDF")
    # end def


    def slot_modified (self, *args, flag=True, **kw):
        """
            event handler for project's modification flag;
        """
        # inits
        self.project_modified = bool(flag)
        # update visual indicator
        _title = self.mainwindow.title().rstrip("*")
        if flag:
            _title += "*"
        # end if
        self.mainwindow.title(_title)
    # end def


    def slot_new (self, *args, **kw):
        """
            event handler for menu Project > New;
        """
        # current project is saved?
        if self.ensure_saved():
            # reset project to new
            self.do_reset_project()
        # cancelled
        else:
            # notify application
            self.notify(_("Project > New: cancelled."))
        # end if
    # end def


    def slot_open (self, *args, **kw):
        """
            event handler for menu Project > Open;
        """
        # inits
        _fpath = None
        # current project is saved?
        if self.ensure_saved():
            # open project file dialog
            _fpath = FD.askopenfilename(
                title=_("Open project file..."),
                defaultextension=self.FILE_EXT,
                filetypes=self.FILE_TYPES,
                initialdir=self.get_current_dir(),
                multiple=False,
                parent=self.mainwindow,
            )
        # end if
        # got path?
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


    def slot_save (self, *args, **kw):
        """
            event handler for menu Project > Save;
        """
        # unsaved project?
        if not self.is_good_file_format(self.project_path):
            # rather save as...
            return self.slot_save_as()
        # okay, save by now
        else:
            # use current project's filepath
            return self.do_save_project(self.project_path)
        # end if
    # end def


    def slot_save_as (self, *args, **kw):
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
            parent=self.mainwindow,
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


    def slot_update_path (self, *args, filename=None, directory=None, **kw):
        """
            event handler for GUI display updates;
        """
        # inits
        _title = self.mainwindow.app.APP["title"]
        # param controls
        if filename and directory:
            # update members
            self.current_dir = directory
            self.mainwindow.options["dirs"]["pfm_preferred_dir"] = directory
            # update GUI
            self.mainwindow.title("{} - {}".format(_title, filename))
        # empty path
        else:
            # reset window title
            self.mainwindow.title(_title)
        # end if
    # end def

# end class ProjectFileManagement
