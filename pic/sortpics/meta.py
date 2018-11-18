# https://www.codingforentrepreneurs.com/blog/extract-gps-exif-images-python/

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import os, hashlib, time

class MetaFile(object):
    def __init__(self, img_path, comment=""):
        img_path = os.path.abspath(img_path)
        self.img_path = img_path
        self._md5sum = None
        self._comment = comment
    def setpath(self,img_path):
        img_path = os.path.abspath(img_path)
        self.img_path = img_path
    def md5(self):
        if not (self._md5sum is None):
            return self._md5sum
        hash_md5 = hashlib.md5()
        with open(self.img_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self._md5sum = hash_md5.hexdigest()
        return self._md5sum
    def comment(self):
        return self._comment;
    def date(self):
        d0 = os.path.getctime(self.img_path)
        try:
            d = datetime.fromtimestamp(d0)
        except:
            d = time.mktime(d.timetuple())
        return d

    def canonicalsuffix(self):
        d = self.date()
        p = d.strftime('%Y-%m-%d_%H_%M_')
        b = os.path.basename(self.img_path)
        if (b.startswith(p)):
            fn = (d,d.strftime('%Y-%m-%d'),b)
        else:
            r1 = d.strftime('%Y-%m-%d_%H_%M_')
            fn = (d,d.strftime('%Y-%m-%d'),"%s%s" %(r1,b))
        return fn
    
