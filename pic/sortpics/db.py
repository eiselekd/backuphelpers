import sqlite3
from pprint import pprint
from sortpics.img import SortImage
from sortpics.mpg import SortMovie
from sortpics.other import SortOther
from sortpics.classify import classify
import subprocess

class picdb(object):
    
    def __init__(self, db='sortpics.db'):
        self.conn = sqlite3.connect('sortpics.db')
        self.c = self.conn.cursor()
        self.createTable('pics')
        self.createTable('movies')
        self.createTable('other')

    def createTable(self,n):
        self.c.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = '%s'" %(n))
        (cnt,)=self.c.fetchone()
        if cnt == 0:
            self.c.execute("CREATE TABLE %s (id integer primary key autoincrement , date DATETIME, path text, md5 text)" %(n))
            self.conn.commit()
        
    def rel(self):
        self.conn.close()

    def getDup(self,i,t):
        m = i.md5()
        self.c.execute("Select (id,path) from %s where (md5=='%s')" %(t,m))
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
        (dup,path,tab) = self.getDup(i,i.table())
        if dup is None:
            (d,p,t,m) = (i.date(), i.path(), i.table(),i.md5())
            self.c.execute(('insert into %s(id,date,path,md5) values (NULL,?,?,?)' %(t)), (d.strftime('%Y-%m-%d %H:%M:%S'), p, m))
            self.conn.commit()
        else:
            print("Already");
    def addImage(self,i):
        self.addToTable(i)

    def addMovie(self,i):
        self.addToTable(i)

    def addOther(self,i):
        self.addToTable(i)
        
    def addFile(self,fn):
        f = MetaFile(fn)
        (i,d) = searchDup(f)
        if not (searchDup(f) is None):
            self.addOther(SortOther(fn,comment=('dup of %s' %(d))))
        m = classify(fn)
        if isinstance(m,SortImage):
            self.addImage(m);
        elif isinstance(m,SortMovie):
            self.addMovie(m);
        elif isinstance(m,SortOther):
            self.addOther(m);
        else:
            raise(Exception("Unknown type"))
