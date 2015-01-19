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

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm, mm

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


def gather_informations (doc):
    """
        gathers informations for specific PDF document;
    """
    # delegate to specific
    doc.gather_info()
    # progression status (0-100%)
    return doc.progress
# end def


def get_pdf_document (doc_name, options):
    """
        returns a new instance for a PDF document with filepath built
        along with @doc_name document name value;
    """
    # new document instance
    return eval(
        "PDFDocument{name}(doc_name, options)"
        .format(name=str(doc_name).title().replace("_", ""))
    )
# end def



class PDFDocumentBase:
    """
        Base class for tkScenarist specific PDF documents to export;
    """

    def __init__ (self, doc_name, options):
        """
            class constructor;
        """
        # member inits
        self.app = SM.ask_for("app") # application
        self.pfm = SM.ask_for("PFM") # Project File Management
        self.mainwindow = self.app.mainwindow
        self.mainframe = self.mainwindow.mainframe
        self.project_data = self.mainframe.tab_title_data.get_data()
        self.database = self.mainwindow.database
        self.pdf = self.get_pdf_document(doc_name)
        self.doc_name = doc_name
        self.options = options
        self.elements = list()
        self.progress = 0
        self.index = 0
    # end def


    def build_document (self):
        """
            hook method to be reimplemented in subclass;
            builds final PDF document;
        """
        # reset progress
        self.reset_progress()
        # must do it one shot
        self.pdf.build(
            self.elements,
            onFirstPage=self.draw_first_page,
            onLaterPages=self.draw_pages,
        )
        # procedure is complete
        self.progress = 100
    # end def


    def build_elements (self):
        """
            hook method to be reimplemented in subclass;
            builds document internal elements;
        """
        # reset progress
        self.reset_progress()
        # put your own code in subclass
        pass
        # procedure is complete
        self.progress = 100
    # end def


    def draw_first_page (self, canvas, doc):
        """
            hook method to be reimplemented in subclass;
            draws fix elements (header, footer, etc) on page;
        """
        # put your own code in subclass
        pass
    # end def


    def draw_pages (self, canvas, doc):
        """
            hook method to be reimplemented in subclass;
            draws fix elements (header, footer, etc) on page;
        """
        # put your own code in subclass
        pass
    # end def


    def gather_info (self):
        """
            hook method to be reimplemented in subclass;
            gathers specific informations for document building;
        """
        # reset progress
        self.reset_progress()
        # put your own code in subclass
        print("options:", self.options)
        # procedure is complete
        self.progress = 100
    # end def


    def get_pdf_document (self, doc_name):
        """
            provides a reportlab.PDFDocument;
        """
        # param controls
        if tools.is_pstr(doc_name):
            # inits
            _data = self.project_data
            _fancy_name = _(str(doc_name).title().replace("_", "/"))
            _fpath, _fext = os.path.splitext(self.pfm.project_path)
            # rebuild filepath
            _fpath = P.normalize("{}-{}.pdf".format(_fpath, doc_name))
            # PDF document instance
            return SimpleDocTemplate(
                filename=_fpath,
                author=_data.get("project_author"),
                title="{project_title} - "
                "{project_subtitle} - "
                "{project_episode}"
                .format(**_data),
                subject=_fancy_name,
                creator=self.app.APP.get("title"),
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


    def reset_progress (self):
        """
            resets progress status to 0 if >= 100 (%);
        """
        if self.progress >= 100:
            self.progress = 0
        # end if
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
    pass
# end class PDFDocumentDraftNotes



class PDFDocumentPitchConcept (PDFDocumentBase):
    """
        specific PDF document class for Pitch/Concept application tab;
    """
    pass
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
    pass
# end class PDFDocumentScenario



class PDFDocumentStoryboard (PDFDocumentBase):
    """
        specific PDF document class for Storyboard application tab;
    """
    pass
# end class PDFDocumentStoryboard
