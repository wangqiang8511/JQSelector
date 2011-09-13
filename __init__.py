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

__version__ = '1.0'
__author__ = 'Wang Qiang'
__license__ = 'BSD License'

__all__ = ['JQSelector']

from JQSelector import JQSelect 
