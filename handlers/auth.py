import time
import tornado.web
from untils import account
from pycket.session import SessionMixin

from .main import AuthBaseHandler
from untils.account import register


class LoginHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        next = self.get_argument('next','/')
        print(next)
        self.render('login.html',nextname = next )

    def post(self, *args, **kwargs):
        nextname = self.get_argument('next',None)
        user = self.get_argument('username',None)
        password = self.get_argument('password',None)

        if account.authenticate(user,password):
            self.set_secure_cookie('tudo_user_info',user)
            self.redirect(nextname)
        else:
            self.write('用户名或密码错误')

class SignupHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('signup.html')
    def post(self, *args, **kwargs):
        name = self.get_argument('username','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')

        # if name and password1 and password2:
        if password1 == password2:
            ret = register(name,password1)
            if ret == 'ok':
                self.set_secure_cookie('tudo_user_info',name)
                self.redirect('/')
            else:
                self.write(ret)
        else:
            self.write('密码不一致')


