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


class ProjectTabTitleData (tkRAD.RADXMLFrame):
    """
        application's project tab class;
    """

    # class constant defs
    FIELD_CVARNAMES = (
        "project_title",
        "project_subtitle",
        "project_episode",
        "project_author",
        "project_author_email",
        "project_author_phone",
    )

    INFO_CVARNAMES = (
        "project_filename",
        "project_directory",
        "scenario_nb_of_pages",
        "scenario_movie_duration",
    )


    def bind_events (self, **kw):
        """
            app-wide event bindings;
        """
        self.events.connect_dict(
            {
                "Project:Path:Update": self.slot_update_path,

                "Scenario:Stats:Updated": self.slot_update_stats,

                "Tab:Reset": self.slot_tab_reset,
            }
        )
    # end def


    def cvar_get_text (self, cvarname):
        """
            retrieves text from a tk.StringVar() control variable;
        """
        return self.get_stringvar(cvarname).get()
    # end def


    def cvar_set_text (self, cvarname, contents):
        """
            set text to a tk.StringVar() control variable;
        """
        self.get_stringvar(cvarname).set(contents)
    # end def


    def get_file_contents (self, fname):
        """
            returns file contents;
        """
        # inits
        fcontents = ""
        # browse fields
        for _cvarname in self.FIELD_CVARNAMES:
            fcontents += (
                "{}: {}\n"
                .format(_cvarname, self.cvar_get_text(_cvarname))
            )
        # end for
        # always return a dict
        return {fname: fcontents}
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented by subclass;
        """
        # looks for ^/xml/widget/tab_title_data.xml
        self.xml_build("tab_title_data")
        # event bindings
        self.bind_events(**kw)
    # end def


    def setup_tab (self, fname, archive):
        """
            tab setup along @fname and @archive contents;
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
                if _name in self.FIELD_CVARNAMES:
                    # update value
                    self.cvar_set_text(_name, _value)
                # end if
            # end if
        # end for
    # end def


    def slot_tab_reset (self, *args, **kw):
        """
            event handler: reset tab to new;
        """
        # reset stringvars
        for _cvar in self.get_stringvars().values():
            _cvar.set("")
        # end for
    # end def


    def slot_update_path (self, *args, filename=None, directory=None, **kw):
        """
            event handler for GUI display updates;
        """
        # param controls
        if filename and directory:
            # update GUI
            self.cvar_set_text("project_filename", filename)
            self.cvar_set_text("project_directory", directory)
        # end if
    # end def


    def slot_update_stats (self, *args, **kw):
        """
            event handler: updates stats info;
        """
        # update info
        self.cvar_set_text(
            "scenario_nb_of_pages",
            kw.get("total_pages") or ""
        )
        self.cvar_set_text(
            "scenario_movie_duration",
            kw.get("movie_duration_label") or ""
        )
    # end def

# end class ProjectTabTitleData
