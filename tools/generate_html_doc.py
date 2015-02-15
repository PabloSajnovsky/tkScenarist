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
import re
import os
import os.path as OP
from glob import glob

from markdown import markdown
from doc_templates import HTML5DocTemplate as html_doc


def normalize (fpath):
    return OP.normpath(OP.abspath(OP.realpath(OP.expanduser(fpath))))
# end def


def clean_fname (fname):
    return re.sub(r"\W+", "_", fname)
# end def


def github_to_md (text):
    """
        formats GitHub-specific MarkDown formats to standard MarkDown
        formats;
    """
    # inits
    text = str(text)
    # replace image src URL
    text = text.replace(
        "https://raw.githubusercontent.com/"
        "tarball69/tkScenarist/master/",
        "../../"
    )
    # reformat GH's links
    text = re.sub(r"\[\[(.*?)\|(.*?)\]\]", gh_links, text)
    text = re.sub(r"(\[.*?\])\s+(\(.*?\))", r"\1\2", text)
    # return formatted text
    return text
# end def


def gh_links (match_obj):
    """ treat it right!"""
    # init
    _link_text = match_obj.group(1)
    _link_href = match_obj.group(2).split("#")
    # got filename?
    if _link_href[0]:
        # ensure correct filename
        _link_href[0] = clean_fname(_link_href[0])
        # add file ext
        _link_href[0] += ".html"
    # end if
    # reset link href
    _link_href = "#".join(_link_href)
    # formatted
    return "[{t}]({h})".format(t=_link_text, h=_link_href)
# end def


# inits
ENCODING = "UTF-8"

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
            clean_fname(OP.basename(OP.splitext(_fsrc)[0])) + _htmlext
        )
    )
    # notify user
    print("converting:\n\t'{}'\n\t--> '{}'\n".format(_fsrc, _fdest))
    # get data
    # caution: this way works better than 'r+' mode /!\
    with open(_fsrc, "r", encoding=ENCODING) as _infile:
        # get file contents
        _text = _infile.read()
    # end with
    # make some updates
    _text = github_to_md(_text)
    # set data
    # caution: this way works better than 'r+' mode /!\
    with open(_fsrc, "w", encoding=ENCODING) as _outfile:
        # save changes
        _outfile.write(_text)
    # end with
    # convert markdown to HTML
    _DOM["body"] = markdown(_text, output_format=_doctype)
    # put data
    with open(_fdest, "w", encoding=ENCODING) as _outfile:
        _outfile.write(html_doc.format(**_DOM))
    # end with
# end for

# program end
print("Done. OK.")
