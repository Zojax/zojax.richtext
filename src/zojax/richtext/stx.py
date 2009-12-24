##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Structured Text Renderer Classes

$Id$
"""
import re

from zope import interface
from zope.structuredtext.html import HTML
from zope.structuredtext.document import Document

from interfaces import _, IRenderer


class StructuredTextRenderer(object):
    interface.implements(IRenderer)

    title = _("Structured Text (STX)")
    description = _("Structured Text (STX) Source")

    def render(self, text):
        encoded = text.encode('UTF-8')
        doc = Document()(encoded)
        html = HTML()(doc)

        # strip html & body added by some zope versions
        html = re.sub(
            r'(?sm)^<html.*<body.*?>\n(.*)</body>\n</html>\n',r'\1', html)

        return html.decode('UTF-8')
