from sortpics.img import SortImage
from sortpics.mpg import SortMovie
from sortpics.other import SortOther
from datetime import datetime
from pprint import pprint
import time, subprocess, re

def classify(path):
    p = subprocess.check_output(['file', path]).decode('utf-8')
    if re.search('JPEG image data', p) and not path.endswith("THM"):
        return SortImage(path);
    elif re.search('Apple QuickTime movie', p):
        return SortMovie(path);
    return SortOther(path)
    
    
