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

# doc templates

HTML5DocTemplate = """\
<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <link rel="stylesheet" type="text/css" href="../styles/common.css"/>
    </head>
    <body>
        <div id="page">
            <div id="title">
                {title}
            </div> <!-- id: title -->
            <div id="nav">
                [return to <a href="index.html">Homepage</a>]
            </div> <!-- id: nav -->
            <div id="contents">
                {body}
            </div> <!-- id: contents -->
            <div id="nav">
                [return to <a href="index.html">Homepage</a>]
            </div> <!-- id: nav -->
        </div> <!-- id: page -->
    </body>
</html>\
"""
