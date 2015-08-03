"""
Tests for playgroundExportToMarkdown.py methods
"""

import unittest

import playgroundExportToMarkdown

from StringIO import StringIO

class playgroundExportToMarkdownTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testListFilesFromXCPlaygroundData(self):
        data = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<playground version='6.0' target-platform='ios' requires-full-environment='true' display-mode='raw'>
    <pages>
        <page name='The first approach'/>
        <page name='Fixing our first approach'/>
        <page name='Targeted saving'/>
    </pages>
</playground>'''
        stream = StringIO(data)

        files_list = playgroundExportToMarkdown.listFilesFromXCPlaygroundData(stream)
        self.assertIsNotNone(files_list)
        self.assertEqual(3, len(files_list))
        self.assertEqual('Pages/The first approach.xcplaygroundpage/Contents.swift', files_list[0])

        stream.close()

    def testExportPageContentToMarkdown(self):
        intput_stream = StringIO(r'''//: Before test line
Swift code
//: After test line
''')
        expected_output_string = r'''Before test line
```Swift
Swift code
```
After test line
'''
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)
        
        self.assertEqual(expected_output_string, output_stream.getvalue())

        output_stream.close()
        intput_stream.close()

if __name__ == '__main__':
    unittest.main()
