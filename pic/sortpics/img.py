from PIL import Image
from sortpics.meta import ImageMetaData
from datetime import datetime
from pprint import pprint
import time

class SortImage(ImageMetaData):

    def __init__(self, img_path):
        super(SortImage, self).__init__(img_path)
        
    def date(self):
        exif_data = self.get_exif_data()
        #pprint(exif_data);

        if "DateTimeOriginal" in exif_data:
            d = datetime.strptime(exif_data['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            return d

        return datetime.now()
        #ds = d.strftime('%Y-%m-%d %H:%M:%S')
        #n = time.mktime(d.timetuple())
        #return datetime.fromtimestamp(n).strftime('%Y-%m-%d %H:%M:%S')
    def path(self):
        return self.img_path

    def table(self):
        return 'pics';
