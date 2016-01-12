'''
Created on Nov 24, 2015

@author: tguo
'''


# coding=UTF-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from TwentyEightyStrategy_single import *

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # greeting = self.get_argument('greeting', 'Hello')
        # self.write(greeting + ', welcome you to read: www.itdiffer.com')
        self.write(Message.info) # add message

if __name__ == "__main__":
    calcreturn()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()