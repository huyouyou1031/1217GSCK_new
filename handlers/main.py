import tornado.web
import glob
from PIL import Image
import os
from pycket.session import SessionMixin

from untils import photo
from untils.account import handlerORM
from models.db import DBSession

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        current = self.get_secure_cookie('tudo_user_info')
        if current:
            return current
        else:
            None
    """
    重写两个方法，验证session
    """
    def prepare(self):
        self.db_session = DBSession()
        self.orm = handlerORM(self.db_session)


    def on_finish(self):
        self.db_session.close()


class IndexHandler(AuthBaseHandler):
    '''
    首页，显示用户关注图片流
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        posts = self.orm.get_post_for(self.current_user)
        # print(name)
        self.render('index.html',posts = posts)


class ExploreHandler(AuthBaseHandler):
    '''
    发现页，最近上传的图片
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        posts = self.orm.get_all_posts()
        self.render('explore.html',posts = posts)

class PostHandler(AuthBaseHandler):
    '''
    单个图片详情页
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        post = self.orm.get_post(kwargs['post_id'])
        if post:
            like_count = self.orm.get_like_count(post)
            self.render('post.html',post=post,like_count=like_count)
        else:
            self.write('post_id {} is wrong'.format(kwargs['post_id']))

class UploadHandler(AuthBaseHandler):
    '''
    上传图片
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        file_list = self.request.files.get('newimg',None)
        # print(file_list)
        post_id = 0
        for ul in file_list:
            name = ul['filename']
            content = ul['body']
            img = photo.UploadImageSave(self.settings['static_path'],name)
            img.save_upload(content)
            img.make_thumb()

            post = self.orm.add_post_for(self.current_user,img.upload_url,img.thumb_url)
            print(post)
            post_id = post.id

        self.redirect('/post/{}'.format(post_id))

class ProfileHandler(AuthBaseHandler):
    def get(self,*args,**kwargs):
        username = self.get_argument('name','')
        if not username:
            username = self.current_user
        user = self.orm.get_user(username)

        like_posts = self.orm.get_like_posts(user)
        self.render('profile.html',user=user,like_posts=like_posts)
