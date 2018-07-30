#!/usr/bin/python3
import argparse, os
from pprint import pprint
from sortpics.img import SortImage
from pyexiftool.exiftool import ExifTool
from pyexiftool.exiftool import fsencode
import tempfile, sys

parser = argparse.ArgumentParser(description='sortpics')
parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
parser.add_argument('--read', '-r', dest='read', action='count', default=0)
parser.add_argument('--update', '-w', type=str, dest='update', default=None)
parser.add_argument('file')
args = parser.parse_args()
f = args.file

with ExifTool() as et:
    exif_data = et.get_metadata(f)
    if (args.update):
        p = map(fsencode,["-EXIF:ImageDescription<=%s" %(args.update), f])
        et.execute(*p)
    else:
        if 'EXIF:ImageDescription' in exif_data:
            sys.stdout.write(exif_data['EXIF:ImageDescription'])
