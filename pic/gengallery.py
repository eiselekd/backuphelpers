#!/usr/bin/python3
import argparse, os
import yaml
from gengallery.album import album

parser = argparse.ArgumentParser(description='sortpics')
parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
parser.add_argument('--hugo', '-H', dest='hugo', required=True, type=str, default=None)
parser.add_argument('dir')
args = parser.parse_args()

hugoidx = args.hugo.index("content/")
staticidx = args.dir.index("static/")+len("static/")
staticprefix=args.dir[staticidx:]
args.staticprefix = staticidx;

a = [ album(args, os.path.join(args.dir,d)) for d in os.listdir(args.dir) \
      if os.path.isdir(os.path.join(args.dir,d)) ]

for i in a:
    i.gen_album()


