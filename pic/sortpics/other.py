from PIL import Image
from sortpics.meta import ImageMetaData
from sortpics.meta import MetaFile
from datetime import datetime
from pprint import pprint
import time, os

class SortOther(MetaFile):

    def __init__(self, img_path, comment=""):
        super(SortOther, self).__init__(img_path, comment)
        
    def path(self):
        return self.img_path

    def table(self):
        return 'other';

