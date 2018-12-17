# import tornado.ioloop
# import tornado.web
#
# class MainHandler(tornado.web.RequestHandler):
#     #get请求，输出hello,world
#     def get(self):
#         self.write("Hello, world")
#
# def make_app():
#     #实例化路由
#     return tornado.web.Application([
#         (r"/", MainHandler),
#     ])
#
# if __name__ == "__main__":
#     print('测试是否运行')
#     #实例化路由 赋值给app实例
#     app = make_app()
#     app.listen(8000)
#     tornado.ioloop.IOLoop.current().start()

