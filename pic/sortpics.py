#!/usr/bin/python3
from sortpics.img import SortImage
from sortpics.db import picdb
import argparse, os

parser = argparse.ArgumentParser(description='sortpics')
parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
parser.add_argument('files', nargs='*', default=[])
args = parser.parse_args()

db = picdb(db='sortpics.db')

for dn in args.files:
    if os.path.isdir(dn):
        for r, d, files in os.walk(dn):
            for f in files: 
                ffn = os.path.join(r, f);
                db.addFile(ffn);
    elif os.path.isfile(dn):
        db.addFile(dn);
    else:
        raise(Exception("Unknown file/dir %s" %(dn)))
