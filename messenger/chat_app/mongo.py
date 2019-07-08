# -*- coding: utf-8 -*-

from subprocess import Popen
from os import kill
from signal import SIGTERM
from messenger import settings
from chat_app.models import MongoServerModel, ChatModel
import pymongo
import inspect


def except_timeout_error_wrapper(cls):
    def except_wrapper(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except pymongo.errors.ServerSelectionTimeoutError:
                cls.restart_server()
            return func(*args, **kwargs)
        return wrapper
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        setattr(cls, name, except_wrapper(method))
    return cls


@except_timeout_error_wrapper
class MongoDB:

    @property
    def _get_start_cmd(self):
        if settings.DEBUG:
            return ['mongod', '--dbpath', '/home/gonchar/Projects/text_me/mongo/db']
        else:
            pass

    def __init__(self):
        cmd = self._get_start_cmd
        model = MongoServerModel.get_model()
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.process = Popen(cmd)
        model.is_started = True
        model.process_id = self.process.pid
        print(model.process_id)
        model.save()

    def __del__(self):
        self.process.kill()
        model = MongoServerModel.get_model()
        model.is_started = False
        model.process_id = -1
        model.save()
        del self
    
    def restart_server(self):
        model = MongoServerModel.get_model()
        model.is_started = False
        model.process_id = -1
        model.save()
        try:
            self.process.kill()
        except Exception:
            pass
        self.__init__()

    def get_db(self, db_name):
        db = self.client[db_name]
        return db

    def get_messages_from_db(self, db_name, collection_name):
        db = self.client[db_name]
        messages = reversed([mes for mes in db[collection_name].find()])
        return messages

    def add_message_to_db(self, db_name, collection_name, message):
        db = self.client[db_name]
        messages = db[collection_name]
        messages.insert_one(message)
        chat = ChatModel.objects.get(mongo_collection=collection_name)
        chat.last_message_text = message['text']
        print(message['time'])
        chat.last_message_time = message['time']
        chat.save()
        print(chat.last_message_time)
