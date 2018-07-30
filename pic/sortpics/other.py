from PIL import Image
from sortpics.meta import ImageMetaData
from sortpics.meta import MetaFile
from datetime import datetime
from pprint import pprint
import time, os

class SortOther(MetaFile):

    def __init__(self, img_path):
        super(ImageMetaData, self).__init__(img_path)
        
    def path(self):
        return self.img_path
    def date(self):
        return datetime.now()

    def table(self):
        return 'other';

