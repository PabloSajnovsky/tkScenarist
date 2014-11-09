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
import tkRAD.core.database as DB


# private module member
__database = None


def get_database (**kw):
    """
        retrieves app-wide unique instance;
    """
    global __database
    if not isinstance(__database, AppDatabase):
        __database = AppDatabase(**kw)
    # end if
    return __database
# end def


class AppDatabase (DB.Database):
    """
        SQLite database layer;
    """

    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # put your own code here
        self.sql_script("""
            /*
                tkScenarist application database
            */

            -- create table for character names

            CREATE TABLE IF NOT EXISTS 'character_names'
            (
                name_key            INTEGER PRIMARY KEY,
                name_name           NOT NULL,
                name_male           INTEGER NOT NULL DEFAULT 0,
                name_female         INTEGER NOT NULL DEFAULT 0,
                name_origin         NOT NULL
            );
        """)
    # end def


    def init_members (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # put your own code here
        pass
    # end def

# end class AppDatabase
