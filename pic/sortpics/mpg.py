from datetime import datetime
from pprint import pprint
import time
from sortpics.meta import MetaFile
from pyexiftool.exiftool import ExifTool

class SortMovie(MetaFile):

    def __init__(self, img_path):
        super(SortMovie, self).__init__(img_path)
    def path(self):
        return self.img_path
    def table(self):
        return 'movies';
    def date(self):
        with ExifTool() as et:
            exif_data = et.get_metadata(self.img_path)
            for i in ['QuickTime:CreateDate','QuickTime:MediaCreateDate']:
                if i in exif_data:
                    d = datetime.strptime(exif_data[i], '%Y:%m:%d %H:%M:%S')
                    return d
        pprint(exif_data)
        print("No date found for %s" %(self.path()))
        return datetime.now()
        #raise(Exception("Cannot find date for %s" %(self.path())))
