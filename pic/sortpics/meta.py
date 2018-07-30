# https://www.codingforentrepreneurs.com/blog/extract-gps-exif-images-python/

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import os, hashlib, time

class MetaFile(object):
    def __init__(self, img_path, comment=""):
        img_path = os.path.abspath(img_path)
        self.img_path = img_path
        self._md5sum = None
        self._comment = comment
    def md5(self):
        if not (self._md5sum is None):
            return self._md5sum
        hash_md5 = hashlib.md5()
        with open(self.img_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self._md5sum = hash_md5.hexdigest()
        return self._md5sum
    def comment(self):
        return self._comment;
    def date(self):
        d0 = os.path.getctime(self.img_path)
        try:
            d = datetime.fromtimestamp(d0)
        except:
            d = time.mktime(d.timetuple())
        return d

    def canonicalsuffix(self):
        d = self.date()
        p = d.strftime('%Y-%m-%d_%H:%M:%S_')
        b = os.path.basename(self.img_path)
        if (b.startswith(p)):
            f = d.strftime('%Y-%m-%d/')
        else:
            f = d.strftime('%Y-%m-%d/%Y-%m-%d_%H:%M:%S_')
        return "%s_%s" %(f,b)
    
    
class ImageMetaData(MetaFile):
    '''
    Extract the exif data from any image. Data includes GPS coordinates, 
    Focal Length, Manufacture, and more.
    '''
    exif_data = None
    image = None

    def __init__(self, img_path):
        super(ImageMetaData, self).__init__(img_path)
        self.image = Image.open(self.img_path)
        self.get_exif_data()

    def get_exif_data(self):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = self.image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        self.exif_data = exif_data
        return exif_data

    def get_if_exist(self, data, key):
        if key in data:
            return data[key]
        return None

    def convert_to_degress(self, value):

        """Helper function to convert the GPS coordinates 
        stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def get_lat_lng(self):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
        lat = None
        lng = None
        exif_data = self.get_exif_data()
        #print(exif_data)
        if "GPSInfo" in exif_data:      
            gps_info = exif_data["GPSInfo"]
            gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self.convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":                     
                    lat = 0 - lat
                lng = self.convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lng = 0 - lng
        return lat, lng
    
