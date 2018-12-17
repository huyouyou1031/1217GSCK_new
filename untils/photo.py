from PIL import Image
import os
import uuid




class UploadImageSave(object):
    upload_dir = 'uploads'
    thumb_dir = 'suolue'
    size = (200, 200)

    def __init__(self,static_path,name):
        self.static_path = static_path
        self.name = name
        self.new_name = self .get_new_name

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir,self.new_name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path,self.upload_url)

    @property
    def get_new_name(self):
        _,ext = os.path.splitext(self.name)
        new_name = uuid.uuid4().hex + ext
        return new_name

    def save_upload(self,content):
        with open(self.upload_path,'wb') as f:
            f.write(content)

    @property
    def thumb_url(self):
        filename,ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}*{}'.format(filename,self.size[0],self.size[1]) + ext
        return os.path.join(self.upload_dir,self.thumb_dir,thumb_name)

    def make_thumb(self):
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        save_thumb = os.path.join(self.static_path,self.thumb_url)
        im.save(save_thumb)
