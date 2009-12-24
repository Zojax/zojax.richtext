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
"""Plain Text Renderer Classes

$Id$
"""
import cgi
from zope import interface
from interfaces import _, IRenderer


class PlainTextRenderer(object):
    """
    >>> renderer = PlainTextRenderer()

    >>> print renderer.render('Test text1\\n   test text2\\n test text3   ')
    Test text1<br />
    &nbsp;&nbsp;&nbsp;test text2<br />
    &nbsp;test text3
    """
    interface.implements(IRenderer)

    title = _("Plain Text")
    description = _("Formatted plain Text Source")

    def render(self, text):
        lines = []
        for line in cgi.escape(text).split('\n'):
            l = u''
            idx = 0
            for ch in line:
                if ch == u' ':
                    idx += 1
                    l = l + u'&nbsp;'
                else:
                    break

            lines.append(l + line[idx:] + u'<br />')

        if lines:
            lines[-1] = lines[-1][:-6]

        return u'\n'.join(lines)
