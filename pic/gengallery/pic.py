from PIL import Image
import os
from mako.template import Template

class pic(object):

    hugo = Template("""{{< photo href="${pic.get_path()}" thumbUrl="${pic.get_thumb()}" rotation="${pic.get_rotation()}" dimension="${pic.get_dim()}" >}}""")

    def __init__(self, album, path):
        self._album = album
        self._path = path
        self._rotation = 0
        self._fn = os.path.basename(path)
        super(pic, self).__init__()
        self.gen_thumb()

    def get_dim(self):
        return "{}x{}".format(self._dim_w,self._dim_h);
        
    def get_rotation(self):
        return str(self._rotation)
        
    def get_hugotag(self):
        m = pic.hugo.render(pic=self);
        return m

    def get_path(self):
        return self._album.rel_path(self._path);

    def get_thumb(self):
        return self._album.rel_path(self._thumb);
        
    def gen_thumb(self):
        if not os.path.exists(self._album.thumb_dir()):
            os.makedirs(self._album.thumb_dir())
        fn = os.path.join(self._album.thumb_dir(), "thumb_" + self._fn)
        self._thumb = fn

        i = Image.open(self._path);
        self._dim_w,self._dim_h = i.size 
        rottyp = None
        if hasattr(i, '_getexif'):
            orientation = 0x0112
            exif = i._getexif()
            if exif is not None and orientation in exif:
                orientation = exif[orientation]
                rotations = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }
                if orientation in rotations:
                    rottyp = rotations[orientation]
                    deg = {
                        3: 180,
                        6: 270,
                        8: 90
                    }
                    self._rotation = deg[orientation]
        
        if not (os.path.exists(fn)):
            i.thumbnail((300,300)) 
            #if not (rottyp is None):
            #    i.transpose(rottyp).save(fn)
            #else:
            i.save(fn);
