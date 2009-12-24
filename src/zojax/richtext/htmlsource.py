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
"""

$Id$
"""
from zope import interface, component
from zope.app.renderer import SourceFactory
from zope.app.renderer.interfaces import ISource, IHTMLRenderer

from interfaces import _


class IHTMLSource(ISource):
    """ HTML source """


HTMLSourceFactory = SourceFactory(
    IHTMLSource, _("HTML"), _("HTML Source"))


class HTMLToHTMLRenderer(object):
    interface.implements(IHTMLRenderer)
    component.adapts(IHTMLSource)

    def render(self):
        return self.context
