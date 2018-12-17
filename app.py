import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from handlers import main,auth,char
from handlers import service

define('port',default=8000,help='Listening port',type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',main.IndexHandler),
            (r'/explore',main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
            (r'/upload',main.UploadHandler),
            (r'/login',auth.LoginHandler),
            (r'/signup',auth.SignupHandler),
            (r'/profile',main.ProfileHandler),
            (r'/room',char.RoomHandler),
            (r'/ws',char.ChatSocketHandler),
            (r'/sync',service.URLSaveHandler),
            (r'/save',service.AsyncURLSaveHandler),
        ]

        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static',
            pycket ={
                'engine':'redis',
                'storage':{
                    'host':'localhost',
                    'port':6379,
                    'db_sessions':5,
                    'max_connections':2 ** 30
                },
                'cookies':{
                    'expires_days':30
                },
            },
            cookie_secret = 'hyy12345',
            login_url = '/login'
        )
        super().__init__(handlers,**settings)

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Server start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
