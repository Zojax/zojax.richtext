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
from zope.component import getUtility, queryUtility
from zojax.preferences.interfaces import IPreferenceGroup

from widget import DefaultRichTextWidget
from interfaces import IRichTextWidgetFactory
from interfaces import IContentEditorConfiglet


class ContentEditorConfiglet(object):
    interface.implements(IContentEditorConfiglet)

    def getEditorWidgetFactory(self, request, principal=None):
        if self.allow_selection:
            prefs = getUtility(IPreferenceGroup, 'portal.contenteditor')
            prefs = prefs.__bind__(principal)
            editor = prefs.editor
            factory = queryUtility(IRichTextWidgetFactory, editor)
            if factory is not None:
                return factory

        factory = queryUtility(IRichTextWidgetFactory, self.default_editor)
        if factory is not None:
            return factory

        return DefaultRichTextWidget


def SelectionAllowed(group):
    return getUtility(IContentEditorConfiglet).allow_selection
