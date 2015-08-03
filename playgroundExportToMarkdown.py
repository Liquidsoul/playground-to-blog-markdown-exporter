#! env python

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

def exportPageContentToMarkdown(content_stream, output_stream):
    lines = content_stream.readlines()
    import re
    markdown_pattern = re.compile(r'(\s*)//:\s(?P<content>.*)')
    code_block = False
    for l in lines:
        match = markdown_pattern.match(l)
        if match is None:
            if not code_block:
                code_block = True
                output_stream.write('```Swift\n')
            output_stream.write(l)
        else:
            if code_block:
                code_block = False
                output_stream.write('```\n')
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
