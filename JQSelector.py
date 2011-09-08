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
'str1, str2,...'
'str1 > str2'
'str1 + str2'
'str1 ~ str2'
'str1 ~ str2 > str3...'
"""

import re
from pyquery import PyQuery


# pyquery function expanding
def listHtml():
    return [PyQuery(el).outerHtml() for i, el in enumerate(this)]

# list all the matched elements in string
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


def selectChild(pelements, selectStr):
    """
    elements = selectChild(pelements, selectStr)
    Select childs according to selectStr
    @param pelements: input parent elements
    @param selectStr: JQuery-like select string for child.
    @return: elements, list of matched elements in PyQuery
    """
    return pelements.children(selectStr)


def selectNext(pelements, selectStr):
    """
    elements = selectNext(pelements, selectStr)
    Select the next elements for the given elements.
    @param pelements: input previous elements
    @param selectStr: JQuery-like select string for next. 
    @return: elements, list of matched elements in PyQuery
    """
    return pelements.next()(selectStr)


def selectSibling(pelements, selectStr):
    """
    elements = selectSibling(pelements, selectStr)
    Select the the siblings
    @param pelements: input previous elements
    @param selectStr: JQuery-like select string for siblings. 
    @return: elements, list of matched elements in PyQuery
    """
    return pelements.siblings(selectStr)


def processSimpleSelector(html, selectStr):
    """
    elements = processSimpleSelector(html, selectStr)
    Implement JQuery-like selecting for a single simple selector
    @param html: input html/xml
    @param selectStr: JQuery-like select string.
    @return: elements, list of matched elements in PyQuery
    """
    pelements = PyQuery(html)
    return pelements(selectStr)


def selectByClass(html, classname):
    """
    elements = selectByClass(html, classname)
    select HTML/XML elements by class name.
    @param html: html source
    @param classname: class name filter
    @return: elements, list to matched elements in list
    """
    return parseByProperties(html, CLASS=classname)


def selectById(html, id):
    """
    elements = selectById(html, id)
    select HTML/XML elements by id.
    @param html: html source
    @param id: id filter
    @return: elements, list to matched elements
    """
    return parseByProperties(html, ID=id)


def parseByElement(html, elementName):
    """
    elements = parseByElement(html, elementName)
    parse HTML/XML elements by element name.
    @param html: html source
    @param elementName: element name filter
    @return: elements, list to matched elements
    """
    pelements = PyQuery(html)
    return pelements(elementName).listOuterHtml()


def parseByTagProperties(html, tagName, **properties):
    """
    elements = parseByTagProperties(html, tagName, **properties)
    parse HTML/XML elements by property pair and tag name.
    @param html: html source
    @param tagName: tag name
    @param properties: property pair
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
    @param html: html source
    @param properties: property pair,
    @return: elements, list to matched elements
    """
    return parseByTagProperties(html, "", **properties)


# Implement strategy pattern
class SelectOperation(object):
    """
    Abstract selectOperation class.
    """
    def performSelector(self, pelements, selectStr):
        """Perform selection operator"""
        raise NotImplementedError("This is abstract class.")


class SelectChildOperation(SelectOperation):
    """
    Perform select child operation.
    """
    @classmethod
    def performSelector(cls, pelements, selectStr):
        """Perform selection operator"""
        return selectChild(pelements, selectStr)


class SelectNextOperation(SelectOperation):
    """
    Perform select child operation.
    """
    @classmethod
    def performSelector(cls, pelements, selectStr):
        """Perform selection operator"""
        return selectNext(pelements, selectStr)


class SelectSiblingOperation(SelectOperation):
    """
    Perform select child operation.
    """
    @classmethod
    def performSelector(cls, pelements, selectStr):
        """Perform selection operator"""
        return selectSibling(pelements, selectStr)


# Implement Factory Pattern
class SelectOperationFactory(object):
    """
    Factory for select operation.
    """
    # select operation dictionary
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
