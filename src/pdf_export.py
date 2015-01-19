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
import os.path as OP
import reportlab
import tkRAD.core.path as P
import tkRAD.core.services as SM


def get_pdf_document (doc_name):
    """
        returns a new instance for a PDF document with filepath built
        along with @doc_name document name value;
    """
    # inits
    pass
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


def build_elements (doc):
    """
        builds elements for specific PDF document;
    """
    # delegate to specific
    doc.build_elements()
    # progression status (0-100%)
    return doc.progress
# end def


def build_document (doc):
    """
        builds final doc for specific PDF document;
    """
    # delegate to specific
    doc.build_document()
    # progression status (0-100%)
    return doc.progress
# end def



class PDFDocumentBase:
    """
        Base class for tkScenarist specific PDF documents to export;
    """

    def __init__ (self, doc_name):
        """
            class constructor;
        """
        # member inits
        self.app = SM.ask_for("app") # application
        self.pfm = SM.ask_for("PFM") # Project File Management
        self.progress = 0
        self.document = self.get_document(doc_name)
    # end def


    def get_document (self, doc_name):
        """
            provides a reportlab.PDFDocument;
        """
        _fpath, _fext = OP.splitext(self.pfm.project_path)
        # rebuild filepath
        _fpath = P.normalize("{}-{}.pdf".format(_fpath, doc_name))
        print("filepath:", _fpath)
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
        self.__progress = float(value)
    # end def

    @progress.deleter
    def progress (self):
        # delete
        del self.__progress
    # end def

# end class PDFDocumentBase














