#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# BSD License
# Copyright (c) 2011, Wang Qiang
# All rights reserved.

"""
JQSelector

Process HTML file and XML file.

Function list:

Three basic parser:
elements = parseByElement(html, elementName)
elements = parseByTagProperties(html, tagName, **properties)
elements = parseByProperties(html, **properties)

Advanced Selector:
elements = selectByClass(html, classname)
elements = selectById(html, id)

JQuery-like Selector:
elements = JQSelect(html, selectStr)

selectStr specification
'tag.class#id[name="value"]'
[name|="value"]
[name*="value"]
[name~="value"]
[name!="value"]
[name^="value"]
[name$="value"]
"""
import re
from pyquery import PyQuery


def listHtml():
    return [PyQuery(el).outerHtml() for i, el in enumerate(this)]

PyQuery.fn.listOuterHtml = listHtml


def JQSelect(html, selectStr):
    """
    elements = JQSelect(html, selectStr)
    Implement JQuery-like selecting function
    @param html: input html/xml
    @param selectStr: JQuery-like select string.
    @return: elements, list of matched elements
    """
    selectors = [s.strip() for s in selectStr.split(',')]
    elements = []
    for selector in selectors:
        elements += processSingleSelector(html, selector) and \
        processSingleSelector(html, selector) or []
    return elements


def processSingleSelector(html, selectStr):
    """
    elements = processSingleSelector(html, selectStr)
    Implement JQuery-like selecting for a single selector
    @param html: input html/xml
    @param selectStr: JQuery-like select string.
    @return: elements, list of matched elements
    """
    selectors = re.split(r' > | \+ | ~ ', selectStr)
    for selector in selectors:
        selector = selector.strip()
    operators = re.findall(r' > | \+ | ~ ', selectStr)
    pelements = processSimpleSelector(html, selectors[0])
    for i in range(1, len(selectors)):
        OperationFactory = SelectOperationFactory(operators[i - 1])
        pelements = OperationFactory.performOperation(pelements, selectors[i])
        if (not pelements):
            break
    return pelements and pelements.listOuterHtml() or []


def processChildSelector(html, selectStr):
    selectors = [s.strip() for s in selectStr.split(' > ')]
    pelements = processSimpleSelector(html, selectors[0])
    return selectChild(pelements, selectors[1])


def selectChild(pelements, selectStr):
    """
    Select childs according to selectStr
    """
    return pelements.children(selectStr)


def processNextSelector(html, selectStr):
    selectors = [s.strip() for s in selectStr.split(' + ')]
    pelements = processSimpleSelector(html, selectors[0])
    return selectNext(pelements, selectors[1])


def selectNext(pelements, selectStr):
    """
    Select the next elements for the given elements.
    """
    return pelements.next()(selectStr)


def processSiblingSelector(html, selectStr):
    selectors = [s.strip() for s in selectStr.split(' ~ ')]
    pelements = processSimpleSelector(html, selectors[0])
    return selectSibling(pelements, selectors[1])


def selectSibling(pelements, selectStr):
    """
    Select the the siblings
    """
    return pelements.siblings(selectStr)


def processSimpleSelector(html, selectStr):
    """
    elements = processSimpleSelector(html, selectStr)
    Implement JQuery-like selecting for a single simple selector
    @param html: input html/xml
    @param selectStr: JQuery-like select string.
    @return: elements, list of matched elements
    """
    pelements = PyQuery(html)
    return pelements(selectStr)


def selectByClass(html, classname):
    """
    elements = selectByClass(html, classname)
    select HTML/XML elements by class name.
    @param classname: class name filter
    @param html: html source
    @return: elements, list to matched elements
    """
    return parseByProperties(html, CLASS=classname)


def selectById(html, id):
    """
    elements = selectById(html, id)
    select HTML/XML elements by id.
    @param id: id filter
    @param html: html source
    @return: elements, list to matched elements
    """
    return parseByProperties(html, ID=id)


def parseByElement(html, elementName):
    """
    elements = parseByElement(html, elementName)
    parse HTML/XML elements by element name.
    @param elementName: element name filter
    @param html: html source
    @return: elements, list to matched elements
    """
    pelements = PyQuery(html)
    return pelements(elementName).listOuterHtml()


def parseByTagProperties(html, tagName, **properties):
    """
    elements = parseByTagProperties(html, tagName, **properties)
    parse HTML/XML elements by property pair and tag name.
    @param properties: property pair
    @param tagName: tag name
    @param html: html source
    @return: elements, list to matched elements
    """
    selector = tagName
    for k, v in properties.items():
        selector += '[' + k + '="' + v + '"]'
    return processSimpleSelector(html, selector).listOuterHtml()


def parseByProperties(html, **properties):
    """
    elements = parseByProperties(html, **properties)
    parse HTML/XML elements by property pair.
    @param properties: property pair,
    @param html: html source
    @return: elements, list to matched elements
    """
    return parseByTagProperties(html, "", **properties)


# Implement strategy pattern
class SelectOperation(object):
    """
    Abstract selectOperation class.
    """
    def performSelector(self, pelements, selectStr):
        raise NotImplementedError("This is abstract class.")


class SelectChildOperation(SelectOperation):
    """
    Perform select child operation.
    """
    @classmethod
    def performSelector(cls, pelements, selectStr):
        return selectChild(pelements, selectStr)


class SelectNextOperation(SelectOperation):
    """
    Perform select child operation.
    """
    @classmethod
    def performSelector(cls, pelements, selectStr):
        return selectNext(pelements, selectStr)


class SelectSiblingOperation(SelectOperation):
    """
    Perform select child operation.
    """
    @classmethod
    def performSelector(cls, pelements, selectStr):
        return selectSibling(pelements, selectStr)


# Implement Factory Pattern
class SelectOperationFactory(object):
    """
    Factory for select operation.
    """
    operationDict = {}
    operationDict[' > '] = SelectChildOperation
    operationDict[' + '] = SelectNextOperation
    operationDict[' ~ '] = SelectSiblingOperation

    def __init__(self, operator):
        """
        Constructor.
        """
        self.operationClass = self.operationDict[operator]

    def performOperation(self, pelements, selectStr):
        """
        Perform operation
        """
        return self.operationClass.performSelector(pelements, selectStr)
