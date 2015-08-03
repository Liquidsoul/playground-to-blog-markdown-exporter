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

    def testExportPageContentToMarkdown_fullMarkdown(self):
        intput_stream = StringIO('''//: This is a markdown text
//: on multiple
//: lines.
''')
        expected_output_string = '''This is a markdown text
on multiple
lines.
'''
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)

        self.assertEqual(expected_output_string, output_stream.getvalue(), msg=">>>\n%s\n===\n%s\n<<<'" % (expected_output_string, output_stream.getvalue()))

        output_stream.close()
        intput_stream.close()

    def testExportPageContentToMarkdown_codeNoLineBreaks(self):
        intput_stream = StringIO('''//: This is the line before
Swift code
//: This is the line after
''')
        expected_output_string = '''This is the line before
%(start_code_tag)s
Swift code
%(end_code_tag)s
This is the line after
''' % {
    'start_code_tag': playgroundExportToMarkdown.start_code_tag,
    'end_code_tag': playgroundExportToMarkdown.end_code_tag
}
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)

        self.assertEqual(expected_output_string, output_stream.getvalue(), msg=">>>\n%s\n===\n%s\n<<<'" % (expected_output_string, output_stream.getvalue()))

        output_stream.close()
        intput_stream.close()

    def testExportPageContentToMarkdown_codeWithEmptyLines(self):
        intput_stream = StringIO(r'''//: Before test line
Swift code first line

Swift code last line
//: After test line
''')
        expected_output_string = r'''Before test line
%(start_code_tag)s
Swift code first line

Swift code last line
%(end_code_tag)s
After test line
''' % {
    'start_code_tag': playgroundExportToMarkdown.start_code_tag,
    'end_code_tag': playgroundExportToMarkdown.end_code_tag
}
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)

        self.assertEqual(expected_output_string, output_stream.getvalue(), msg=">>>\n%s\n===\n%s\n<<<'" % (expected_output_string, output_stream.getvalue()))

        output_stream.close()
        intput_stream.close()

    def testExportPageContentToMarkdown_removePageLinks(self):
        intput_stream = StringIO(r'''//: [Next](@next)
//: Some Markdown
//: [Previous](@previous)
''')
        expected_output_string = r'''Some Markdown
'''
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)
        
        self.assertEqual(expected_output_string, output_stream.getvalue(), msg=">>>\n%s\n===\n%s\n<<<'" % (expected_output_string, output_stream.getvalue()))

        output_stream.close()
        intput_stream.close()

    def testExportPageContentToMarkdown_emptylinesBetweenMarkdownBlocks(self):
        intput_stream = StringIO(r'''//: First markdown block
//: some more markdown

//: Second markdown block
''')
        expected_output_string = r'''First markdown block
some more markdown

Second markdown block
'''
        output_stream = StringIO()

        playgroundExportToMarkdown.exportPageContentToMarkdown(intput_stream, output_stream)
        
        self.assertEqual(expected_output_string, output_stream.getvalue(), msg=">>>\n%s\n===\n%s\n<<<'" % (expected_output_string, output_stream.getvalue()))

        output_stream.close()
        intput_stream.close()

if __name__ == '__main__':
    unittest.main()
