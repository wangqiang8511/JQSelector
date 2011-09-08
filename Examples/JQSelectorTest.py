#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test for JQSelector 

@author Wang Qiang
"""

import unittest
import JQSelector as jqs


class UnitTest(unittest.TestCase):
    """
    Test for JQSelector
    """

    f = open("test.html", 'r')
    html = f.read()
    f.close()
    f = open("test.xml", 'r')
    xml = f.read()
    f.close()
            
    def testParseByElement(self):
        """test for parseByElement"""
        #self.assertTrue(e)
        #self.assertEqual(a, b)
        xml = self.xml
        element = jqs.parseByElement(xml, "to")
        self.assertEqual(len(element), 1)
        html = self.html
        element = jqs.parseByElement(html, "title")
        self.assertEqual(len(element), 1)
        
    def testParseByTagProperties(self):
        """
        test for parseByProperties
        """
        html = self.html
        element = jqs.parseByTagProperties(html, "div", id="screen-switcher")
        self.assertEqual(element[0], '<div id="screen-switcher"></div>')
        
    def testParseByProperties(self):
        """
        test for parseByProperties
        """
        html = self.html
        element = jqs.parseByProperties(html, id="screen-switcher")
        self.assertEqual(element[0], '<div id="screen-switcher"></div>')
        
    def testJQSelect(self):
        """
        test for JQSelect
        """
        html = self.html
        elements = jqs.JQSelect(html, "meta")
        self.assertEqual(len(elements), 3)
        elements = jqs.JQSelect(html, 'div#searchbox')
        self.assertEqual(len(elements), 1)
        elements = jqs.JQSelect(html, 'div.skiptonav')
        self.assertEqual(len(elements), 2)
        elements = jqs.JQSelect(html, '#searchbox')
        self.assertEqual(len(elements), 1)
        elements = jqs.JQSelect(html, '.skiptonav')
        self.assertEqual(len(elements), 2)
        elements = jqs.JQSelect(html, '.homepage-box#quote')
        self.assertEqual(len(elements), 1)
        elements = jqs.JQSelect(html, '#quote.homepage-box')
        self.assertEqual(len(elements), 1)
        elements = jqs.JQSelect(html, 'div#quote.homepage-box')
        self.assertEqual(len(elements), 1)
        elements = jqs.JQSelect(html, '[type="hidden"]')
        self.assertEqual(len(elements), 6)
        elements = jqs.JQSelect(html, '[class|="homepage"]')
        self.assertEqual(len(elements), 4)
        elements = jqs.JQSelect(html, '[class*="homepage"]')
        self.assertEqual(len(elements), 4)
        elements = jqs.JQSelect(html, '[class^="homepage"]')
        self.assertEqual(len(elements), 4)
        elements = jqs.JQSelect(html, '[class$="box"]')
        self.assertEqual(len(elements), 3)
        elements = jqs.JQSelect(html, '[class~="success"]')
        self.assertEqual(len(elements), 2)
        elements = jqs.JQSelect(html, 'div[class="homepage-box"][id!="quote"]')
        self.assertEqual(len(elements), 1)
        
    def testJQSelectAdvance(self):
        """
        test for advanced JQSelect
        """
        html = self.html
        elements = jqs.JQSelect(html, 'li.group > a')
        self.assertEqual(len(elements), 8)
        elements = jqs.JQSelect(html, 'input#domains + input')
        self.assertEqual(len(elements), 2)
        elements = jqs.JQSelect(html, 'input#domains ~ input')
        self.assertEqual(len(elements), 8)
        
    def testJQSelectComplex(self):
        """
        test for complex JQSelector
        """
        html = self.html
        elements = jqs.JQSelect(html, 'div#test > div.label + div.table > li')
        self.assertEqual(len(elements), 8)
    
    def testJQSelectCombination(self):
        """
        test for multiple JQSelect
        """
        html = self.html
        elements = jqs.JQSelect(html, 'div[class="homepage-box"][id!="quote"],[class~="success"]')
        self.assertEqual(len(elements), 3)

if __name__ == '__main__':
    # Test all
    unittest.main()
    ## Test a specific function
    #fast = unittest.TestSuite()
    #fast.addTest(StatusesTest('testFunction'))
    #unittest.TextTestRunner().run(fast)
