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

#~ tkRAD.i18n.switch_off()


class tkScenarist (tkRAD.RADApplication):

    # class constant defs
    APP = {
        "name": _("tkScenarist"),
        "version": _("0.9b"),
        "description": _("Movie scriptwriting utility program."),
        "title": _("tkScenarist - screen writing made simpler"),
        "author": _("Raphaël SEBAN <motus@laposte.net>"),
        # current maintainer (may be different from author)
        "maintainer": _("Raphaël SEBAN"),
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
        # tkinter root window inits
        self.init_root_window()
        # splash screen inits
        self.init_splash_screen()
        # show splash screen
        self.show_splash_screen()
        # application main window inits (tkRAD - GUI)
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


    def init_root_window (self, *args, **kw):
        """
            event handler: sets up the Tk() root window;
        """
        # lib imports
        from tkinter import Tk
        # tkinter root window inits
        self.root = Tk()
        # hide this ugly window
        self.root.withdraw()
        # raise above all (MS-Win fixups)
        self.root.lift()
    # end def


    def init_splash_screen (self, *args, **kw):
        """
            event handler: sets up a tkinter.Toplevel splash screen;
        """
        # lib imports
        from tkinter import Toplevel, Frame, Label
        # inits
        _sp = self.splash = Toplevel(
            self.root,
            relief="solid",
            highlightthickness=1,
            highlightbackground="grey50",
        )
        _sp.withdraw()
        _sp.overrideredirect(True)
        _sp.bind("<Button-1>", self.hide_splash_screen)
        _frame = Frame(_sp, background="grey95")
        Label(
            _frame,
            text=self.APP["name"],
            font="times 36 bold italic",
            background=_frame["background"],
            foreground="royal blue",
        ).pack(expand=1, fill="x", padx=20)
        Label(
            _frame,
            text=_("Loading application, please wait..."),
            font="helvetica 9",
            background=_frame["background"],
            foreground="grey20",
        ).pack(expand=1, fill="x", padx=20, pady=10)
        _frame.pack()
        # update coordinates
        _sp.update_idletasks()
        # center on screen
        _sp.geometry(
            "+{x}+{y}"
            .format(
                x=(_sp.winfo_screenwidth() - _sp.winfo_reqwidth())//2,
                y=(_sp.winfo_screenheight() - _sp.winfo_reqheight())//2,
            )
        )
    # end def


    def keep_under_splash_screen (self, window):
        """
            event handler: tries to keep @window display under splash
            screen;
        """
        # MS-Win fixups
        try:
            window.lower(self.splash)
        except:
            pass
        # end try
    # end def


    def show_splash_screen (self, *args, **kw):
        """
            event handler: shows up splash screen;
        """
        try:
            # show splash screen
            self.splash.deiconify()
            # raise above all
            self.splash.lift()
            # update display for more efficiency
            self.splash.update()
        except:
            pass
        # end try
    # end def

# end class tkScenarist


# asked for launching?
if __name__ == "__main__":
    # run app
    tkScenarist().run()
# end if
