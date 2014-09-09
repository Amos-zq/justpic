#!/usr/bin/env python
# encoding: utf-8

import tornado
import os
import tornado.web

from tornado.options import define,options

define("port",default=8888,help="run on the given port",type=int)

class Applicaiton(tornado.web.Application):
    def __init__(self):
        handlers=[
                (r"/",HomeHandler),
        ]
        settings=dict(
                template_path=os.path.join(os.path.dirname(__file__),"templates"),
                static_path=os.path.join(os.path.dirname(__file__),"static"),
                xsrf_cookies=True,
                cookie_secret="_TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                login_url="/auth/login",
                debug=True,
                )
        tornado.web.Application.__init__(self,handlers,**settings)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def attribute(self):
        return "my attribute"

class HomeHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        pass
