import sqlite3
from pprint import pprint
import os
from sortpics.meta import MetaFile
from sortpics.img import SortImage
from sortpics.mpg import SortMovie
from sortpics.other import SortOther
from sortpics.classify import classify
import subprocess

class picdb(object):

    def __init__(self, args, db='sortpics.db'):
        self._args = args
        self._db = db
        h = self.getbase()
        self.conn = sqlite3.connect(os.path.join(h,db))
        self.c = self.conn.cursor()
        self.createTable('pics')
        self.createTable('movies')
        self.createTable('other')

    def getbase(self):
        h = os.environ.get("SORTPICHOME")
        if not (self._args.sortpic is None):
            h = self._args.sortpic
        if h is None:
            h = "."
        return h

    def getdestbase(self):
        h = os.environ.get("SORTPICDEST")
        if not (self._args.dest is None):
            h = self._args.dest
        if h is None:
            h = "."
        return h


    def createTable(self,n):
        self.c.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = '%s'" %(n))
        (cnt,)=self.c.fetchone()
        if cnt == 0:
            self.c.execute("CREATE TABLE %s (id integer primary key autoincrement , date DATETIME, path text, md5 text, comment text)" %(n))
            self.conn.commit()

    def rel(self):
        self.conn.close()

    def getDup(self,i,t):
        m = i.md5()
        self.c.execute("Select id, path from %s where (md5=='%s')" %(t,m))
        r=self.c.fetchall()
        if (len(r) > 0):
            return (r[0][0],r[0][1]);
        return (None,None)

    def searchDup(self,i):
        (picdup,p) = self.getDup(i, 'pics');
        if not (picdup is None):
            return (picdup, p, 'pics')
        (moviedup,p) = self.getDup(i, 'movies');
        if not (moviedup is None):
            return (moviedup, p, 'movies')
        return (None,None,None)

    def addToTable(self,i):
        (dup,path) = self.getDup(i,i.table())
        if dup is None:
            (d,p,t,m,c) = (i.date(), i.path(), i.table(),i.md5(),i.comment())
            self.c.execute(('insert into %s(id,date,path,md5,comment) values (NULL,?,?,?,?)' %(t)), (d.strftime('%Y-%m-%d %H:%M:%S'), p, m, c))
            self.conn.commit()
        else:
            print("Already present");

    def addImage(self,i):
        self.addToTable(i)
        #print(i.canonicalsuffix())

    def addMovie(self,i):
        self.addToTable(i)
        #print(i.canonicalsuffix())

    def addOther(self,i):
        self.addToTable(i)
        #print(i.canonicalsuffix())

    def testDup(self,fn):
        f = classify(fn)
        if isinstance(f,SortOther):
            return f
        (i,d,t) = self.searchDup(f)
        #print("Testdup %s : %s : %s" %(fn,f.md5(),f.date()))
        if not (i is None):
            return None
        if isinstance(f,SortImage):
            pass #print("#copy-img{}".format(fn))
        elif isinstance(f,SortMovie):
            pass #print("#copy-mov{}".format(fn))
        elif isinstance(f,SortOther):
            return None
        else:
            raise(Exception("Unknown type"))
        return f;

    def addFile(self,fn):
        f = classify(fn)
        if isinstance(f,SortOther):
            return
        (i,d,t) = self.searchDup(f)
        print("Process %s : %s : %s" %(fn,f.md5(),f.date()))
        if not (i is None):
            self.addOther(SortOther(fn,comment=('dup of %s' %(d))))
            return
        m = f
        if isinstance(m,SortImage):
            self.addImage(m);
        elif isinstance(m,SortMovie):
            self.addMovie(m);
        elif isinstance(m,SortOther):
            self.addOther(m);
        else:
            raise(Exception("Unknown type"))

    def pics(self):
        self.c.execute("SELECT path FROM pics ")
        r=self.c.fetchall()
        return [SortImage(x[0]) for x in r ]

    def movs(self):
        self.c.execute("SELECT path FROM movies ")
        r=self.c.fetchall()
        return [SortMovie(x[0]) for x in r ]
