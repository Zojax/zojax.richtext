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
from zope import schema, interface
from zope.schema.interfaces import IField
from zope.i18nmessageid import MessageFactory
from zope.component.interfaces import IObjectEvent

_ = MessageFactory('zojax.richtext')


class IRichText(IField):
    """ rich text field """

    default_format = schema.Choice(
        title = u'Default format',
        default = u"zope.source.plaintext",
        vocabulary = u'zojax.richtext-renderers',
        required = False)


class IRichTextData(interface.Interface):
    """ rich text data """

    format = schema.Choice(
        title = u'Format',
        description = u'Text format',
        vocabulary = u'zojax.richtext-renderers',
        default = 'zope.source.plaintext',
        required = False)

    text = schema.Text(
        title = u'Text',
        description = u'Field data',
        required = True)

    cooked = interface.Attribute('Cooked text')

    def __eq__():
        """ compare IRichTextData objects """

    def __ne__():
        """ compare IRichTextData objects """

    def __len__():
        """ text length """

    def __str__():
        """ cooked text """

    def render():
        """ render text """


class IRichTextDataModified(IObjectEvent):

    data = interface.Attribute('IRichTextData object')



class IRichTextWidgetFactory(interface.Interface):
    """ RichText widget factory """

    title = schema.TextLine(
        title = u'Title',
        description = u'Widget title',
        required = True)

    def __call__(request):
        """ create widget """


class IRichTextWidget(interface.Interface):
    """ rich text widget """


class IDefaultRichTextWidget(IRichTextWidget):
    """ default rich text widget """


class IContentEditorConfiglet(interface.Interface):
    """ controlpanel configlet """

    allow_selection = schema.Bool(
        title = _(u'Allow change editor'),
        description = _('Allow change editor for members.'),
        default = True,
        required = False)

    default_editor = schema.Choice(
        title = _(u'Content editor'),
        description = _(u'Select the content editor that members will use. '
                        u'Note that content editors often have specific browser '
                        u'requirements.'),
        vocabulary = 'zojax.richtext-widgets',
        default = u'default')

    def getEditorWidgetFactory(request, principal=None):
        """ return intialized widget """


class IContentEditorPreference(interface.Interface):
    """ user editor preference """

    editor = schema.Choice(
        title = _(u'Content editor'),
        description = _(u'Select the content editor that you would like to use. '
                        u'Note that content editors often have specific browser '
                        u'requirements.'),
        vocabulary = 'zojax.richtext-widgets')


class IRenderer(interface.Interface):
    """ renderer """

    title = interface.Attribute('Title')

    description = interface.Attribute('Description')

    def render(text):
        """ render text to html """
