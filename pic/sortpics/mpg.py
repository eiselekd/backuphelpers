from datetime import datetime
from pprint import pprint
import time
from sortpics.meta import MetaFile

class SortMovie(MetaFile):

    def __init__(self, img_path):
        super(ImageMetaData, self).__init__(img_path)
        
    def path(self):
        return self.img_path

    def table(self):
        return 'movies';
