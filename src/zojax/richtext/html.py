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
from zope import interface, component, cachedescriptors
from zope.app.intid.interfaces import IIntIds

from interfaces import _, IRenderer
import re

SUB = re.compile('@@content\.browser/(\n+)')

class HTMLRenderer(object):
    interface.implements(IRenderer)

    title = _("HTML")
    description = _("HTML Source")
    
    @cachedescriptors.property.CachedProperty
    def ids(self):
        return component.getUtility(IIntIds)

    def render(self, text):
        return SUB.sub(self.getObjectUrl, text)
    
    def getObjectUrl(self, uid):
        id = uid.group(1)
        try:
            return absoluteURL(self.ids.getObject(int(id)))
        except (TypeError, ValueError, KeyError), e:
            return '@@content.browser/'+id