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
from tkinter import Toplevel, Frame, Label



class SplashScreen (Toplevel):
    """
        Generic splash screen window for apps;
    """

    # class constant defs
    APP_NAME = "My Application"

    BG_COLOR = "grey50"

    DEFAULT_CONFIG = {
        "relief": "solid",
        "highlightthickness": 1,
        "highlightbackground": "grey50",
    }

    FG_COLOR1 = "royal blue"
    FG_COLOR2 = "grey20"

    FONT1 = "times 36 bold italic"
    FONT2 = "helvetica 9"


    def __init__ (self, master=None, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(master)
        # member inits
        self.master = master
        # widget inits
        self.init_widget(**kw)
    # end def


    def hide (self, *args, **kw):
        """
            event handler: hides current splash screen;
        """
        # hide splash screen
        self.withdraw()
    # end def


    def init_widget (self, **kw):
        """
            widget internal content inits;
        """
        # ensure not visible
        self.hide()
        # no borders
        self.overrideredirect(True)
        # auto remove on mouse click
        self.bind("<Button-1>", self.hide)
        # config inits
        _cfg = self.DEFAULT_CONFIG.copy()
        _cfg.update(kw)
        self.configure(**_cfg)
        # hook method: widget content inits
        self.set_widget_contents(**kw)
        # update coordinates
        self.update_idletasks()
        # center on screen
        self.geometry(
            "+{x}+{y}"
            .format(
                x=(self.winfo_screenwidth() - self.winfo_reqwidth())//2,
                y=(self.winfo_screenheight() - self.winfo_reqheight())//2,
            )
        )
    # end def


    def set_widget_contents (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        #
        # put your own code in subclass
        #
        # widgets container init
        _frame = Frame(self, background=self.BG_COLOR)
        # app name inits
        try:
            _text = self.master.APP["name"]
        except:
            _text = self.APP_NAME
        # end try
        # widget inits
        Label(
            _frame,
            text=_text,
            font=self.FONT1,
            background=self.BG_COLOR,
            foreground=self.FG_COLOR1,
        ).pack(expand=1, fill="x", padx=20)
        # info message inits
        try:
            # i18n support
            _text = _("Loading application, please wait...")
        except:
            # no support (raw)
            _text = "Loading application, please wait..."
        # end try
        # widget inits
        Label(
            _frame,
            text=_text,
            font=self.FONT2,
            background=self.BG_COLOR,
            foreground=self.FG_COLOR2,
        ).pack(expand=1, fill="x", padx=20, pady=10)
        # lay out widgets container
        _frame.pack()
    # end def


    def show (self, *args, **kw):
        """
            event handler: shows up current splash screen;
        """
        # show splash screen
        self.deiconify()
        # raise above all
        self.lift()
        # update display for more efficiency
        self.update()
    # end def

# end class SplashScreen
