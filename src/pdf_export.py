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
import os.path
import threading
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Frame
from reportlab.platypus import Paragraph, Spacer, PageBreak, Table
from reportlab.platypus.frames import ShowBoundaryValue
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import *                      # text alignments

import tkinter.constants as TK
import tkRAD.core.path as P
import tkRAD.core.services as SM
from tkRAD.core import tools


def build_document (doc):
    """
        builds final doc for specific PDF document;
    """
    # delegate to specific
    doc.build_document()
    # progression status (0-100%)
    return doc.progress
# end def


def build_elements (doc):
    """
        builds elements for specific PDF document;
    """
    # delegate to specific
    doc.build_elements()
    # progression status (0-100%)
    return doc.progress
# end def


def get_pdf_document (doc_name, **kw):
    """
        returns a new instance for an app-specific PDF document with
        filepath built along with @doc_name document name value;
    """
    # new document instance
    return eval(
        "PDFDocument{name}(doc_name, **kw)"
        .format(name=str(doc_name).title().replace("_", ""))
    )
# end def


def get_stylesheet ():
    """
        returns a dict of ParagraphStyle settings;
    """
    # inits
    _root_style = ParagraphStyle(
        "root_style",
        fontName="Courier",
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        leftIndent=0,
        rightIndent=0,
        spaceBefore=0,
        spaceAfter=0,
    )
    # stylesheet as Python dict()
    return {
        # main styles
        "header": ParagraphStyle(
            "header",
            parent=_root_style,
            fontName="Times-BoldItalic",
            fontSize=12,
            leading=12,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=_root_style,
            fontName="Times-Bold",
            fontSize=24,
            leading=26,
            underlineProportion=1,
            alignment=TA_CENTER,
            spaceAfter=0.3*inch,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=_root_style,
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=0.1*inch,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=_root_style,
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=0.1*inch,
        ),
        "body": ParagraphStyle(
            "body",
            parent=_root_style,
            fontName="Helvetica",
            alignment=TA_JUSTIFY,
            spaceAfter=0.1*inch,
            bulletIndent=0.1*inch,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=_root_style,
            fontName="Times-Italic",
            alignment=TA_CENTER,
        ),
        "footer_tiny": ParagraphStyle(
            "footer_tiny",
            parent=_root_style,
            fontName="Helvetica-Oblique",
            fontSize=6,
            leading=6,
            alignment=TA_CENTER,
        ),
        # table header
        "th": ParagraphStyle(
            "th",
            parent=_root_style,
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
            alignment=TA_CENTER,
        ),
        # table data
        "td": ParagraphStyle(
            "td",
            parent=_root_style,
            fontName="Helvetica",
            alignment=TA_JUSTIFY,
            spaceAfter=0.1*inch,
        ),

        # project data styles

        "title": ParagraphStyle(
            "title",
            fontName="Times-Bold",
            fontSize=36,
            leading=40,
            alignment=TA_CENTER,
            leftIndent=0.5*inch,
            rightIndent=0.5*inch,
            spaceBefore=0,
            spaceAfter=0.1*inch,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontName="Times-Italic",
            fontSize=18,
            leading=20,
            alignment=TA_CENTER,
            leftIndent=1*inch,
            rightIndent=1*inch,
            spaceBefore=0,
            spaceAfter=0.1*inch,
        ),
        "episode": ParagraphStyle(
            "episode",
            fontName="Helvetica",
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            leftIndent=1.5*inch,
            rightIndent=1.5*inch,
            spaceBefore=0,
            spaceAfter=0.1*inch,
        ),
        "author": ParagraphStyle(
            "author",
            fontName="Times-BoldItalic",
            fontSize=16,
            leading=18,
            alignment=TA_CENTER,
            leftIndent=1.5*inch,
            rightIndent=1.5*inch,
            spaceBefore=0.3*inch,
            spaceAfter=0.1*inch,
        ),
        "contact": ParagraphStyle(
            "contact",
            fontName="Times-Italic",
            fontSize=12,
            leading=12,
            alignment=TA_LEFT,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=0,
            spaceAfter=6,
        ),

        # characters tab styles

        "charname": ParagraphStyle(
            "charname",
            parent=_root_style,
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=0.3*inch,
            spaceAfter=0.1*inch,
            keepWithNext=True,
        ),
        "charlog": ParagraphStyle(
            "charlog",
            parent=_root_style,
            fontName="Helvetica",
            alignment=TA_JUSTIFY,
            leftIndent=0.1*inch,
            rightIndent=0.1*inch,
            spaceAfter=0.1*inch,
        ),

        # scenario tab styles

        "action": ParagraphStyle(
            "action",
            parent=_root_style,
            alignment=TA_JUSTIFY,
            spaceAfter=0.1*inch,
        ),
        "character": ParagraphStyle(
            "character",
            parent=_root_style,
            fontName="Courier-Bold",
            alignment=TA_CENTER,
            leftIndent=2*inch,
            rightIndent=2*inch,
            keepWithNext=True,
        ),
        "dialogue": ParagraphStyle(
            "dialogue",
            parent=_root_style,
            alignment=TA_JUSTIFY,
            leftIndent=1*inch,
            rightIndent=1*inch,
            spaceAfter=0.1*inch,
        ),
        "parenthetical": ParagraphStyle(
            "parenthetical",
            parent=_root_style,
            fontName="Courier-Oblique",
            alignment=TA_CENTER,
            leftIndent=1.5*inch,
            rightIndent=1.5*inch,
            keepWithNext=True,
        ),
        "scene": ParagraphStyle(
            "scene",
            parent=_root_style,
            fontName="Courier-Bold",
            backColor="#f0f0f0",
            spaceAfter=0.1*inch,
            keepWithNext=True,
        ),
        "transition": ParagraphStyle(
            "transition",
            parent=_root_style,
            alignment=TA_RIGHT,
            spaceAfter=0.1*inch,
        ),
        "stats": ParagraphStyle(
            "stats",
            parent=_root_style,
            fontName="Times",
            alignment=TA_LEFT,
            leftIndent=0.25*inch,
            spaceAfter=0.1*inch,
        ),

        # storyboard tab styles

        "shot_title": ParagraphStyle(
            "shot_title",
            parent=_root_style,
            fontName="Courier-Bold",
            backColor="#f0f0f0",
            spaceAfter=0.1*inch,
            keepWithNext=True,
        ),
        "shot_body": ParagraphStyle(
            "shot_body",
            parent=_root_style,
            alignment=TA_JUSTIFY,
            leftIndent=0.2*inch,
            rightIndent=0.2*inch,
            spaceAfter=0.1*inch,
        ),
    }
# end def



class PDFDocumentBase:
    """
        Base class for tkScenarist specific PDF documents to export;
    """

    # class constant defs
    FRAME_OPTIONS = {
        "leftPadding": 0, "rightPadding": 0,
        "topPadding": 0, "bottomPadding": 0,
        "showBoundary": 0,
    }


    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # member inits
        self.filepath = None
        self.doc_name = doc_name
        self.options = kw.get("options")
        self.project_data = kw.get("data")
        self.app = SM.ask_for("app") # application
        self.pfm = SM.ask_for("PFM") # Project File Management
        self.mainwindow = self.app.mainwindow
        self.mainframe = self.mainwindow.mainframe
        self.database = self.mainwindow.database
        self.document = self.get_pdf_document(doc_name)
        self.styles = get_stylesheet()
        self.elements = list()
        self.reset_progress(force_reset=True)
    # end def


    def _thread_build (self):
        """
            private method def;
            for internal use only;
            thread for building PDF document as it may take a (very)
            long time;
        """
        # build PDF document
        self.document.build(
            self.elements,
            onFirstPage=self.draw_first_page,
            onLaterPages=self.draw_pages,
        )
    # end def


    def add_pagebreak (self):
        """
            adds a PageBreak() object to elements;
        """
        # inits
        self.elements.append(PageBreak())
    # end def


    def add_paragraph (self, text, style, bulletText=None):
        """
            adds a Paragraph() object only if @text is a plain string
            of chars;
        """
        # ensure we have some text
        if tools.is_pstr(text):
            # add paragraph
            self.elements.append(Paragraph(text, style, bulletText))
        # end if
    # end def


    def build_document (self):
        """
            hook method to be reimplemented in subclass;
            builds final PDF document;
        """
        # reset progress
        self.reset_progress()
        # very first step (inits)
        if not self.step:
            # next step
            self.step = 1
            # incremental step
            self.index = 4700.0 / (1.0 + len(self.elements))
            # launch thread
            self._thread = threading.Thread(target=self._thread_build)
            self._thread.start()
        # all steps
        else:
            # simulate progression
            self.progress = min(99.0, self.progress + self.index)
            # thread ended?
            if not self._thread.is_alive():
                # procedure is complete
                self.progress = 100
                # destroy thread
                del self._thread
            # end if
        # end if
    # end def


    def build_elements (self):
        """
            hook method to be reimplemented in subclass;
            builds document internal elements;
        """
        # reset progress
        self.reset_progress()
        # first page elements
        self.set_first_page_elements()
        # put your own code in subclass
        for i in range(20):
            # dummy text
            self.add_paragraph("*** TEST ***", self.styles["body"])
        # end if
        # procedure is complete
        self.progress = 100
    # end def


    def draw_first_page (self, canvas, doc):
        """
            hook method to be reimplemented in subclass;
            draws fix elements (header, footer, etc) on page;
        """
        # save settings
        canvas.saveState()
        # reset sequence counters
        SeqNumberParagraph.reset()
        # inits
        _data = self.project_data
        _width, _height = doc.pagesize
        # doc inner margin width
        _margin_w = _width - doc.leftMargin - doc.rightMargin
        # set header
        _style = self.styles["header"]
        _frame_h = _style.fontSize + 4
        Frame(
            doc.leftMargin, _height - 0.75 * doc.topMargin,
            _margin_w, _frame_h, **self.FRAME_OPTIONS
        ).addFromList([Paragraph(self.fancy_name, _style)], canvas)
        # set contact frame
        _style = self.styles["contact"]
        _frame_h = _style.fontSize + _style.spaceAfter
        Frame(
            doc.leftMargin, doc.bottomMargin,
            _margin_w, _frame_h * 4 - _style.spaceAfter,
            showBoundary=ShowBoundaryValue(),
        ).addFromList(
            [
                Paragraph(_t.format(**_data), _style)
                for _t in (
                    _("Contact: {project_author}"),
                    _("E-mail: {project_author_email}"),
                    _("Phone: {project_author_phone}"),
                )
            ],
            canvas
        )
        # set footer + mentions
        _footer = self.styles["footer"]
        _mentions = self.styles["footer_tiny"]
        _frame_h = _footer.fontSize + _mentions.fontSize + 8
        Frame(
            doc.leftMargin, 0.5 * doc.bottomMargin,
            _margin_w, _frame_h, **self.FRAME_OPTIONS
        ).addFromList(
            [
                Paragraph(
                    _("Printed on {date}")
                    .format(date=datetime.today().strftime("%c")),
                    _footer
                ),
                Paragraph(
                    _(
                        "Document generated by {name} with "
                        "{pdflib} PDF toolkit"
                    ).format(**self.app.APP),
                    _mentions
                ),
            ],
            canvas
        )
        # restore settings
        canvas.restoreState()
    # end def


    def draw_pages (self, canvas, doc):
        """
            hook method to be reimplemented in subclass;
            draws fix elements (header, footer, etc) on page;
        """
        # save settings
        canvas.saveState()
        # inits
        _data = self.project_data
        _width, _height = doc.pagesize
        # doc inner margin width
        _margin_w = _width - doc.leftMargin - doc.rightMargin
        # set header
        _text = _data["project_title"].strip()
        _text = "{}{} - {}".format(
            _text[:60].strip(),
            len(_text) >= 60 and "..." or "",
            self.fancy_name
        )
        _style = self.styles["header"]
        _frame_h = _style.fontSize + 4
        Frame(
            doc.leftMargin, _height - 0.75 * doc.topMargin,
            _margin_w, _frame_h, **self.FRAME_OPTIONS
        ).addFromList([Paragraph(_text, _style)], canvas)
        # set footer
        _text = _("Page {number}").format(number=doc.page)
        _style = self.styles["footer"]
        _frame_h = _style.fontSize + 4
        Frame(
            doc.leftMargin, 0.5 * doc.bottomMargin,
            _margin_w, _frame_h, **self.FRAME_OPTIONS
        ).addFromList([Paragraph(_text, _style)], canvas)
        # restore settings
        canvas.restoreState()
    # end def


    @property
    def fancy_name (self):
        """
            property attribute;
            returns a fancier name for self.doc_name;
            this is a READ-ONLY property;
        """
        return _(str(self.doc_name).title().replace("_", "/"))
    # end def


    def get_pdf_document (self, doc_name):
        """
            provides a reportlab.PDFDocument;
        """
        # param controls
        if tools.is_pstr(doc_name):
            # inits
            _data = self.project_data
            _fpath, _fext = os.path.splitext(self.pfm.project_path)
            # rebuild filepath
            self.filepath = P.normalize(
                "{}-{}.pdf".format(_fpath, doc_name)
            )
            # PDF document instance
            return SimpleDocTemplate(
                filename=self.filepath,
                author=_data.get("project_author"),
                title="{project_title} - "
                "{project_subtitle} - "
                "{project_episode}"
                .format(**_data),
                subject=self.fancy_name,
                creator=self.app.APP.get("title"),
                # debugging
                showBoundary=0,
            )
        # error
        else:
            # notify
            raise ValueError(
                "parameter 'doc_name' must be of "
                "plain string type."
            )
        # end if
    # end def


    @property
    def progress (self):
        """
            property attribute;
            progression status (0.0-100.0%);
        """
        return self.__progress
    # end def

    @progress.setter
    def progress (self, value):
        # inits
        self.__progress = float(min(100, max(0, value)))
    # end def

    @progress.deleter
    def progress (self):
        # delete
        del self.__progress
    # end def


    def reset_progress (self, force_reset=False):
        """
            resets progress status to 0 if >= 100 (%);
        """
        # forced or reached 100%?
        if force_reset or self.progress >= 100:
            # reset all
            self.progress = 0
            self.index = 0
            self.step = 0
            self.read_bytes = 0
            self.total_bytes = 0
        # end if
    # end def


    def set_first_page_elements (self):
        """
            sets document's first page flowable elements such as title,
            subtitle, episode, etc;
        """
        # inits
        _data = self.project_data
        _styles = self.styles
        # reset elements
        self.elements.clear()
        # add spacer
        self.elements.append(Spacer(0, 2*inch))
        # add paragraphs
        self.add_paragraph(
            _data.get("project_title"), _styles["title"]
        )
        self.add_paragraph(
            _data.get("project_subtitle"), _styles["subtitle"]
        )
        self.add_paragraph(
            _data.get("project_episode"), _styles["episode"]
        )
        self.add_paragraph(
            tools.str_complete(
                _("By {}"),
                _data.get("project_author")
            ),
            _styles["author"]
        )
        # add page break
        self.add_pagebreak()
    # end def

# end class PDFDocumentBase



class PDFDocumentBaseText (PDFDocumentBase):
    """
        base PDF document for tkinter.Text widget contents;
    """

    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(doc_name, **kw)
        # additional member inits
        self.init_document(**kw)
    # end def


    def build_elements (self):
        """
            hook method to be reimplemented in subclass;
            builds document internal elements;
        """
        # reset progress
        self.reset_progress()
        # very first step (inits)
        if not self.step:
            # init elements list
            self.init_elements()
        # next steps
        else:
            # do steps
            self.do_steps()
        # end if
    # end def


    def do_steps (self):
        """
            executes elements building step by step;
            this is one step at a time;
        """
        # get text block
        _text = self.wtext.get(self.index, self.index + 100.0)
        # update index
        self.index += 100.0
        # update consumed bytes
        self.read_bytes += len(_text)
        # evaluate progress
        self.progress = min(
            99.0, 100.0 * self.read_bytes / self.total_bytes
        )
        # no more text?
        if not _text:
            # procedure is complete
            self.progress = 100
        # got text
        else:
            # browse collection
            for _p in _text.split("\n"):
                # add new paragraph
                self.add_paragraph(_p, self.styles["body"])
            # end for
        # end if
    # end def


    def estimate_text_size (self):
        """
            tries to estimate text size without loading text contents;
        """
        # estimate size of text without loading text contents
        _paragraphs = float(self.wtext.index(TK.END))
        # not so much?
        if _paragraphs < 3000:
            # get real size
            self.total_bytes = len(self.wtext.get("1.0", TK.END))
        # spare time
        else:
            # estimate 1 paragraph is about 360 chars
            self.total_bytes = _paragraphs * 360
        # end if
        # ensure it is > 0
        self.total_bytes = max(1, self.total_bytes)
    # end def


    def init_document (self, **kw):
        """
            hook method to be reimplemented in subclass;
            additional member and document inits;
        """
        # put your own code in subclass
        pass
        # member inits
        self.wtext = None       # tkinter.Text widget to redefine here
    # end def


    def init_elements (self):
        """
            inits elements list;
        """
        # force reset all
        self.reset_progress(force_reset=True)
        # next step
        self.step = 1
        self.index = 1.0
        # estimate text size
        self.estimate_text_size()
        # first page elements
        self.set_first_page_elements()
    # end def

# end class PDFDocumentBaseText



class PDFDocumentCharacters (PDFDocumentBase):
    """
        specific PDF document class for Characters application tab;
    """

    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(doc_name, **kw)
        # additional member inits
        _tab = self.mainframe.tab_characters
        _canvas = _tab.CANVAS
        self.character_logs = _tab.character_logs
        self.character_names = _canvas.character_names
        self.relationships = _canvas.get_named_relationships()
    # end def


    def build_elements (self):
        """
            hook method to be reimplemented in subclass;
            builds document internal elements;
        """
        # reset progress
        self.reset_progress()
        # switch to step method
        exec("self.do_step_{}()".format(self.step))
    # end def


    def do_step_0 (self):
        """
            elements building process step;
            for internal use only;
        """
        # force reset all
        self.reset_progress(force_reset=True)
        # sorted list of character names
        self.sorted_names = sorted(self.character_logs)
        self.index = 0
        # first page elements
        self.set_first_page_elements()
        # next step
        self.step += 1
    # end def


    def do_step_1 (self):
        """
            elements building process step;
            for internal use only;
        """
        # got character names?
        if self.character_logs:
            # add little stats
            self.add_paragraph(_("Statistics"), self.styles["h2"])
            self.add_paragraph(
                _("Known character names: {name_count}")
                .format(name_count=len(self.character_logs)),
                self.styles["body"]
            )
            # next step
            self.step += 1
        # nothing to dump
        else:
            # procedure is complete
            self.progress = 100
        # end if
    # end def


    def do_step_2 (self):
        """
            elements building process step;
            for internal use only;
        """
        # try out
        try:
            # get character name
            _name = self.sorted_names[self.index]
            # character name as paragraph heading
            self.add_paragraph(_name, self.styles["charname"])
            # inits
            _log = self.character_logs[_name].strip()
            # got history log?
            if _log:
                # character history log as body text
                for _p in _log.split("\n"):
                    self.add_paragraph(_p, self.styles["charlog"])
                # end for
            # no history log
            else:
                # notify
                self.add_paragraph(
                    "<i>{}</i>".format(_("(no history log)")),
                    self.styles["charlog"]
                )
            # end if
            # update progression
            self.progress = 50.0 * self.index / len(self.sorted_names)
            # next index
            self.index += 1
        # end of list
        except:
            # procedure is half complete
            self.progress = 50
            # next step
            self.step += 1
        # end try
    # end def


    def do_step_3 (self):
        """
            elements building process step;
            for internal use only;
        """
        # no relationships to dump out?
        if not self.relationships:
            # procedure is complete
            self.progress = 100
            # stop right now
            return
        # end if
        # new page
        self.add_pagebreak()
        # page title
        self.add_paragraph(_("Relationships"), self.styles["h1"])
        # inits
        _count = len(self.relationships)
        # add little stats
        self.add_paragraph(_("Statistics"), self.styles["h2"])
        self.add_paragraph(
            _("Known distinct mutual relationships: {dmr}")
            .format(dmr=_count),
            self.styles["body"]
        )
        self.add_paragraph(
            _("Listed relationships: {list_count}")
            .format(list_count=_count*2),
            self.styles["body"]
        )
        self.add_paragraph(_("Relationships"), self.styles["h2"])
        # table rows
        self.table_rows = []
        # set headers
        self.table_rows.append(
            (
                Paragraph(_("Name"), self.styles["th"]),
                Paragraph(_("Name"), self.styles["th"]),
                Paragraph(_("Relationship"), self.styles["th"]),
            )
        )
        # reset list of character names
        self.sorted_names = sorted(self.character_names)
        self.index = 0
        # next step
        self.step += 1
    # end def


    def do_step_4 (self):
        """
            elements building process step;
            for internal use only;
        """
        # try out
        try:
            # inits
            _td = self.styles["td"]
            # get character name
            _name = self.sorted_names[self.index]
            # related dict
            _relationships = self.get_relationships_for(_name)
            # browse relationships
            for _name2 in sorted(_relationships):
                # add table row
                self.table_rows.append(
                    (
                        Paragraph(_name, _td),
                        Paragraph(_name2, _td),
                        Paragraph(_relationships[_name2], _td),
                    )
                )
            # end for
            # update progression
            self.progress = min(
                99.0,
                50.0 * (1.0 + self.index / len(self.sorted_names))
            )
            # next index
            self.index += 1
        # end of list
        except:
            # inits
            _style = [
                ("BOX", (0, 0), (-1, -1), 0.2, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
            # add table
            self.elements.append(
                Table(self.table_rows, repeatRows=1, style=_style)
            )
            # procedure is complete
            self.progress = 100
        # end try
    # end def


    def get_relationships_for (self, character_name):
        """
            returns a Python dict() of {name:relationship_text}
            matching @character_name parameter value;
        """
        # inits
        _dict = dict()
        # browse relationships
        for _group in self.relationships:
            # group contains searched character name?
            if _group["name0"] == character_name:
                # add to dict
                _dict[_group["name1"]] = _group["text"]
            elif _group["name1"] == character_name:
                # add to dict
                _dict[_group["name0"]] = _group["text"]
            # end if
        # end for
        # return relationships dict
        return _dict
    # end def

# end class PDFDocumentCharacters



class PDFDocumentDraftNotes (PDFDocumentBaseText):
    """
        specific PDF document class for Draft/Notes application tab;
    """

    def init_document (self, **kw):
        """
            hook method to be reimplemented in subclass;
            additional member and document inits;
        """
        # additional member inits
        self.wtext = self.mainframe.tab_draft_notes.text_draft_notes
    # end def

# end class PDFDocumentDraftNotes



class PDFDocumentPitchConcept (PDFDocumentBaseText):
    """
        specific PDF document class for Pitch/Concept application tab;
    """

    def init_document (self, **kw):
        """
            hook method to be reimplemented in subclass;
            additional member and document inits;
        """
        # additional member inits
        self.wtext = self.mainframe.tab_pitch_concept.text_pitch_concept
    # end def

# end class PDFDocumentPitchConcept



class PDFDocumentResources (PDFDocumentBase):
    """
        specific PDF document class for Resources application tab;
    """

    # class constant defs
    ITEM_FIELDNAMES = (
        "name", "role", "contact", "phone", "email", "notes"
    )


    def add_item_data (self, fk_type):
        """
            adds item data as unordered list;
            for internal use only;
        """
        # get item data
        _row = self.database.res_get_item(fk_type)
        # got data?
        if _row:
            # must get ordered this way
            for _key in self.ITEM_FIELDNAMES:
                # inits
                _value = _row[_key]
                # got value?
                if _value:
                    # unordered list
                    self.add_paragraph(
                        _("{key}: {value}")
                        .format(
                            key=_(_key.capitalize()), value=_value
                        ),
                        self.styles["body"],
                        bulletText="\u2022",
                    )
                # end if
            # end for
        # no data
        else:
            # tell it
            self.notify_no_data(0)
        # end if
    # end def


    def add_item_datebars (self, fk_type):
        """
            adds item availability dates as table;
            for internal use only;
        """
        # get item data
        _rows = self.database.res_get_datebars([fk_type])
        # got data?
        if _rows:
            # inits
            _table_rows = [
                # table headers
                (
                    Paragraph(_("Date begin"), self.styles["th"]),
                    Paragraph(_("Date end"), self.styles["th"]),
                    Paragraph(_("Availability"), self.styles["th"]),
                ),
            ]
            _td = self.styles["td"]
            # browse dates
            for _row in _rows:
                # add table data
                _table_rows.append(
                    (
                        Paragraph(
                            self.convert_iso_date(_row["date_begin"]),
                            _td
                        ),
                        Paragraph(
                            self.convert_iso_date(_row["date_end"]),
                            _td
                        ),
                        Paragraph(
                            _("Available")
                            if _row["status"].upper() == "OK"
                            else _("NOT available"),
                            _td
                        ),
                    )
                )
            # end for
            # inits
            _style = [
                ("BOX", (0, 0), (-1, -1), 0.2, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
            _table = Table(_table_rows, repeatRows=1, style=_style)
            # forgotten angels?
            _table.spaceBefore = 0.2*inch
            _table.spaceAfter = 0.2*inch
            # add table
            self.elements.append(_table)
        # end if
    # end def


    def build_elements (self):
        """
            hook method to be reimplemented in subclass;
            builds document internal elements;
        """
        # reset progress
        self.reset_progress()
        # switch to step method
        exec("self.do_step_{}()".format(self.step))
    # end def


    def convert_iso_date (self, date_str):
        """
            tries to convert an ISO 8601 'YYYY-MM-DD' formatted string
            to locale date representation format; returns formatted
            string on success, raises error otherwise;
        """
        # inits
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%A %x")
    # end def


    def do_step_0 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 0: document inits
        #
        # force reset all
        self.reset_progress(force_reset=True)
        # get resource sections (dict)
        self.sections = self.database.res_get_types()
        self.sections_sorted = sorted(self.sections)
        self.total_sections = len(self.sections)
        # init index
        self.index = 0
        # first page elements
        self.set_first_page_elements()
        # next step
        self.step += 1
    # end def


    def do_step_1 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 1: consuming one entire section
        #
        # try out
        try:
            # get section
            _section = self.sections_sorted.pop(0)
        # no more section
        except:
            # no data for this? tell it!
            self.notify_no_data(self.total_sections)
            # procedure is complete
            self.progress = 100
        # go on trying
        else:
            # update progress
            self.progress = min(
                99.0, 100.0 * self.index / self.total_sections
            )
            # update index
            self.index += 1
            # add paragraph
            self.add_paragraph(_section, self.styles["h1"])
            # subsection inits
            self.subsections = self.database.res_get_types(
                self.sections[_section]
            )
            self.subsections_sorted = sorted(self.subsections)
            self.total_subsections = len(self.subsections)
            # next step
            self.step += 1
        # end try
    # end def


    def do_step_2 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 2: consuming one entire subsection
        #
        # try out
        try:
            # get subsection
            _subsection = self.subsections_sorted.pop(0)
        # no more subsection
        except:
            # no data for this? tell it!
            self.notify_no_data(self.total_subsections)
            # add page break for next section
            self.add_pagebreak()
            # step 1: next section
            self.step = 1
        # go on trying
        else:
            # update progress
            self.progress = min(
                99.0,
                self.progress +
                100.0 / (self.total_sections * self.total_subsections)
            )
            # add paragraph
            self.add_paragraph(_subsection, self.styles["h2"])
            # items inits
            self.items = self.database.res_get_types(
                self.subsections[_subsection]
            )
            self.items_sorted = sorted(self.items)
            self.total_items = len(self.items)
            # next step
            self.step += 1
        # end try
    # end def


    def do_step_3 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 3: consuming one item at a time
        #
        # try out
        try:
            # get item
            _item = self.items_sorted.pop(0)
        # no more item
        except:
            # no data for this? tell it!
            self.notify_no_data(self.total_items)
            # step 2: next subsection
            self.step = 2
        # go on trying
        else:
            # inits
            _key = self.items[_item]
            # add paragraph
            self.add_paragraph(_item, self.styles["h3"])
            # add item data
            self.add_item_data(_key)
            # add item availability dates
            self.add_item_datebars(_key)
        # end try
    # end def


    def notify_no_data (self, count):
        """
            for internal use only;
            notifies if there is no data;
        """
        if not count:
            self.add_paragraph(
                "<i>{}</i>".format(_("(no data)")),
                self.styles["body"]
            )
        # end if
    # end def

# end class PDFDocumentResources



class PDFDocumentScenario (PDFDocumentBaseText):
    """
        specific PDF document class for Scenario application tab;
    """

    def add_stats_elements (self):
        """
            adds statistics to document as appendix;
        """
        # inits
        _s = self.stats
        _ds = self.styles["stats"]
        _elements = (
            (_("Statistics"), "h1"),
            (_("Document"), "h2"),
            (PageNumber(_("Pages: {field}"), _ds), "*"),
            (_("Paragraphs: {paragraph_count}").format(**_s), ""),
            (_("Words: {word_count}").format(**_s), ""),
            (_("Glyphs (letters/signs): {byte_count}").format(**_s), ""),
            (_("Scenario"), "h2"),
            (PageNumber(_("Pages: {field}"), _ds, adjust=-2), "*"),
            (_("Scenes: {scene_count}").format(**_s), ""),
            (_("Dialogues: {dialogue_count}").format(**_s), ""),
            (_("Transitions: {transition_count}").format(**_s), ""),
            (_("Movie"), "h2"),
            (
                _("Movie protagonists: {char_count}")
                .format(char_count=len(_s["movie_chars"])),
                ""
            ),
            (
                PageNumber(
                    _("Estimated movie duration: {field}"),
                    _ds, adjust=-2, formatter=self.get_duration,
                ),
                "*"
            ),
            #~ (_("").format(), ""),
        )
        # new page
        self.add_pagebreak()
        # loop on collection
        for (_p, _s) in _elements:
            # special paragraph?
            if _s == "*":
                # add special
                self.elements.append(_p)
            # default paragraph
            else:
                # add paragraph
                self.add_paragraph(_p, self.styles[_s or "stats"])
            # end if
        # end for
    # end def


    def do_steps (self):
        """
            executes elements building step by step;
            this is one step at a time;
            inherited from PDFDocumentBaseText;
        """
        # get tagged text block
        _tagged_text = self.wtext.get_tagged_text(
            self.index, self.index + 100.0
        )
        _only_texts = _tagged_text[::2]
        _only_tags = _tagged_text[1::2]
        # update index
        self.index += 100.0
        # update consumed bytes
        _bytes = sum(map(len, _only_texts))
        self.read_bytes += _bytes
        # evaluate progress
        self.progress = min(
            99.0, 100.0 * self.read_bytes / self.total_bytes
        )
        # no more text?
        if not _bytes:
            # add stats as appendix
            self.add_stats_elements()
            # procedure is complete
            self.progress = 100
        # got text
        else:
            # inits
            _print_left = self.options.get("print_scene_left")
            _print_right = self.options.get("print_scene_right")
            # browse collection
            for _index, _text in enumerate(_only_texts):
                # inits
                _text = _text.strip()
                try:
                    # get style from tags
                    _style = self.styles[_only_tags[_index][0]]
                except:
                    # default style
                    _style = self.styles["body"]
                # end try
                # browse lines in text
                for _line in _text.split("\n"):
                    # do some clean-ups
                    _line = _line.strip()
                    # got line?
                    if _line:
                        # specific flowable for scenes
                        if _style.name == "scene":
                            # add special paragraph
                            self.elements.append(
                                SeqNumberParagraph(
                                    _line, _style,
                                    print_left=_print_left,
                                    print_right=_print_right,
                                )
                            )
                        # default flowable
                        else:
                            # add new paragraph
                            self.add_paragraph(_line, _style)
                        # end if
                    # end if
                    # update statistics
                    self.update_stats(_line, _style.name)
                # end for
            # end for
        # end if
    # end def


    def get_duration (self, duration):
        """
            returns a formatted string for a given movie @duration
            (input value in minutes);
        """
        return _(
            "{hours:02d} h {minutes:02d} min"
        ).format(
            hours=(duration // 60), minutes=(duration % 60)
        )
    # end def


    def init_document (self, **kw):
        """
            hook method to be reimplemented in subclass;
            additional member and document inits;
        """
        # additional member inits
        self.wtext = self.mainframe.tab_scenario.TEXT
        self.stats = dict()
    # end def


    def init_elements (self):
        """
            inits elements list;
        """
        # super class inits
        super().init_elements()
        # reset stats
        self.stats.clear()
    # end def


    def update_stats (self, text, tag):
        """
            for internal use only;
            updates document stats in order to show them off as
            appendix;
        """
        # inits
        _s = self.stats
        # nb of paragraphs
        _s["paragraph_count"] = (
            _s.setdefault("paragraph_count", 0) + 1
        )
        # nb of words
        _s["word_count"] = (
            _s.setdefault("word_count", 0)
            + ((text or 0) and (text.count(" ") + 1))
        )
        # nb of bytes
        _s["byte_count"] = (
            _s.setdefault("byte_count", 0) + len(text)
        )
        # nb of scenes
        _s["scene_count"] = (
            _s.setdefault("scene_count", 0) + int(tag == "scene")
        )
        # nb of dialogues
        _s["dialogue_count"] = (
            _s.setdefault("dialogue_count", 0) + int(tag == "dialogue")
        )
        # nb of transitions
        _s["transition_count"] = (
            _s.setdefault("transition_count", 0)
            + int(tag == "transition")
        )
        # inits
        _s["movie_chars"] = _s.setdefault("movie_chars", set())
        # nb of movie characters
        if tag == "character":
            # add character name
            _s["movie_chars"].add(text)
        # end if
    # end def

# end class PDFDocumentScenario



class PDFDocumentStoryboard (PDFDocumentBase):
    """
        specific PDF document class for Storyboard application tab;
    """

    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(doc_name, **kw)
        # additional member inits
        self.scenario = self.mainframe.tab_scenario
        self.storyboard = self.mainframe.tab_storyboard
        self.wtext = self.scenario.TEXT
        self.stats = dict()
    # end def


    def build_elements (self):
        """
            hook method to be reimplemented in subclass;
            builds document internal elements;
        """
        # reset progress
        self.reset_progress()
        # switch to step method
        exec("self.do_step_{}()".format(self.step))
    # end def


    def do_step_0 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 0: document inits
        #
        # force reset all
        self.reset_progress(force_reset=True)
        # reset stats
        self.stats.clear()
        # get scene line numbers
        self.scene_lines = self.scenario.LISTBOX.current_lines
        # get scene IDs
        self.scene_ids = self.storyboard.LBOX_SCENE.line_ids
        # get nb of scenes
        self.total_scenes = len(self.scene_lines)
        # reset index
        self.index = 0
        # first page elements
        self.set_first_page_elements()
        # next step
        self.step += 1
    # end def


    def do_step_1 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 1: ensure current scene has shots
        #
        # try out
        try:
            # get shots for current scene number
            self.scene_shots = self.database.stb_get_scene_shots(
                self.scene_ids[self.index]
            )
        except:
            # index out of range
            self.scene_shots = None
        else:
            # update progress
            self.progress = min(
                99.0, 100.0 * (self.index + 1) / self.total_scenes
            )
        # end try
        # no shots for this scene?
        if not self.scene_shots:
            # go next scene
            self.index += 1
            # no more scene?
            if self.index >= self.total_scenes:
                # got stats to print?
                if self.stats.get("byte_count"):
                    # go to step 4: print stats
                    self.step = 4
                # no stats
                else:
                    # procedure is complete
                    self.progress = 100
                # end if
            # end if
        # got scene shots to print
        else:
            # update stats
            _len_shots = len(self.scene_shots)
            self.stats["min_shot"] = min(
                self.stats.setdefault("min_shot", _len_shots),
                _len_shots
            )
            self.stats["max_shot"] = max(
                self.stats.setdefault("max_shot", 0), _len_shots
            )
            # next step: print scene preview
            self.step += 1
        # end if
    # end def


    def do_step_2 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 2: print current scene's preview
        #
        # try out
        try:
            # get scene line number (tkinter.Text.index)
            _start = float(self.scene_lines[self.index])
        # no more scene
        except:
            # procedure is complete
            self.progress = 100
        # go on trying
        else:
            # get next scene line number (tkinter.Text.index)
            try:
                _end = float(self.scene_lines[self.index + 1])
            except:
                _end = TK.END
            # end try
            # get tagged text block for entire scene
            _tagged_text = self.wtext.get_tagged_text(_start, _end)
            _only_texts = _tagged_text[::2]
            _only_tags = _tagged_text[1::2]
            # add page break for scene numbers > 1
            if self.index:
                self.add_pagebreak()
            # end if
            # add some text
            self.add_paragraph(_("Scene preview"), self.styles["h2"])
            # printing options
            _print_left = self.options.get("print_shot_left")
            _print_right = self.options.get("print_shot_right")
            # browse collection
            for _index, _text in enumerate(_only_texts):
                # inits
                _text = _text.strip()
                try:
                    # get style from tags
                    _style = self.styles[_only_tags[_index][0]]
                except:
                    # default style
                    _style = self.styles["body"]
                # end try
                # browse lines in text
                for _line in _text.split("\n"):
                    # do some clean-ups
                    _line = _line.strip()
                    # specific flowable for scenes
                    if _style.name == "scene":
                        # add special paragraph
                        self.elements.append(
                            SeqNumberParagraph(
                                _line, _style,
                                print_left=_print_left,
                                print_right=_print_right,
                            )
                        )
                    # default flowable
                    else:
                        # add new paragraph
                        self.add_paragraph(_line, _style)
                    # end if
                    # update stats
                    self.update_stats(_line, _style.name)
                # end for
            # end for
            # add some text
            self.add_paragraph(_("Scene shots"), self.styles["h2"])
            # go next step: print scene shots
            self.step += 1
        # end try
    # end def


    def do_step_3 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 3: print all current scene shots
        #
        # try out
        try:
            # next shot
            _row = self.scene_shots.pop(0)
        # no more shot
        except:
            # next scene
            self.index += 1
            # return to step 1
            self.step = 1
        # keep on trying
        else:
            # shot title
            self.elements.append(
                SeqNumberParagraph(
                    _row["title"], self.styles["shot_title"],
                    print_left=self.options.get("print_shot_left"),
                    print_right=self.options.get("print_shot_right"),
                    use_subcounter=True,
                )
            )
            # update stats
            self.update_stats(_row["title"], "shot_title")
            # shot text
            for _line in _row["text"].strip().split("\n"):
                self.add_paragraph(_line, self.styles["shot_body"])
                # update stats
                self.update_stats(_line, "shot_body")
            # end for
        # end try
    # end def


    def do_step_4 (self):
        """
            elements building process step;
            for internal use only;
        """
        #
        # step 4: print document stats
        #
        # inits
        _s = self.stats
        _elements = (
            (_("Statistics"), "h1"),
            (_("Document"), "h2"),
            (
                PageNumber(_("Pages: {field}"), self.styles["stats"]),
                "*"
            ),
            (_("Paragraphs: {paragraph_count}").format(**_s), ""),
            (_("Words: {word_count}").format(**_s), ""),
            (
                _("Glyphs (letters/signs): {byte_count}").format(**_s),
                ""
            ),
            (_("Scenario"), "h2"),
            (_("Scenes with shots: {scene_count}").format(**_s), ""),
            (_("Dialogues: {dialogue_count}").format(**_s), ""),
            (_("Transitions: {transition_count}").format(**_s), ""),
            (_("Storyboard"), "h2"),
            (_("Total shots: {shot_count}").format(**_s), ""),
            (
                _("Average number of shots per scene: {:01.3f}")
                .format(
                    _s["shot_count"] / _s["scene_count"]
                    if _s["scene_count"] else 0.0
                ),
                ""
            ),
            (_("Min. shots per scene: {min_shot}").format(**_s), ""),
            (_("Max. shots per scene: {max_shot}").format(**_s), ""),
            #~ (_("").format(), ""),
        )
        # new page
        self.add_pagebreak()
        # loop on collection
        for (_p, _s) in _elements:
            # special paragraph?
            if _s == "*":
                # add special
                self.elements.append(_p)
            # default paragraph
            else:
                # add paragraph
                self.add_paragraph(_p, self.styles[_s or "stats"])
            # end if
        # end for
        # procedure is complete
        self.progress = 100
    # end def


    def update_stats (self, text, tag):
        """
            for internal use only;
            updates document stats in order to show them off as
            appendix;
        """
        # inits
        _s = self.stats
        # nb of paragraphs
        _s["paragraph_count"] = (
            _s.setdefault("paragraph_count", 0) + 1
        )
        # nb of words
        _s["word_count"] = (
            _s.setdefault("word_count", 0)
            + ((text or 0) and (text.count(" ") + 1))
        )
        # nb of bytes
        _s["byte_count"] = (
            _s.setdefault("byte_count", 0) + len(text)
        )
        # nb of scenes
        _s["scene_count"] = (
            _s.setdefault("scene_count", 0) + int(tag == "scene")
        )
        # nb of dialogues
        _s["dialogue_count"] = (
            _s.setdefault("dialogue_count", 0) + int(tag == "dialogue")
        )
        # nb of transitions
        _s["transition_count"] = (
            _s.setdefault("transition_count", 0)
            + int(tag == "transition")
        )
        # nb of scene shots
        _s["shot_count"] = (
            _s.setdefault("shot_count", 0) + int(tag == "shot_title")
        )
    # end def

# end class PDFDocumentStoryboard



class PageNumber (Paragraph):
    """
        Special flowable paragraph with PageNumber feature while
        drawing;
    """

    def __init__(self, text, style, bulletText=None, frags=None,
    caseSensitive=1, encoding='utf8', adjust=0, formatter=None):
        """
            class constructor;
        """
        # member inits
        self.field_adjust = adjust
        self.field_formatter = formatter
        # super class inits
        super().__init__(
            text, style, bulletText, frags, caseSensitive, encoding
        )
    # end def


    def draw (self):
        """
            subclass override;
            refer to reportlab/platypus/paragraph.py
            for more detail;
        """
        # inits
        _field = "{field}"
        _formatter = self.field_formatter or (lambda t:str(t))
        # browse collection
        for _i, _line in enumerate(self.blPara.lines):
            # inits
            _frags = _line[1]
            # text *MUST* embed {field} tag
            if _field in _frags:
                # replace tag by field value
                _frags[_frags.index(_field)] = _formatter(
                    self.canv._doctemplate.page + self.field_adjust
                )
                # trap out - do it once
                break
            # end if
        # end for
        # delegate to super class
        super().draw()
    # end def

# end class PageNumber



class SeqNumberParagraph (Paragraph):
    """
        Special flowable paragraph with sequential number feature while
        drawing;
    """

    # class constant defs
    MAIN_COUNTER = 1
    SUB_COUNTER = 1


    def __init__(
        self, text, style,
        bulletText=None, frags=None,
        caseSensitive=1, encoding='utf8',
        print_left=True, print_right=True,
        use_subcounter=False,
    ):
        """
            class constructor;
        """
        # member inits
        self.options = {
            "print_left": bool(print_left),
            "print_right": bool(print_right),
            "use_subcounter": bool(use_subcounter),
        }
        # super class inits
        super().__init__(
            text, style, bulletText, frags, caseSensitive, encoding
        )
    # end def


    def draw (self):
        """
            subclass override;
            refer to reportlab/platypus/paragraph.py
            for more detail;
        """
        # draw option marks
        self.draw_option_marks()
        # delegate to super class
        super().draw()
    # end def


    def draw_option_marks (self):
        """
            draws sequential number marks on margin left/right side of
            current paragraph along with self.options settings;
        """
        # inits
        _canvas = self.canv
        _text = self.get_seq_mark()
        _padding = 0.1*inch
        _font_size = self.blPara.fontSize
        _dy = self.height - _font_size
        # update counter(s) between instances
        self.update_seq_count()
        # keep settings
        _canvas.saveState()
        # fixed style for marks
        _canvas.setFont("Courier-Bold", _font_size)
        # print mark on left side?
        if self.options["print_left"]:
            # print mark
            _canvas.drawRightString(-_padding, _dy, _text)
        # end if
        # print mark on right side?
        if self.options["print_right"]:
            # print mark
            _canvas.drawString(self.width + _padding, _dy, _text)
        # end if
        # restore settings
        _canvas.restoreState()
    # end def


    def get_seq_mark (self):
        """
            returns formatted string for sequence mark;
        """
        # need subcounter?
        if self.options["use_subcounter"]:
            # format string
            return (
                # at this time, main counter is always one step beyond
                "#{}.{:02d}"
                .format(self.MAIN_COUNTER - 1, self.SUB_COUNTER)
            )
        # simple sequence
        else:
            # format string
            return "#{}".format(self.MAIN_COUNTER)
        # end if
    # end def


    @classmethod
    def reset (cls):
        """
            resets counters before building a document;
        """
        # reset counters
        cls.MAIN_COUNTER = 1
        cls.SUB_COUNTER = 1
    # end def


    def update_seq_count (self):
        """
            updates sequence counter(s) between instances;
        """
        # need subcounter?
        if self.options["use_subcounter"]:
            # update subcounter only
            __class__.SUB_COUNTER += 1
        # simple sequence
        else:
            # update main counter
            __class__.MAIN_COUNTER += 1
            # reset subcounter
            __class__.SUB_COUNTER = 1
        # end if
    # end def

# end class SeqNumberParagraph
