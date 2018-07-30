from PIL import Image
from sortpics.meta import ImageMetaData
from datetime import datetime
from pprint import pprint
from pyexiftool.exiftool import ExifTool
import time, atexit


class SortImage(ImageMetaData):
    
    et = ExifTool()
    et.start()
    def etclean():
        SortImage.et.terminate()
    atexit.register(etclean)

    def __init__(self, img_path):
        super(SortImage, self).__init__(img_path)
        
    def date(self):
        exif_data = self.get_exif_data()
        #;
        if "DateTimeOriginal" in exif_data:
            d = datetime.strptime(exif_data['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            return d
        if "DateTime" in exif_data:
            d = datetime.strptime(exif_data['DateTime'], '%Y:%m:%d %H:%M:%S')
            return d
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
                return exif_data[j]
        return None

    def updateid(self):
        m = self.hasid()
        if m is None:
            m = ImageMetaData.md5(self)
            p = map(fsencode,["-EXIF:ImageUniqueID+=%s" %(m), self.img_path])
            SortImage.et.execute(*p)
    
    def md5(self):
        m = self.hasid()
        if not m is None:
            return m
        return ImageMetaData.md5(self)
        
        
