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

    # class constant defs
    APP = {
        "name": _("tkScenarist"),
        "version": _("0.9b"),
        "description": _("Movie scriptwriting utility program."),
        "title": _("tkScenarist - screen writing made simpler"),
        "author": _("Raphaël SEBAN <motus@laposte.net>"),
        # current maintainer (may be different from author)
        "maintainer": _("idem."),
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
        """).strip(),
        "license_url": _("http://www.gnu.org/licenses/"),
        "pdflib": _("ReportLab®"),
        "pdflib_author": _("(c) ReportLab Europe Ltd. 2000-2012"),
    } # end of APP

    DIRECTORIES = (
        "data", "etc", "html", "locale", "reportlab", "src", "tkRAD",
        "xml",
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
        # lib imports
        from tkinter import Tk
        # get root
        self.root = Tk()
        self.root.withdraw()
        # show splash screen
        self.show_splash_screen()
        # GUI
        import src.mainwindow as MW
        self.mainwindow = MW.MainWindow(**kw)
        self.mainwindow.run()
    # end def


    def hide_splash_screen (self, *args, **kw):
        """
            event handler: hides application's splash screen;
        """
        try:
            self.splash.withdraw()
        except:
            pass
        # end try
    # end def


    def show_splash_screen (self, *args, **kw):
        """
            event handler: shows up a tkinter.Toplevel splash screen;
        """
        # lib imports
        from tkinter import Toplevel
        from tkinter.ttk import Frame, Label
        # inits
        self.splash = _splash = Toplevel(
            self.root,
            relief="solid",
            highlightthickness=1,
            highlightbackground="grey50",
        )
        _splash.withdraw()
        _splash.overrideredirect(True)
        _splash.bind("<Button-1>", self.hide_splash_screen)
        _frame = Frame(_splash, padding=20)
        Label(
            _frame,
            text=self.APP["name"],
            foreground="royal blue",
            font="monospace 36 bold",
        ).pack()
        Label(
            _frame,
            text=_("Loading application, please wait..."),
            foreground="grey30",
            font="sans 8",
        ).pack()
        _frame.pack()
        # update coordinates
        _splash.update_idletasks()
        # center on screen
        _splash.geometry(
            "+{x}+{y}".format(
                x=(
                    self.winfo_screenwidth()-_splash.winfo_reqwidth()
                )//2,
                y=(
                    self.winfo_screenheight()-_splash.winfo_reqheight()
                )//2,
            )
        )
        # show splash screen
        _splash.deiconify()
        # update display
        _splash.update_idletasks()
    # end def

# end class tkScenarist


# asked for launching?
if __name__ == "__main__":
    # run app
    tkScenarist().run()
# end if
