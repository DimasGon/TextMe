import json
import pymongo
import tornado.web
import tornado.ioloop
import tornado.websocket
from tornado import template

class WebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        self.application.webSocketsPool.append(self)

    def on_message(self, message_json):

        db = self.application.db

        message = json.loads(message_json)
        db.chat.insert(message)

        for key, val in enumerate(self.application.webSocketsPool):
            if val != self:
                val.ws_connection.write_message(message)

    def on_close(self, message=None):

        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]

class Application(tornado.web.Application):

    def __init__(self):

        self.webSocketsPool = []

        connection = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = connection.chat

        handlers = (
            ('chat_api/?', WebSocket),
        )

        tornado.web.Application.__init__(self, handlers)

app = Application()
app.listen(8888)
tornado.ioloop.IOLoop.instance().start()
