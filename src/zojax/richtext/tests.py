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
import os.path
import unittest, doctest
from zope import component
from zope.component.eventtesting import setUp as eventsSetUp
from zope.app.testing import setup
from zope.app.testing.functional import ZCMLLayer, FunctionalDocFileSuite
from zojax.richtext import configlet, plaintext, rest, stx, html, htmlsource

richTextLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'richTextLayer', allow_teardown=True)


def setUp(test):
    eventsSetUp(test)
    site = setup.placefulSetUp(True)
    setup.setUpTestAsModule(test, name='zojax.richtext.TESTS')

    component.provideUtility(
        plaintext.PlainTextRenderer(), name='zope.source.plaintext')
    component.provideUtility(
        html.HTMLRenderer(), name="zope.source.html")
    component.provideUtility(
        rest.ReStructuredTextRenderer(), name="zope.source.rest")
    component.provideUtility(
        stx.StructuredTextRenderer(), name="zope.source.stx")
    component.provideUtility(
        htmlsource.HTMLSourceFactory, name="zope.source.html")


def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)


def test_suite():
    widget = FunctionalDocFileSuite(
        "widget.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    widget.layer = richTextLayer

    field = FunctionalDocFileSuite(
        'field.txt',
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
    field.layer = richTextLayer

    return unittest.TestSuite((
            widget, field,
            doctest.DocTestSuite(
                'zojax.richtext.plaintext',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
