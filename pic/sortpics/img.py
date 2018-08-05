from PIL import Image
from sortpics.meta import MetaFile
from datetime import datetime
from pprint import pprint
from pyexiftool.exiftool import ExifTool
import time, atexit


class SortImage(MetaFile):
    
    et = ExifTool()
    et.start()
    def etclean():
        SortImage.et.terminate()
    atexit.register(etclean)

    def __init__(self, img_path):
        self._exif_data = None
        super(SortImage, self).__init__(img_path)

    def get_exif_data(self):
        if self._exif_data is None:
            self._exif_data = SortImage.et.get_metadata(self.img_path)
        #pprint(self._exif_data)
        return self._exif_data
        
    def date(self):
        exif_data = self.get_exif_data()
        #;
        if "EXIF:DateTimeOriginal" in exif_data:
            try:
                d = datetime.strptime(exif_data['EXIF:DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
                return d
            except:
                pass
        if "EXIF:DateTime" in exif_data:
            try:
                d = datetime.strptime(exif_data['EXIF:DateTime'], '%Y:%m:%d %H:%M:%S')
                return d
            except:
                pass
        pprint(exif_data)
        print("No date found for %s" %(self.path()))
        return datetime.now()
        #ds = d.strftime('%Y-%m-%d %H:%M:%S')
        #n = time.mktime(d.timetuple())
        #return datetime.fromtimestamp(n).strftime('%Y-%m-%d %H:%M:%S')

    def path(self):
        return self.img_path

    def table(self):
        return 'pics';

    def hasid(self):
        exif_data = SortImage.et.get_metadata(self.img_path)
        for j in [ 'EXIF:ImageUniqueID', 'MakerNotes:ImageUniqueID' ]:
            if j in exif_data:
                if (len(exif_data[j]) > 16):
                    return exif_data[j]
        return None

    def updateid(self):
        m = self.hasid()
        if m is None:
            m = MetaFile.md5(self)
            p = map(fsencode,["-EXIF:ImageUniqueID+=%s" %(m), self.img_path])
            SortImage.et.execute(*p)
    
    def md5(self):
        m = self.hasid()
        if not m is None:
            return m
        return MetaFile.md5(self)
        
        
