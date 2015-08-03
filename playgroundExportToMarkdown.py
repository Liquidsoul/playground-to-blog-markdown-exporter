#! env python

import re

start_code_tag = r'{% highlight swift linenos %}'
end_code_tag = r'{% endhighlight %}'
jekyll_page_export = True
jekyll_page_layout = 'post'

def pathsFromPageNameList(page_name_list):
    return map(lambda x: 'Pages/' + x + '.xcplaygroundpage/Contents.swift', page_name_list)

def listFilesFromXCPlaygroundData(data_stream):
    import xml.etree.ElementTree as ET
    tree = ET.parse(data_stream)
    root = tree.getroot()
    if root.tag != 'playground':
        return None
    pages = None
    for root_child in root.getchildren():
        if root_child.tag == 'pages':
            pages = root_child
            break
    if pages is None:
        return None
    page_name_list = []
    for page_child in pages.getchildren():
        if page_child.tag != 'page' or 'name' not in page_child.attrib:
            return None
        page_name_list.append(page_child.attrib['name'])
    return pathsFromPageNameList(page_name_list)

def exportTitleFromLines(lines, output_stream):
    title_pattern = re.compile(r'(\s*)//:\s#\s*(?P<title>.*)')
    for l in lines:
        match = title_pattern.match(l)
        if match is not None:
            output_stream.write('---\nlayout: %(layout)s\ntitle: %(title)s\n---\n' % {'layout': jekyll_page_layout, 'title': match.group('title')})
            lines.remove(l)
            return

def exportPageContentToMarkdown(content_stream, output_stream):
    lines = content_stream.readlines()
    empty_line_pattern = re.compile(r'^\s*$')
    markdown_pattern = re.compile(r'(\s*)//:\s(?P<content>.*)')
    page_links_pattern = re.compile(r'\[(Next|Previous)\]\(@(next|previous)\)')
    code_block = False
    if jekyll_page_export:
        exportTitleFromLines(lines, output_stream)
    for l in lines:
        if page_links_pattern.search(l) is not None:
            # we skip lines containing playground page links
            continue

        if empty_line_pattern.match(l) is not None:
            output_stream.write(l)
            continue
        match = markdown_pattern.match(l)
        if match is None:
            if not code_block:
                code_block = True
                output_stream.write(start_code_tag + '\n')
            output_stream.write(l)
        else:
            if code_block:
                code_block = False
                output_stream.write(end_code_tag + '\n')
            output_stream.write(match.group('content') + '\n')
    return True

def xcplaygroundStreamForPlaygroundPath(playground_path):
    xcplayground_path = playground_path + '/contents.xcplayground'
    if not os.path.exists(xcplayground_path):
        return None
    return open(xcplayground_path, 'r')


def exportPlayground(playground_path, output_stream):
    xcplayground_stream = xcplaygroundStreamForPlaygroundPath(playground_path)
    if xcplayground_stream is None:
        return False
    files_path_list = listFilesFromXCPlaygroundData(xcplayground_stream)
    xcplayground_stream.close()

    for path in files_path_list:
        with open(playground_path + '/' + path, 'r') as content_stream:
            if not exportPageContentToMarkdown(content_stream, output_stream):
                return False
    return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Export script that convert a playground into a markdown file.')
    parser.add_argument(dest='playground', help='The playground to export.')
    parser.add_argument('-o', '--output', dest='output_file', help='File name to export to. If none is provided, output to stdout.')

    args = parser.parse_args()

    import sys
    import os

    if args.output_file is None:
        if not exportPlayground(args.playground, sys.stdout):
            os.exit(1)
    else:
        with open(args.output_file, 'w') as output_stream:
            if not exportPlayground(args.playground, output_stream):
                os.exit(1)
