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

    FALSE_VALUES = (None, 0, "", "0", "-", "no", "false", "na", "n/a")

    FIELD_NAMES = ("name", "male", "female", "origin", "description")

    SQL_IMPORT = """\
        INSERT OR IGNORE INTO 'character_names'
        VALUES (NULL, :name, :male, :female, :origin, :description)
    """

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


    def clean_up (self, fields, field_names):
        """
            resets @fields data row along with @field_names column
            names;
        """
        # inits
        _row = dict()
        # browse mandatory field names
        for _name in field_names:
            # reset value
            _row[_name] = fields.get(_name, "")
        # end for
        # return clean-ups
        return _row
    # end def


    def get_character_names (self, limit=50, offset=0, **criteria):
        """
            selects rows in table 'character_names' along with
            @criteria dictionary;
        """
        # inits
        _where = ""
        _matchup = {
            "s": "{}%", "e": "%{}", "x": "{}",
        }.get(criteria.pop("matchup", "")) or "%{}%"
        _query = _matchup.format(
            self.sanitize(criteria.pop("query", ""))
        )
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
                            "name_name like '{}'", _query
                        )
                    )
                # end if
                # into origin
                if _crit.get("origin"):
                    # reformat field
                    _criteria.append(
                        tools.str_complete(
                            "name_origin like '{}'", _query
                        )
                    )
                # end if
                # into description
                if _crit.get("description"):
                    # reformat field
                    _criteria.append(
                        tools.str_complete(
                            "name_description like '{}'", _query
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


    def get_int_boolean (self, value):
        """
            returns 1 if @value is evaluated to something True;
            returns 0 otherwise;
        """
        return int(bool(tools.ensure_int(value) != 0))
    # end def


    def import_character_name (self, **fields):
        """
            imports a new character name into database;
        """
        # param inits
        self.parse_gender(fields)
        # all mandatory fields *DO* exist by now (and *ONLY* them)
        _row = self.clean_up(fields, self.FIELD_NAMES)
        # value *MUST* be a plain string of chars
        if tools.is_pstr(_row["name"]):
            # inits
            _row["origin"] = _row["origin"].lower()
            _row["description"] = _row["description"].capitalize()
            # do SQL query
            self.sql_query(self.SQL_IMPORT, **_row)
        # no name to import
        else:
            # error
            raise ValueError(
                "cannot import character name without a given name. "
                "Expected plain string of chars for field 'name'."
            )
        # end if
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

            -- DROP TABLE IF EXISTS 'character_names';

            -- create table for character names

            CREATE TABLE IF NOT EXISTS 'character_names'
            (
                name_key            INTEGER PRIMARY KEY,
                name_name           TEXT NOT NULL,
                name_male           INTEGER NOT NULL DEFAULT 0,
                name_female         INTEGER NOT NULL DEFAULT 0,
                name_origin         TEXT NOT NULL,
                name_description    TEXT NOT NULL DEFAULT "",
                UNIQUE (name_name, name_origin)
            );

            CREATE TEMPORARY TABLE IF NOT EXISTS 'storyboard_shots'
            (
                shot_key            INTEGER PRIMARY KEY,
                shot_scene          INTEGER NOT NULL DEFAULT 0,
                shot_shot           INTEGER NOT NULL DEFAULT 0,
                shot_title          TEXT NOT NULL DEFAULT "",
                shot_text           TEXT NOT NULL DEFAULT "",
                UNIQUE (shot_scene, shot_shot)
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


    def parse_gender (self, row):
        """
            parses different values for 'gender' field name in @row;
            resets @row to match table columns constraints;
        """
        # inits
        row.setdefault("male", 0)
        row.setdefault("female", 0)
        # try to get 'gender' data
        _gender = str(row.pop("gender", "")).lower()
        # got male value?
        if _gender in ("m", "mf", "fm", "male", "both"):
            # inits
            row["male"] = 1
        # end if
        # got female value?
        if _gender in ("f", "mf", "fm", "female", "both"):
            # inits
            row["female"] = 1
        # end if
        # parse genuine values
        row["male"] = self.get_int_boolean(
            row["male"] not in self.FALSE_VALUES
        )
        row["female"] = self.get_int_boolean(
            row["female"] not in self.FALSE_VALUES
        )
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


    def stb_del_shot (self, scene, shot):
        """
            removes storyboard shot record;
        """
        print("DB: deleting shot #{}.{}".format(scene, shot))
        # SQL query
        self.sql_query(
            "DELETE FROM 'storyboard_shots' "
            "WHERE shot_scene = ? and shot_shot = ?",
            int(scene), int(shot)
        )
    # end def


    def stb_get_shot (self, scene, shot):
        """
            retrieves storyboard shot record;
        """
        # SQL query
        self.sql_query(
            "SELECT shot_text AS text FROM 'storyboard_shots' "
            "WHERE shot_scene = ? and shot_shot = ? LIMIT 1",
            int(scene), int(shot)
        )
        # get one row or default
        return self.fetch(default={"text": ""})
    # end def


    def stb_get_shot_list (self, scene):
        """
            retrieves storyboard shot list for given @scene;
        """
        # SQL query
        self.sql_query(
            "SELECT shot_shot AS shot, shot_title AS title "
            "FROM 'storyboard_shots' "
            "WHERE shot_scene = ? ORDER BY shot_shot",
            int(scene)
        )
        # get all rows or None
        return self.fetch(self.ALL, default=[])
    # end def


    def stb_update_shot (self, **row):
        """
            inserts or replaces storyboard shot record;
        """
        print("DB: updating shot #{scene}.{shot}".format(**row))
        # insert or replace
        self.sql_query(
            "INSERT OR REPLACE INTO 'storyboard_shots' "
            "VALUES (NULL, :scene, :shot, :title, :text)",
            **row
        )
    # end def

# end class AppDatabase
