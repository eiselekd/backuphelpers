from PIL import Image
from sortpics.meta import ImageMetaData
from datetime import datetime
from pprint import pprint
import time

class SortOther(object):

    def __init__(self, img_path):
        img_path = os.path.abspath(img_path)
        self.img_path = img_path
        super(object, self).__init__()
        
    def path(self):
        return self.img_path

    def table(self):
        return 'other';

