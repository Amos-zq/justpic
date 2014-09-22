import tornado.ioloop
import tornado.web
import tornadocnauth.Baidu

from tornado import gen

class AuthHandler(tornado.web.RequestHandler, tornadocnauth.Baidu.BaiduMixin):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument('code', None):
            user = yield self.get_authenticated_user(
                redirect_uri='YOUR_REDIRECT_URI',
                client_id=self.settings['baidu_api_key'],
                client_secret=self.settings['baidu_api_secret'],
                code=self.get_argument('code'))
            self.render('main.html', user=user)
        else:
            self.authorize_redirect(
                redirect_uri="YOUR_REDIRECT_URI",
                client_id=self.settings['baidu_api_key']
               )

app = tornado.web.Application([
        ('/', AuthHandler),
        ], baidu_api_key='YOUR_API_KEY',
                              baidu_api_secret='YOUR_API_SECRET', debug=True)

if __name__ == '__main__':
    app.listen(80)
    tornado.ioloop.IOLoop.instance().start()
