from datetime import datetime
from pprint import pprint
import time
from sortpics.meta import MetaFile
from pyexiftool.exiftool import ExifTool
import time, atexit, re

class SortMovie(MetaFile):

    et = ExifTool()
    et.start()
    def etclean():
        SortMovie.et.terminate()
    atexit.register(etclean)
    
    def __init__(self, img_path):
        self._exif_data = None
        super(SortMovie, self).__init__(img_path)

    def get_exif_data(self):
        if self._exif_data is None:
            self._exif_data = SortMovie.et.get_metadata(self.img_path)
        #pprint(self._exif_data)
        return self._exif_data

    def path(self):
        return self.img_path
    def table(self):
        return 'movies';
    def date(self):
        exif_data = self.get_exif_data()
        for i in ['QuickTime:CreateDate','QuickTime:MediaCreateDate','File:FileModifyDate']:
            if i in exif_data:
                try:
                    a = exif_data[i]
                    a = re.sub(r"\+[0-9]+:[0-9]+$","",a);
                    d = datetime.strptime(a, '%Y:%m:%d %H:%M:%S')
                    return d
                except Exception as e:
                    print(str(e))
        pprint(exif_data)
        print("No date found for %s" %(self.path()))
        return datetime.now()
        #raise(Exception("Cannot find date for %s" %(self.path())))
