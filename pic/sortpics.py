#!/usr/bin/python3
from sortpics.img import SortImage
from sortpics.db import picdb
from pprint import pprint
import argparse, os, shutil
from os.path import expanduser
home = expanduser("~")

def copyfunc(args):
    db = picdb(args,db='sortpics.db')
    r = db.pics()
    b = db.getbase()
    dest = b # os.path.join(b,"Pictures")
    hist = os.path.join(b,"history")
    with open(hist, "a") as f:
        for i in r:
            dest = os.path.abspath(dest)
            (d,r0,r1) = i.canonicalsuffix()
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
        print("/".join((r0,r1)))
    

def addfunc(args):
    print("addfunc");
    db = picdb(args,db='sortpics.db')
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
parser_add.add_argument('files', nargs='*', default=[])
parser_add.set_defaults(func=addfunc)

# create the parser for the "copy" command
parser_add = subparsers.add_parser('copy', help='add help')
parser_add.add_argument('--dry-run', '-r', dest='dryrun', action='count', default=0)
parser_add.set_defaults(func=copyfunc)

args = parser.parse_args()
args.func(args)




    
