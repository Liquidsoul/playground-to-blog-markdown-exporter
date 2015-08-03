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

    def _exportPageContentToMarkdownTest(self, input_string, expected_output_string):
        intput_stream = StringIO(input_string)
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)

        self.assertEqual(expected_output_string, output_stream.getvalue(), msg=">>>\n%s\n===\n%s\n<<<'" % (expected_output_string, output_stream.getvalue()))

        output_stream.close()
        intput_stream.close()

    def testExportPageContentToMarkdown_exportJekyllTitle(self):
        self._exportPageContentToMarkdownTest('''//: # This is the title we want
//: This is markdown text.
''', '''---
layout: post
title: This is the title we want
---
This is markdown text.
''')

    def testExportPageContentToMarkdown_fullMarkdown(self):
        self._exportPageContentToMarkdownTest('''//: This is a markdown text
//: on multiple
//: lines.
''', '''This is a markdown text
on multiple
lines.
''')

    def testExportPageContentToMarkdown_codeNoLineBreaks(self):
        self._exportPageContentToMarkdownTest('''//: This is the line before
Swift code
//: This is the line after
''', '''This is the line before
%(start_code_tag)s
Swift code
%(end_code_tag)s
This is the line after
''' % {
    'start_code_tag': playgroundExportToMarkdown.start_code_tag,
    'end_code_tag': playgroundExportToMarkdown.end_code_tag
})

    def testExportPageContentToMarkdown_codeWithEmptyLines(self):
        self._exportPageContentToMarkdownTest('''//: Before test line
Swift code first line

Swift code last line
//: After test line
''', '''Before test line
%(start_code_tag)s
Swift code first line

Swift code last line
%(end_code_tag)s
After test line
''' % {
    'start_code_tag': playgroundExportToMarkdown.start_code_tag,
    'end_code_tag': playgroundExportToMarkdown.end_code_tag
})

    def testExportPageContentToMarkdown_removePageLinks(self):
        self._exportPageContentToMarkdownTest('''//: [Next](@next)
//: Some Markdown
//: [Previous](@previous)
''', '''Some Markdown
''')

    def testExportPageContentToMarkdown_emptylinesBetweenMarkdownBlocks(self):
        self._exportPageContentToMarkdownTest('''//: First markdown block
//: some more markdown

//: Second markdown block
''', '''First markdown block
some more markdown

Second markdown block
''')

if __name__ == '__main__':
    unittest.main()
