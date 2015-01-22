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
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.platypus.frames import ShowBoundaryValue
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import *                   # text alignments

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
            fontName="Times-BoldItalic",
            fontSize=24,
            leading=26,
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
        "body": ParagraphStyle(
            "body",
            parent=_root_style,
            fontName="Helvetica",
            alignment=TA_JUSTIFY,
            spaceAfter=0.1*inch,
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
            leftIndent=0.5*inch,
            spaceAfter=0.1*inch,
        ),

        # storyboard tab styles

        "shot_title": ParagraphStyle(
            "shot_title",
            parent=_root_style,
            fontName="Courier-Bold",
            backColor="#f0f0f0",
            spaceAfter=0.1*inch,
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


    def add_paragraph (self, text, style):
        """
            adds a Paragraph() object only if @text is a plain string
            of chars;
        """
        # ensure we have some text
        if tools.is_pstr(text):
            # add paragraph
            self.elements.append(Paragraph(text, style))
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



class PDFDocumentCharacters (PDFDocumentBase):
    """
        specific PDF document class for Characters application tab;
    """
    pass
# end class PDFDocumentCharacters



class PDFDocumentDraftNotes (PDFDocumentBase):
    """
        specific PDF document class for Draft/Notes application tab;
    """

    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(doc_name, **kw)
        # additional member inits
        self.wtext = self.mainframe.tab_draft_notes.text_draft_notes
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
            # force reset all
            self.reset_progress(force_reset=True)
            # next step
            self.step = 1
            self.index = 1.0
            # estimate size of text
            # without loading text contents
            _lines = float(self.wtext.index(TK.END))
            # not so much?
            if _lines < 3000:
                # get real size
                self.total_bytes = len(self.wtext.get("1.0", TK.END))
            # spare time
            else:
                # estimate 1 line of text is about 360 chars
                self.total_bytes = _lines * 360
            # end if
            # ensure it is > 0
            self.total_bytes = max(1, self.total_bytes)
            # first page elements
            self.set_first_page_elements()
        # next steps
        else:
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
                # browse lines of text
                for _line in _text.split("\n"):
                    # add new paragraph
                    self.add_paragraph(_line, self.styles["body"])
                # end for
            # end if
        # end if
    # end def

# end class PDFDocumentDraftNotes



class PDFDocumentPitchConcept (PDFDocumentDraftNotes):
    """
        specific PDF document class for Pitch/Concept application tab;
    """

    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(doc_name, **kw)
        # additional member inits
        self.wtext = self.mainframe.tab_pitch_concept.text_pitch_concept
    # end def

# end class PDFDocumentPitchConcept



class PDFDocumentResources (PDFDocumentBase):
    """
        specific PDF document class for Resources application tab;
    """
    pass
# end class PDFDocumentResources



class PDFDocumentScenario (PDFDocumentBase):
    """
        specific PDF document class for Scenario application tab;
    """

    def __init__ (self, doc_name, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__(doc_name, **kw)
        # additional member inits
        self.wtext = self.mainframe.tab_scenario.TEXT
        self.stats = dict()
    # end def


    def add_stats_elements (self):
        """
            adds statistics to document as appendix;
        """
        # inits
        _s = self.stats
        _texts = (
            (_("Statistics"), "h1"),
            (_("Document"), "h2"),
            (_("Pages: {page_count}").format(**_s), ""),
            (_("Paragraphs: {paragraph_count}").format(**_s), ""),
            (_("Words: {word_count}").format(**_s), ""),
            (_("Chars: {byte_count}").format(**_s), ""),
            (_("Elements"), "h2"),
            (_("Scenes: {scene_count}").format(**_s), ""),
            (_("Dialogues: {dialogue_count}").format(**_s), ""),
            (_("Transitions: {transition_count}").format(**_s), ""),
            (_("Movie"), "h2"),
            (
                _("Movie characters: {char_count}")
                .format(char_count=len(_s["movie_chars"])),
                ""
            ),
            (
                _("Estimated movie duration: {movie_duration}")
                .format(movie_duration=self.get_duration(95)),              # FIXME
                ""
            ),
            #~ (_("").format(), ""),
        )
        # new page
        self.add_pagebreak()
        # loop on collection
        for (_text, _stylename) in _texts:
            # add paragraph
            self.add_paragraph(
                _text, self.styles[_stylename or "stats"]
            )
        # end for
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
            # force reset all
            self.reset_progress(force_reset=True)
            # reset stats
            self.stats.clear()
            # next step
            self.step = 1
            self.index = 1.0
            # estimate size of text
            # without loading text contents
            _lines = float(self.wtext.index(TK.END))
            # not so much?
            if _lines < 3000:
                # get real size
                self.total_bytes = len(self.wtext.get("1.0", TK.END))
            # spare time
            else:
                # estimate 1 line of text is about 360 chars
                self.total_bytes = _lines * 360
            # end if
            # ensure it is > 0
            self.total_bytes = max(1, self.total_bytes)
            # first page elements
            self.set_first_page_elements()
        # next steps
        else:
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
                        # add new paragraph
                        self.add_paragraph(_line, _style)
                        # update statistics
                        self.update_stats(_line, _style.name)
                    # end for
                # end for
            # end if
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
        # nb of movie characters
        if tag == "character":
            # inits
            _s["movie_chars"] = _s.setdefault("movie_chars", set())
            # add character name
            _s["movie_chars"].add(text)
        # end if
        # nb of pages
        _s["page_count"] = '<seq template="%(Page)s"/>'
    # end def

# end class PDFDocumentScenario



class PDFDocumentStoryboard (PDFDocumentBase):
    """
        specific PDF document class for Storyboard application tab;
    """
    pass
# end class PDFDocumentStoryboard
