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
""" RichText field

$Id$
"""
from rwproperty import getproperty, setproperty

from zope import schema, interface, event
from persistent import Persistent
from persistent.interfaces import IPersistent
from zope.schema.interfaces import WrongType, RequiredMissing
from zope.proxy import removeAllProxies
from zope.security.proxy import removeSecurityProxy
from zope.component import getUtility, queryUtility
from zope.component.interfaces import ObjectEvent
from zope.schema._bootstrapinterfaces import RequiredMissing
from interfaces import IRenderer, IRichText, IRichTextData, IRichTextDataModified


class RichText(schema.MinMaxLen, schema.Field):
    interface.implements(IRichText)

    _type = None
    default_format = u"zope.source.plaintext"

    def __init__(self, default_format=u"zope.source.plaintext", **kw):
        self.default_format = default_format
        super(RichText, self).__init__(**kw)

    def get(self, object, _getattr=getattr, _setattr=setattr):
        value = _getattr(object, self.__name__, None)

        if IRichTextData.providedBy(value):
            return value
        elif value is None:
            return None
        elif isinstance(value, list):
            self.set(
                object, RichTextData(value[0], value[1]), _getattr, _setattr)
        else:
            self.set(
                object,
                RichTextData(value, self.default_format), _getattr, _setattr)

        return self.get(object, _getattr, _setattr)

    def set(self, object, value, _getattr=getattr, _setattr=setattr):
        if self.readonly:
            raise TypeError("Can't set values on read-only fields "
                            "(name=%s, class=%s.%s)"
                            % (self.__name__,
                               object.__class__.__module__,
                               object.__class__.__name__))

        if IRichTextData.providedBy(value):
            _setattr(object, self.__name__, value)
        else:
            _setattr(object, self.__name__, RichTextData(unicode(value)))

        event.notify(RichTextDataModified(
                object, _getattr(object, self.__name__)))

    def validate(self, value):
        if not isinstance(value, unicode):
            if not IRichTextData.providedBy(value):
                raise WrongType(value, IRichTextData)

            if self.required:
                if not value.text:
                    raise RequiredMissing()

        return super(RichText, self).validate(value)


class RichTextData(Persistent):
    interface.implements(IRichTextData)

    cooked = u''

    def __init__(self, text=u'', format=u'zope.source.plaintext'):
        self.format = format
        self.text = unicode(text, 'utf-8')

    def clear(self):
        self.format = u''
        self.text = u''
        self.cooked = None

    def render(self):
        renderer = queryUtility(IRenderer, name=self.format)
        if renderer is None:
            renderer = getUtility(IRenderer, name=u"zope.source.plaintext")

        return renderer.render(self.text)

    @getproperty
    def text(self):
        return self.__dict__.get('text', u'')

    @setproperty
    def text(self, value):
        self.__dict__['text'] = value
        self.cooked = self.render()
        self._p_changed = True

    def __len__(self):
        return len(self.text)

    def __nonzero__(self):
        return len(self.text) > 0

    def __eq__(self, other):
        if IRichTextData.providedBy(other):
            if (self.format == other.format) and (self.text == other.text):
                return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)


_marker = object()

class RichTextProperty(object):

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __get__(self, inst, klass):
        if inst is None:
            return self

        try:
            value = self.__field.get(inst, self.__getattr, self.__setattr)
        except AttributeError:
            value = _marker

        if value is _marker:
            field = self.__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)

        return value

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        if field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__field.set(inst, value, self.__getattr, self.__setattr)

    def __delete__(self, inst):
        if self.__name in inst.__dict__:
            del inst.__dict__[self.__name]

    def __getattr(self, object, name, default=None):
        return removeSecurityProxy(object).__dict__.get(name, default)

    def __setattr(self, object, name, value):
        removeSecurityProxy(object).__dict__[name] = removeAllProxies(value)

        if IPersistent.providedBy(object):
            object._p_changed = True


class RichTextDataModified(ObjectEvent):
    interface.implements(IRichTextDataModified)

    def __init__(self, object, data):
        self.object = object
        self.data = data
