#!/usr/bin/env python3

import argparse
import re
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageColor

re_wh = re.compile(r'^([0-9]+)x([0-9]+)$')

size_using = """
The size shoud be [width]x[height] for example :300x400 . 
When width == heigth just use size number directly .
For example : 128 means a 128x128 size
"""


def create_cmd_parser(subparsers):
    parser_resize = subparsers.add_parser(
        'resize', help='resize a pic',
    )
    parser_resize.add_argument("-f",
                               "--file",
                               help="The file to be resize")
    parser_resize.add_argument("-o",
                               "--outfile",
                               help="The output file resized")
    resize_group = parser_resize.add_mutually_exclusive_group()
    resize_group.add_argument("-s",
                              "--size",
                              help=size_using)
    resize_group.add_argument("-a",
                              "--app",
                              action='store_true',
                              help=size_using)
    parser_resize.set_defaults(on_args_parsed=_on_args_parsed)


def _on_args_parsed(args):
    params = vars(args)
    app = params['app']
    infile = params['file']
    outfile = params['outfile']
    size = params['size']

    if app:
        _on_app_parsed(infile, outfile)
    else:
        _on_size_parsed(infile, outfile, size)


def _on_app_parsed(infile, outfile):
    width = 192
    height = 192
    resize(infile, width, height, outfile)


def _on_size_parsed(infile, outfile, size):
    m_wh = re_wh.match(size)
    if not m_wh:
        print(size_using)
        exit(2)

    width = m_wh.group(1)
    height = m_wh.group(2)
    bar_filename, ext = os.path.splitext(infile)
    filename_new = outfile if outfile else f"{bar_filename}_{width}x{height}{ext}"
    resize(infile, width, height, filename_new)


def resize(filename, width, height, outputfile):
    print(f"{filename} -> {outputfile}")
