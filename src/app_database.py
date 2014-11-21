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
from tkRAD.core import tools


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

    # class constant defs
    SQL_NAMES = """\
        SELECT
            name_name AS Name,
            CASE name_male WHEN 1 THEN 'M' ELSE '' END ||
            CASE name_female WHEN 1 THEN 'F' ELSE '' END AS Gender,
            name_origin AS Origin,
            name_description AS Description
        FROM
            'character_names'
        {where}
        ORDER BY
            name_name ASC, name_origin ASC
        LIMIT
            {limit}
        OFFSET
            {offset}
    """


    def get_int_boolean (self, value):
        """
            returns 1 if @value is evaluated to something True;
            returns 0 otherwise;
        """
        return int(bool(tools.ensure_int(value) != 0))
    # end def


    def get_character_names (self, limit=50, offset=0, **criteria):
        """
            selects rows in table 'character_names' along with
            @criteria dictionary;
        """
        # inits
        _where = ""
        _query = self.sanitize(criteria.pop("query", ""))
        _crit = dict()
        # reset values
        for _field, _value in criteria.items():
            # reset
            _crit[_field] = self.get_int_boolean(criteria[_field])
        # end for
        # got criteria?
        if any(_crit.values()):
            # inits
            _criteria = list()
            # ----------------------- gender ---------------------------
            # selective gender?
            if not _crit.get("all"):
                # reformat field
                _criteria.append(
                    tools.str_complete(
                        "name_male = {}", str(_crit.get("male", ""))
                    )
                )
                # reformat field
                _criteria.append(
                    tools.str_complete(
                        "name_female = {}", str(_crit.get("female", ""))
                    )
                )
            # end if
            # -------------------- searching ---------------------------
            # got a query?
            if _query:
                # into name
                if _crit.get("name"):
                    # reformat field
                    _criteria.append(
                        tools.str_complete(
                            "name_name like '%{}%'", _query
                        )
                    )
                # end if
                # into origin
                if _crit.get("origin"):
                    # reformat field
                    _criteria.append(
                        tools.str_complete(
                            "name_origin like '%{}%'", _query
                        )
                    )
                # end if
                # into description
                if _crit.get("description"):
                    # reformat field
                    _criteria.append(
                        tools.str_complete(
                            "name_description like '%{}%'", _query
                        )
                    )
                # end if
            # end if
            # sanitize criteria
            _criteria = " AND ".join(tuple(filter(None, _criteria)))
            # set WHERE clause, if any
            _where = tools.str_complete("WHERE {}", _criteria)
        # end if
        # setup SQL query
        _sql = self.SQL_NAMES.format(
            where=_where, limit=limit, offset=offset
        )
        # try out
        try:
            # retrieve results
            self.sql_query(_sql)
            # fetch all rows
            return self.fetch(self.ALL)
        # failed
        except Exception as e:
            print("got an error:", e)
            return None
        # end try
    # end def


    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # put your own code here
        self.sql_script("""
            /*
                tkScenarist application database
            */

            -- this is for debugging session
            -- (comment this out in production state)

            DROP TABLE IF EXISTS 'character_names';

            -- create table for character names

            CREATE TABLE IF NOT EXISTS 'character_names'
            (
                name_key            INTEGER PRIMARY KEY,
                name_name           TEXT NOT NULL,
                name_male           INTEGER NOT NULL DEFAULT 0,
                name_female         INTEGER NOT NULL DEFAULT 0,
                name_origin         TEXT NOT NULL,
                name_description    TEXT NOT NULL DEFAULT ""
            );

            -- for testing session
            INSERT INTO 'character_names' VALUES
                (NULL, 'aaron', 1, 0, 'hebrew', 'qlsmdjfmqlskjdf'),
                (NULL, 'ibn''abdul', 1, 0, 'arab', 'qlsmd jfmqls kjdf'),
                (NULL, 'éloïse', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'michelle', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'camille', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'dominique', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'alf', 0, 0, 'alien', 'soucoupe violente'),
                (NULL, 'aaron', 1, 0, 'hebrew', 'qlsmdjfmqlskjdf'),
                (NULL, 'ibn''abdul', 1, 0, 'arab', 'qlsmd jfmqls kjdf'),
                (NULL, 'éloïse', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'michelle', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'camille', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'dominique', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'alf', 0, 0, 'alien', 'soucoupe violente'),
                (NULL, 'aaron', 1, 0, 'hebrew', 'qlsmdjfmqlskjdf'),
                (NULL, 'ibn''abdul', 1, 0, 'arab', 'qlsmd jfmqls kjdf'),
                (NULL, 'éloïse', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'michelle', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'camille', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'dominique', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'alf', 0, 0, 'alien', 'soucoupe violente'),
                (NULL, 'aaron', 1, 0, 'hebrew', 'qlsmdjfmqlskjdf'),
                (NULL, 'ibn''abdul', 1, 0, 'arab', 'qlsmd jfmqls kjdf'),
                (NULL, 'éloïse', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'michelle', 0, 1, 'french', 'mlqskjd f qmsldj fqsd'),
                (NULL, 'camille', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'dominique', 1, 1, 'french', 'qmlkjd  qsldjf qsdl k'),
                (NULL, 'alf', 0, 0, 'alien', 'soucoupe violente')
            ;
        """)
    # end def


    def init_members (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # put your own code here
        pass
    # end def


    def sanitize (self, value):
        """
            returns a quote-protected string;
        """
        # param controls
        if value:
            value = str(value).replace(r"\'", "'").replace("'", "''")
        # end if
        return value
    # end def

# end class AppDatabase
