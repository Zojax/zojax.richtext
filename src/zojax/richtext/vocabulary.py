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
from zope import interface
from zope.component import getUtilitiesFor
from zope.security.management import queryInteraction
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import IRenderer, IRichTextWidgetFactory


class WysiwygWidgets(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        widgets = []
        for name, factory in getUtilitiesFor(IRichTextWidgetFactory):
            widgets.append((factory.title, name))

        widgets.sort()
        return SimpleVocabulary([SimpleTerm(name, name, title)
                                 for title, name in widgets])


class Renderers(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        renderers = []
        for name, renderer in getUtilitiesFor(IRenderer):
            renderers.append((renderer.title, name))

        renderers.sort()
        return SimpleVocabulary([
                SimpleTerm(name, name, title) for title, name in renderers])
