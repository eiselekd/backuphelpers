import os
import yaml
from gengallery.pic import pic
from mako.template import Template
import string, re

class album(object):

    preview = Template("""
	<div class="grid albumitem" >
            % for p in pics:
               <div class="grid-item"><img src="${p.get_thumb()}"> </div>
            % endfor
	    <div class="banner">
		<div class="albumdate">
		    ${album.get_date()}
		</div>
		<div class="albumtitle">
		    ${album.get_name()}
		</div>
		
	    </div>
	</div>
    """)
    
    albumpage = Template("""
<!DOCTYPE html>
<html>
<head>
 <title>jQuery Isotope</title>
 <link rel="stylesheet" href="css/style.css">
 <script src="http://code.jquery.com/jquery-latest.js" type="text/javascript"></script>
 <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.js"></script>
</head>
<body>

	<div class="grid albumitem" >
            % for p in pics:
               <div class="grid-item"><img width="100" src="${p.get_thumb()}"> </div>
            % endfor
	</div>
    

    <script type="text/javascript">

     $('.grid').isotope({
	 layoutMode: 'masonry',
	 itemSelector: '.grid-item',
	 masonry: {
	     columnWidth: 100
	 }
	});
    </script>
</body>

    """)


    hugopage = Template("""
+++
title = "${album.get_name()}"
date = ""

cover = ""
summary ="gettitle"
files = ${album.get_preview_list()}
+++
<div class="my-gallery" itemscope itemtype="http://schema.org/ImageGallery">
    % for p in pics:
        ${p.get_hugotag()}
    % endfor
</div>
    """)
    
    def __init__(self, args, path):
        self._args = args
        self._path = path
        self._files = []
        super(album, self).__init__()
        self.scan()

    def base_dir(self):
        return os.path.join(self._path,"photos");
    def thumb_dir(self):
        return os.path.join(self._path,"thumbs");
    def page_file(self):
        return os.path.join(self._path,"index.html");
    def hugo_file(self):
        return os.path.join(self._args.hugo,self.get_filename()+".md");
    def rel_path(self,fn):
        return fn[self._args.staticprefix:]

    
    def get_preview_list(self):
        files = self._files[0:8];
        return "[ {} ]".format(",".join(['["{}","rotate-{}"]'.format(f.get_thumb(),f.get_rotation()) for f in files]))
    
    def get_filename(self):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        valid_chars = re.sub('[\(\) ]', '', valid_chars)
        return ''.join(c for c in self.get_name() if c in valid_chars)
    def get_name(self):
        return str(self._c['title'])
    def get_date(self):
        return self._c['title']
        
    
    def scan(self):
        yf = os.path.join(self._path,"album.yml")
        if os.path.isfile(yf):
            with open(yf) as stream:
                try:
                    self._c = yaml.load(stream)
                    print(str(self._c))
                    print("Process album {}".format(self.base_dir()))
                    self._files = [ pic(self, os.path.join(self.base_dir(),f)) \
                                    for f in os.listdir(self.base_dir()) \
                                    if os.path.isfile(os.path.join(self.base_dir(),f)) ]
                except yaml.YAMLError as e:
                    print(e)

    def tile(self):
        if (len(self._files)):
            f = self._files[0:8]
            return album.preview.render(album=self,pics=self._files[0:8]);
        return ""
        
    def gen_album(self):
        if (len(self._files)):
            f = self._files
            m = album.hugopage.render(album=self,pics=self._files);
            with open(self.hugo_file(),"w") as f:
                f.write(m)
        return ""
    
    
