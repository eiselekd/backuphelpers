#!/usr/bin/python3
import argparse, os
from pprint import pprint
from sortpics.img import SortImage
from pyexiftool.exiftool import ExifTool
from pyexiftool.exiftool import fsencode
import tempfile, sys, hashlib

parser = argparse.ArgumentParser(description='sortpics')
parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
parser.add_argument('--update', '-u', dest='update', action='count', default=0)
parser.add_argument('file')
args = parser.parse_args()
f = args.file

def md5(img_path):
    hash_md5 = hashlib.md5()
    with open(img_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

with ExifTool() as et:
    exif_data = et.get_metadata(f)
    if (args.verbose):
        pprint(exif_data)
    m = ""
    for j in [ 'EXIF:ImageUniqueID', 'MakerNotes:ImageUniqueID' ]:
        if j in exif_data:
            m = exif_data[j]
    if m == "":
        if (args.update):
            m = md5(f)
            p = map(fsencode,["-EXIF:ImageUniqueID+=%s" %(m), f])
            et.execute(*p)
    sys.stdout.write(m)

            
