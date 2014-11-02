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


class tkScenarist (tkRAD.RADApplication):

    APP = {
        "name": _("tkScenarist"),
        "version": _("0.1a"),
        "description": _("Movie scriptwriting utility program."),
        "title": _("tkScenarist - screen writing made simpler"),
        "author": _("Raphaël SEBAN <motus@laposte.net>"),
        # current maintainer (may be different from author)
        "maintainer": _("idem"),
        "copyright": _("(c) 2014+ Raphaël SEBAN."),
        "license": _("""\
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.

If not, see: http://www.gnu.org/licenses/
        """),
        "license_url": _("http://www.gnu.org/licenses/"),
    } # end of APP

    DIRECTORIES = (
        "etc", "src", "locale", "xml",
    ) # end of DIRECTORIES

    PYTHON = {
        "version": "3.2",
        "strict": False,
    } # end of PYTHON

    RC_OPTIONS = {
        "user_file": "user_options.rc",
        "user_dir": "^/etc",
        "app_file": "application.rc",
        "app_dir": "^/etc",
    } # end of RC_OPTIONS


    def _start_gui (self, **kw):
        # GUI
        import src.mainwindow as MW
        self.mainwindow = MW.MainWindow(**kw)
        self.mainwindow.run()
    # end def

# end class tkScenarist


if __name__ == "__main__":

    tkScenarist().run()

# end if
