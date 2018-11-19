from sortpics.img import SortImage
from sortpics.mpg import SortMovie
from sortpics.other import SortOther
from datetime import datetime
from pprint import pprint
import time, subprocess, re

def classify(path):
    try:
        p = subprocess.check_output(['file', path]).decode('utf-8')
    except Exception as e:
        print ("File type error");
        return SortOther(path)
    if re.search('JPEG image data', p) and not path.endswith("THM"):
        return SortImage(path);
    elif re.search('Apple QuickTime movie', p) or re.search('MPEG', p):
        return SortMovie(path);
    else:
        print("unknown format %s : %s " %(path,p))
    return SortOther(path)
    
    
