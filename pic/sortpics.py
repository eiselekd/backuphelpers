#!/usr/bin/python3
from sortpics.img import SortImage
from sortpics.db import picdb
from pprint import pprint
import argparse, os, shutil, re
from os.path import expanduser
home = expanduser("~")

def copyfunc(args):
    ismovies=args.ismovies
    db = picdb(args,db='sortpics.db')
    if ismovies:
        r = db.movs()
    else:
        r = db.pics()
    b = db.getbase()
    dest = b
    hist = os.path.join(b,"history")
    with open(hist, "a") as f:
        for i in r:
            dest = os.path.abspath(dest)
            (d,r0,r1) = i.canonicalsuffix()
            if ismovies:
                cd = os.path.join(dest, r0, "movies")
            else:
                cd = os.path.join(dest, r0, "photos")
            ad = os.path.join(dest, r0, "album.yml")
            if not os.path.isdir(cd):
                os.makedirs(cd)
            if not os.path.exists(ad):
                f1 = d.strftime('%Y-%m-%d')
                f0 = d.strftime('%Y-%m-%dT%H:%M:%S')
                m = """---
title: %s
album_date:
properties:
copyright:
coverimage:
creation_time: "%s"
modification_time: "%s"

photos:

""" %(f1,f0,f0)
                with open(ad, 'w') as fh:
                    fh.write(m)
            if args.dryrun == 0:
                d = os.path.join(cd, r1)
                if os.path.isfile(d) and (os.path.getsize(d) == os.path.getsize(i.path())):
                    print ("already copied %s->%s" %(i.path(), d))
                else:
                    print ("copy %s->%s" %(i.path(), d))
                    shutil.copyfile(i.path(), d)
                    f.write("\"%s\" \"%s\"\n" %(i.path(), d))
            
    
def listpics(args):
    db = picdb(args,db='sortpics.db')
    r = db.pics()
    for i in r:
        (d,r0,r1) = i.canonicalsuffix()
        print("/".join((r0,r1)))
    

def listmovs(args):
    db = picdb(args,db='sortpics.db')
    r = db.movs()
    for i in r:
        (d,r0,r1) = i.canonicalsuffix()
        p = i.path()
        print("/".join((r0,r1))+":"+p)
    

def addfunc(args):
    print("addfunc");
    filters = []
    if os.path.isfile(args.exclude):
        with open(args.exclude) as f:
            lines = f.readlines()
            for r in lines:
                print("Add filter: " + r.strip());
            filters = [ re.compile(r.strip()) for r in lines ]
    db = picdb(args,db='sortpics.db')
    for dn in args.files:
        if os.path.isdir(dn):
            for r, d, files in os.walk(dn):
                for f in files:
                    skip=False
                    ffn = os.path.join(r, f);
                    for filt in filters:
                        m = filt.search(ffn)
                        #print(m)
                        if m:
                            skip=True
                            #print("Skipping %s" %(ffn))
                            break
                    if not skip:
                        db.addFile(ffn);
        elif os.path.isfile(dn):
            db.addFile(dn);
        else:
            raise(Exception("Unknown file/dir %s" %(dn)))

parser = argparse.ArgumentParser(description='sortpics')
parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
parser.add_argument('--sortpic', '-b', dest='sortpic', type=str, default=None)

subparsers = parser.add_subparsers(help='sub-commands help')

# create the parser for the "listpics" command
parser_list = subparsers.add_parser('listpics', help='list help')
parser_list.set_defaults(func=listpics)

# create the parser for the "listmovs" command
parser_list = subparsers.add_parser('listmovs', help='list help')
parser_list.set_defaults(func=listmovs)

# create the parser for the "add" command
parser_add = subparsers.add_parser('add', help='add help')
parser_add.add_argument('--exclude', '-e', dest='exclude', action='count', default="sortpics_exclude.txt")
parser_add.add_argument('files', nargs='*', default=[])
parser_add.set_defaults(func=addfunc)

# create the parser for the "copy" command
parser_add = subparsers.add_parser('copy', help='add help')
parser_add.add_argument('--dry-run', '-r', dest='dryrun', action='count', default=0)
parser_add.add_argument('--ismovies', '-m', dest='ismovies', action='count', default=0)

parser_add.set_defaults(func=copyfunc)

args = parser.parse_args()
args.func(args)




    
