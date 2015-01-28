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

# script for generating HTML documentation from markdown (.md) files
# located at ^/html/{LC_LANG}/md/*.md

# lib imports
import os
import os.path as OP
from glob import glob

from markdown import markdown
from doc_templates import HTML5DocTemplate as html_doc


def normalize (fpath):
    return OP.normpath(OP.abspath(OP.realpath(OP.expanduser(fpath))))
# end def


# file/dir inits
_wdir = normalize(OP.join(OP.dirname(__file__), "../html/"))
_mddir = "md"
_schdir = normalize(OP.join(_wdir, "*", _mddir))
_schfile = "*.md"
_schpattern = normalize(OP.join(_schdir, _schfile))

# HTML inits
_htmlext = ".html"
_doctype = "HTML5"
_DOM = {
    "title": "tkScenarist - screenwriting made simpler",
    "body": "",
}

# browse files
for _fsrc in glob(_schpattern):
    # destination file path init
    _fdest = normalize(
        OP.join(
            OP.dirname(_fsrc),
            "../",
            OP.basename(OP.splitext(_fsrc)[0]) + _htmlext
        )
    )
    # notify user
    print("converting:\n\t'{}'\n\t--> '{}'\n".format(_fsrc, _fdest))
    # get data
    with open(_fsrc) as _infile:
        _text = _infile.read()
    # end with
    # convert markdown to HTML
    _DOM["body"] = markdown(_text, output_format=_doctype)
    # put data
    with open(_fdest, "w") as _outfile:
        _outfile.write(html_doc.format(**_DOM))
    # end with
# end for

# program end
print("Done. OK.")
