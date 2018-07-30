#!/usr/bin/python3
from sortpics.img import SortImage
from sortpics.db import picdb
from pprint import pprint
import argparse, os, shutil
from os.path import expanduser
home = expanduser("~")

def copyfunc(args):
    db = picdb(db='sortpics.db')
    r = db.pics()
    for i in r:
        dest = os.path.abspath(args.dest)
        d = os.path.join(dest, i.canonicalsuffix())
        cd = os.path.dirname(d)
        if not os.path.isdir(cd):
            os.makedirs(cd)
        if args.dryrun == 0:
            print ("copy %s->%s" %(i.path(), d))
            shutil.copyfile(i.path(), d)
    
def listpics(args):
    db = picdb(db='sortpics.db')
    r = db.pics()
    for i in r:
        print(i.canonicalsuffix())
    

def listmovs(args):
    db = picdb(db='sortpics.db')
    r = db.movs()
    for i in r:
        print(i.canonicalsuffix())
    

def addfunc(args):
    print("addfunc");
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

parser = argparse.ArgumentParser(description='sortpics')
parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
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
parser_add.add_argument('--dest', '-d', dest='dest', type=str, default=("%s/Pictures"%(home)))
parser_add.add_argument('--dry-run', '-r', dest='dryrun', action='count', default=0)
parser_add.set_defaults(func=copyfunc)

args = parser.parse_args()
args.func(args)




    
