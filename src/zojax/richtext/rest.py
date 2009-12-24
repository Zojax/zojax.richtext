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
"""ReStructured Text Renderer Classes

$Id$
"""
import docutils.core
from docutils.writers.html4css1 import Writer
from docutils.writers.html4css1 import HTMLTranslator

from zope import interface
from interfaces import _, IRenderer


class ZopeTranslator(HTMLTranslator):

    def astext(self):
        # use the title, subtitle, author, date, etc., plus the content
        body = self.body_pre_docinfo + self.docinfo + self.body
        return u"".join(body)


class ReStructuredTextRenderer(object):
    interface.implements(IRenderer)

    title = _("ReStructured Text (ReST)")

    description = _("ReStructured Text (ReST) Source")

    def render(self, text, settings_overrides={}):
        overrides = {
            'halt_level': 6,
            'input_encoding': 'unicode',
            'output_encoding': 'unicode',
            'initial_header_level': 3,
            }
        overrides.update(settings_overrides)
        writer = Writer()
        writer.translator_class = ZopeTranslator
        html = docutils.core.publish_string(
            text,
            writer=writer,
            settings_overrides=overrides,
            )
        return html
