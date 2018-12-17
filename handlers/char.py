import tornado.websocket
import tornado.escape

from .main import AuthBaseHandler
from pycket.session import SessionMixin
import tornado.web
import uuid
import tornado.httpclient

from untils.photo import UploadImageSave
from untils.account import handlerORM
from untils.photo import UploadImageSave

import tornado.gen
from tornado.ioloop import IOLoop


def make_chat(msg_body,name='system',img_url=None):
    ret = {
        'id':str(uuid.uuid4()) ,
        'body':msg_body,
        'user':name,
        'img_url':img_url,
    }
    return ret


class RoomHandler(AuthBaseHandler):
    """
    聊天室页面
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        print('新的ws连接:%s' % self)
        self.render('room.html',messages=ChatSocketHandler.history)


class ChatSocketHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    """
    处理响应 websocket链接
    """
    waiters = set()
    history = []
    history_size = 200

    #这个会报错
    # def get_current_user(self):
    #     return self.session.get('tudo_user_info',None)

    def get_current_user(self):
        return self.get_secure_cookie('tudo_user_info',None)

    def open(self, *args, **kwargs):
        print('新的ws连接:%s' % self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """
        websocket断开后，自动调用
        :return:
        """
        print("关闭ws connetction:%s"%self)
        ChatSocketHandler.waiters.remove(self)

    @tornado.gen.coroutine
    def on_message(self, message):
        """
        服务端接收消息自动调用
        :param message:
        :return:
        """
        print("得到消息：%s"% message)
        parsed= tornado.escape.json_decode(message)

        body = parsed['body']
        if body and body.startswith('http://'):
            client = tornado.httpclient.AsyncHTTPClient()
            save_api_url  = "http://127.0.0.1:8000/save?save_url={}&user={}&from=room"\
                .format(body,self.current_user.decode('utf-8'))
            IOLoop.current().spawn_callback(client.fetch,save_api_url)
            body = "user {},url {} 上传".format(self.current_user,body)

            chat = make_chat(body)

            msg = {
                'html':tornado.escape.to_basestring(
                    self.render_string('message.html',message=chat,)
                ),
                'id':chat['id'],
            }
            self.write_message(msg)

        else:
            chat = make_chat(body,self.current_user)
            msg = {
                'html':tornado.escape.to_basestring(
                    self.render_string('message.html',message=chat,)
                ),
                'id':chat['id'],
            }

            ChatSocketHandler.update_history(msg)
            ChatSocketHandler.send_updates(msg)



    @classmethod
    def send_updates(cls,msg):
        for w in ChatSocketHandler.waiters:
            w.write_message(msg)

    @classmethod
    def update_history(cls,msg):
        cls.history.append(msg)
        if len(cls.history) > cls.history_size:
            cls.history = cls.history[-cls.history_size]
