import tornado.web
import requests
from .main import AuthBaseHandler
from untils.photo import UploadImageSave
from untils.account import handlerORM
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient

from .char import ChatSocketHandler,make_chat
import tornado.escape

class URLSaveHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        url = self.get_argument('save_url','')
        resp = requests.get(url)
        ims = UploadImageSave(self.settings['static_path'],'x.jpg')
        ims.save_upload(resp.content)
        ims.make_thumb()

        post = add_post_for(self.current_user,ims.upload_url,ims.thumb_url)
        self.redirect('/post/{}'.format(post.id))


class AsyncURLSaveHandler(AuthBaseHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url = self.get_argument('save_url','')

        is_from_room = self.get_argument('from','') == 'room'
        user = self.get_argument('user','')
        if not (is_from_room and user):
            self.write('wrong call')
            return

        client = AsyncHTTPClient()

        resp = yield client.fetch(url)
        ims = UploadImageSave(self.settings['static_path'],'x.jpg')
        ims.save_upload(resp.body)
        ims.make_thumb()

        post = add_post_for(self.get_current_user(),ims.upload_url,ims.thumb_url)

        chat = make_chat('{} post new_image:http://127.0.0.1:8000/post/{}'.format(user,post.id),img_url=post.thumb_url)

        msg = {
            'html': tornado.escape.to_basestring(
                self.render_string('message.html', message=chat,)
            ),
            'id': chat['id'],
        }
        ChatSocketHandler.update_history(msg)
        ChatSocketHandler.send_updates(msg)
