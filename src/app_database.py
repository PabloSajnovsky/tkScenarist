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

            CREATE TEMPORARY TABLE IF NOT EXISTS 'resource_types'
            (
                type_key            INTEGER PRIMARY KEY,
                type_fk_parent      INTEGER NOT NULL DEFAULT 0,
                type_name           TEXT NOT NULL DEFAULT ""
            );

            CREATE TEMPORARY TABLE IF NOT EXISTS 'resource_items'
            (
                item_key            INTEGER PRIMARY KEY,
                item_fk_type        INTEGER NOT NULL DEFAULT 0,
                item_name           TEXT NOT NULL DEFAULT "",
                item_role           TEXT NOT NULL DEFAULT "",
                item_contact        TEXT NOT NULL DEFAULT "",
                item_phone          TEXT NOT NULL DEFAULT "",
                item_email          TEXT NOT NULL DEFAULT "",
                item_notes          TEXT NOT NULL DEFAULT ""
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


    def res_get_types (self, fk_parent=0):
        """
            retrieves {type_name: type_key} for a given type_fk_parent;
        """
        self.sql_query(
            "SELECT type_name, type_key FROM 'resource_types' "
            "WHERE type_fk_parent = ?",
            fk_parent
        )
        _rows = self.fetch(self.ALL)
    # end def


    def res_reset (self):
        """
            resets resource tables to default values;
        """
        self.sql_script("""
            DELETE FROM 'resource_types', 'resource_items';
            INSERT INTO 'resource_types' VALUES
                (1, 0, '1-Staff'),
                    (4, 1, '01-Producers'),
                        (5, 4, 'Executive producer'),
                        (6, 4, 'Film producer'),
                        (7, 4, 'Line producer'),
                        (8, 4, 'Production manager'),
                        (9, 4, 'Unit manager'),
                    (10, 1, '02-Directors'),
                        (11, 10, 'Art director'),
                        (12, 10, 'Director of Photography'),
                        (13, 10, 'Film author'),
                        (14, 10, 'Film maker'),
                        (15, 10, 'Stage director'),
                    (16, 1, '03-Actors'),
                        (17, 16, '1-Main role (male)'),
                        (18, 16, '2-Main role (female)'),
                        (19, 16, '3-Secundary #1'),
                        (20, 16, '4-Secundary #2'),
                        (21, 16, 'Extra #1'),
                        (22, 16, 'Extra #2'),
                        (23, 16, 'Extra #3'),
                    (24, 1, '04-Grip'),
                        (25, 24, '1-Key grip'),
                        (26, 24, '2-Best boy'),
                        (27, 24, '3-Dolly grip'),
                        (28, 24, 'Grip #1'),
                        (29, 24, 'Grip #2'),
                        (30, 24, 'Grip #3'),
                    (31, 1, '05-Lighting'),
                        (32, 31, '1-Gaffer'),
                        (33, 31, '2-Best boy'),
                        (34, 31, 'Technician #1'),
                        (35, 31, 'Technician #2'),
                        (36, 31, 'Technician #3'),
                    (37, 1, '06-Electrical'),
                        (38, 37, 'Electrician #1'),
                        (39, 37, 'Electrician #2'),
                        (40, 37, 'Electrician #3'),
                    (41, 1, '07-Production sound'),
                        (42, 41, '1-Production sound mixer'),
                        (43, 41, '2-Boom operator'),
                        (44, 41, '3-Utility sound technician'),
                    (45, 1, '08-Costume dept'),
                        (46, 45, '1-Costume designer'),
                        (47, 45, '2-Costume supervisor'),
                        (48, 45, '3-Key costumer'),
                        (49, 45, '4-Costume standby'),
                        (50, 45, 'Cutter #1'),
                        (51, 45, 'Cutter #2'),
                        (52, 45, 'Cutter #3'),
                    (53, 1, '09-Hair and make-up'),
                        (54, 53, '1-Key make-up artist'),
                        (55, 53, '2-Make-up supervisor'),
                        (56, 53, '3-Make-up artist'),
                        (57, 53, '4-Key hair'),
                        (58, 53, '5-Hair stylist'),
                    (59, 1, '10-Special effects'),
                        (60, 59, '1-SFX supervisor'),
                        (61, 59, 'SFX assistant #1'),
                        (62, 59, 'SFX assistant #2'),
                        (63, 59, 'SFX assistant #3'),
                    (64, 1, '11-Stunt team'),
                        (65, 64, '1-Stunt coordinator'),
                        (66, 64, 'Stuntman #1'),
                        (67, 64, 'Stuntman #2'),
                        (68, 64, 'Stuntman #3'),
                    (69, 1, '12-CG team'),
                        (70, 69, '1-CG supervisor'),
                        (71, 69, 'CG artist #1'),
                        (72, 69, 'CG artist #2'),
                        (73, 69, 'CG artist #3'),
                (2, 0, '2-Hardware'),
                    (74, 2, '01-Audio'),
                        (75, 74, 'Boom pole'),
                        (76, 74, 'Cables'),
                        (77, 74, 'Microphone'),
                        (78, 74, 'Mixer'),
                        (79, 74, 'Recorder'),
                    (80, 2, '02-Video'),
                        (81, 80, 'Camera'),
                        (82, 80, 'Crane'),
                        (83, 80, 'Dolly'),
                        (84, 80, 'Mount'),
                        (85, 80, 'Opticals'),
                        (86, 80, 'Steady'),
                    (87, 2, '03-Logistics'),
                        (88, 87, 'Autobus'),
                        (89, 87, 'Minibus'),
                        (90, 87, 'Personal car'),
                        (91, 87, 'Train'),
                        (92, 87, 'Truck'),
                (3, 0, '3-Events'),
                    (93, 3, '01-Casting'),
                        (94, 93, '1-Director'),
                        (95, 93, '2-Male #1'),
                        (96, 93, '2-Male #2'),
                        (97, 93, '2-Male #3'),
                        (98, 93, '3-Female #1'),
                        (99, 93, '3-Female #2'),
                        (100, 93, '3-Female #3'),
                        (101, 93, '4-Animal #1'),
                        (102, 93, '4-Animal #2'),
                        (103, 93, '4-Animal #3'),
                    (104, 3, '02-Meeting'),
                        (105, 104, 'Location #1'),
                        (106, 104, 'Location #2'),
                        (107, 104, 'Location #3'),
                        (108, 104, 'Location #4'),
                        (109, 104, 'Location #5'),
                    (110, 3, '03-Promotion'),
                        (111, 110, 'Location #1'),
                        (112, 110, 'Location #2'),
                        (113, 110, 'Location #3'),
                        (114, 110, 'Location #4'),
                        (115, 110, 'Location #5')
            ;
        """)
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


    def stb_clear_shots (self):
        """
            truncates table of storyboard shots;
        """
        # simply truncate table
        self.sql_query("DELETE FROM 'storyboard_shots'")
    # end def


    def stb_del_shot (self, scene, shot):
        """
            removes storyboard shot record;
        """
        # SQL query
        self.sql_query(
            "DELETE FROM 'storyboard_shots' "
            "WHERE shot_scene = ? and shot_shot = ?",
            int(scene), int(shot)
        )
    # end def


    def stb_get_all_shots (self):
        """
            retrieves all storyboard shots;
        """
        # SQL query
        self.sql_query(
            "SELECT * FROM 'storyboard_shots' "
            "ORDER BY shot_scene, shot_shot"
        )
        # get all rows or default
        return self.fetch(self.ALL, default=[])
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
        # get all rows or default
        return self.fetch(self.ALL, default=[])
    # end def


    def stb_import_shots (self, sequence):
        """
            imports shot rows from @sequence into DB table;
        """
        # truncate table
        self.stb_clear_shots()
        # import many rows
        self.cursor.executemany(
            "INSERT OR IGNORE INTO 'storyboard_shots' "
            "VALUES (NULL, :shot_scene, :shot_shot, "
            ":shot_title, :shot_text)",
            sequence
        )
        # commit new transaction
        self.commit()
    # end def


    def stb_purge_shots (self, scene):
        """
            removes storyboard empty shot records;
        """
        # SQL query
        self.sql_query(
            "DELETE FROM 'storyboard_shots' "
            "WHERE shot_scene = ? and shot_text = ''",
            int(scene)
        )
    # end def


    def stb_update_shot (self, **row):
        """
            inserts or replaces storyboard shot record;
        """
        # insert or replace
        self.sql_query(
            "INSERT OR REPLACE INTO 'storyboard_shots' "
            "VALUES (NULL, :scene, :shot, :title, :text)",
            **row
        )
    # end def

# end class AppDatabase
