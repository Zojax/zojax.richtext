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
from zope import schema, component, interface
from zope.proxy import removeAllProxies
from zope.component import getUtility, queryUtility, getMultiAdapter
from zope.app.pagetemplate import ViewPageTemplateFile

from z3c.form import interfaces, converter, datamanager
from z3c.form.browser import textarea
from z3c.form.widget import Widget, FieldWidget

from zojax.preferences.interfaces import IPreferenceGroup

from interfaces import _
from interfaces import IRichText, IRichTextData
from interfaces import IRichTextWidgetFactory
from interfaces import IRichTextWidget, IDefaultRichTextWidget
from interfaces import IContentEditorConfiglet

from field import RichTextData


@component.adapter(IRichText, interface.Interface)
@interface.implementer(interfaces.IFieldWidget)
def RichTextFieldWidget(field, request):
    configlet = getUtility(IContentEditorConfiglet)
    factory = configlet.getEditorWidgetFactory(request)

    return FieldWidget(field, factory(request))


class DefaultRichTextWidget(textarea.TextAreaWidget):
    interface.implements(IDefaultRichTextWidget)

    format_template = ViewPageTemplateFile('widget.pt')

    rows = 15
    klass = 'widget-richtext'

    def update(self):
        field = self.field

        self.format = schema.Choice(
            __name__ = '%s_format'%field.__name__,
            title = _(u"Text format"),
            description = _(u"If you are unsure of which format to use, just select Plain Text and type the document as you usually do."),
            vocabulary = "zojax.richtext-renderers",
            required = False)

        self.format.context = self

        self.format_widget = getMultiAdapter(
            (self.format, self.request),  interfaces.IFieldWidget)
        self.format_widget.context = self
        interface.alsoProvides(self.format_widget, interfaces.IContextAware)
        self.format_widget.update()

        super(DefaultRichTextWidget, self).update()

    def render(self):
        textarea = super(DefaultRichTextWidget, self).render()

        if self.mode == interfaces.DISPLAY_MODE:
            return textarea
        else:
            return textarea + self.format_template()

    def extract(self, default=interfaces.NOVALUE):
        textarea = self.request.get(self.name, default)
        format = self.format_widget.extract()

        if textarea is default and format is default:
            return default

        if format is not default:
            format = format[0]

        return RichTextData(textarea, format)

    def getValue(self):
        if IRichTextData.providedBy(self.value):
            return removeAllProxies(self.value).text
        else:
            return u''


class DefaultDataManager(datamanager.AttributeField):
    interface.implements(interfaces.IDataManager)
    component.adapts(IDefaultRichTextWidget, interface.Interface)

    def __init__(self, context, field):
        self.context = context
        self.field = field

    def get(self):
        if interfaces.IContextAware.providedBy(self.context) and \
                not self.context.ignoreContext:
            manager = component.queryMultiAdapter(
                (self.context.context, self.context.field),
                interfaces.IDataManager)
            if manager is not None:
                try:
                    value = manager.get()
                except TypeError:
                    value = self.context.field.default_format
            else:
                self.context.field.default_format
        else:
            value = self.context.value

        if IRichTextData.providedBy(value):
            return value.format
        else:
            return self.context.field.default_format

    def query(self, default=interfaces.NOVALUE):
        if interfaces.IContextAware.providedBy(self.context) and \
                not self.context.ignoreContext:
            manager = component.queryMultiAdapter(
                (self.context.context, self.context.field),
                interfaces.IDataManager)
            if manager is not None:
                value = manager.query(self.context.field.default_format)
            else:
                self.context.field.default_format
        else:
            value = self.context.value

        if IRichTextData.providedBy(value):
            return value.format
        else:
            return self.context.field.default_format


class DefaultDataConverter(converter.BaseDataConverter):
    component.adapts(IRichText, IRichTextWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return RichTextData(u'', self.widget.field.default_format)
        return value

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        return value


class DefaultWidgetFactory(object):
    interface.implements(IRichTextWidgetFactory)

    title = _(u'Basic HTML textarea editor')

    def __call__(self, request):
        return DefaultRichTextWidget(request)
