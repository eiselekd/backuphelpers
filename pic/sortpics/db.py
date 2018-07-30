import sqlite3
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
            self.c.execute("CREATE TABLE %s (date DATETIME, path text)" %(n))
            self.conn.commit()
        
    def rel(self):
        self.conn.close()

    def addToTable(self,i):
        (d,p,t) = (i.date(), i.path(), i.table())
        self.c.execute(('insert into %s values (?,?)' %(t)), (d.strftime('%Y-%m-%d %H:%M:%S'), p))
        self.conn.commit()

        
    def addImage(self,i):
        self.addToTable(i)

    def addMovie(self,i):
        self.addToTable(i)

    def addOther(self,i):
        self.addToTable(i)
        
    def addFile(self,fn):
        m = classify(fn)
        if isinstance(m,SortImage):
            self.addImage(m);
        elif isinstance(m,SortMovie):
            self.addMovie(m);
        elif isinstance(m,SortOther):
            self.addOther(m);
        else:
            raise(Exception("Unknown type"))
