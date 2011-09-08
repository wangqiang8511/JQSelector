#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test for JQSelector 

@author Wang Qiang
"""

import unittest
import JQSelector as hsa


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
        element = hsa.parseByElement(xml, "to")
        self.assertEqual(element[0], "<to>Tove</to>")
        html = self.html
        element = hsa.parseByElement(html, "title")
        self.assertEqual(element[0], \
                         "<title>Python Programming Language; Official Website</title>")
        
    def testParseByTagProperties(self):
        """
        test for parseByProperties
        """
        html = self.html
        element = hsa.parseByTagProperties(html, "div", id="screen-switcher")
        self.assertEqual(element[0], '<div id="screen-switcher"></div>')
        
    def testParseByProperties(self):
        """
        test for parseByProperties
        """
        html = self.html
        element = hsa.parseByProperties(html, id="screen-switcher")
        self.assertEqual(element[0], '<div id="screen-switcher"></div>')
        
    def testJQSelect(self):
        """
        test for JQSelect
        """
        html = self.html
        elements = hsa.JQSelect(html, "meta")
        self.assertEqual(len(elements), 3)
        elements = hsa.JQSelect(html, 'div#searchbox')
        self.assertEqual(len(elements), 1)
        elements = hsa.JQSelect(html, 'div.skiptonav')
        self.assertEqual(len(elements), 2)
        elements = hsa.JQSelect(html, '#searchbox')
        self.assertEqual(len(elements), 1)
        elements = hsa.JQSelect(html, '.skiptonav')
        self.assertEqual(len(elements), 2)
        elements = hsa.JQSelect(html, '.homepage-box#quote')
        self.assertEqual(len(elements), 1)
        elements = hsa.JQSelect(html, '#quote.homepage-box')
        self.assertEqual(len(elements), 1)
        elements = hsa.JQSelect(html, 'div#quote.homepage-box')
        self.assertEqual(len(elements), 1)
        elements = hsa.JQSelect(html, '[type="hidden"]')
        self.assertEqual(len(elements), 6)
        elements = hsa.JQSelect(html, '[class|="homepage"]')
        self.assertEqual(len(elements), 4)
        elements = hsa.JQSelect(html, '[class*="homepage"]')
        self.assertEqual(len(elements), 4)
        elements = hsa.JQSelect(html, '[class^="homepage"]')
        self.assertEqual(len(elements), 4)
        elements = hsa.JQSelect(html, '[class$="box"]')
        self.assertEqual(len(elements), 3)
        elements = hsa.JQSelect(html, '[class~="success"]')
        self.assertEqual(len(elements), 2)
        elements = hsa.JQSelect(html, 'div[class="homepage-box"][id!="quote"]')
        self.assertEqual(len(elements), 1)
        
    def testJQSelectAdvance(self):
        """
        test for advanced JQSelect
        """
        html = self.html
        elements = hsa.JQSelect(html, 'li.group > a')
        self.assertEqual(len(elements), 8)
        elements = hsa.JQSelect(html, 'input#domains + input')
        self.assertEqual(len(elements), 2)
        elements = hsa.JQSelect(html, 'input#domains ~ input')
        self.assertEqual(len(elements), 8)
        
    def testJQSelectComplex(self):
        """
        test for complex JQSelector
        """
        html = self.html
        elements = hsa.JQSelect(html, 'div#test > div.label + div.table > li')
        self.assertEqual(len(elements), 8)
    
    def testJQSelectCombination(self):
        """
        test for multiple JQSelect
        """
        html = self.html
        elements = hsa.JQSelect(html, 'div[class="homepage-box"][id!="quote"],[class~="success"]')
        self.assertEqual(len(elements), 3)

if __name__ == '__main__':
    # Test all
    unittest.main()
    ## Test a specific function
    #fast = unittest.TestSuite()
    #fast.addTest(StatusesTest('testFunction'))
    #unittest.TextTestRunner().run(fast)
