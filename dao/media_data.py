import os
from pymongo import MongoClient


class MediaData:
    media_storage_root = os.path.join('static', 'resources', 'media')

    host = '101.132.40.25'
    port = 27017

    def __init__(self):
        self.table = MongoClient(MediaData.host, port=MediaData.port).get_database('judging').get_collection('case')

    def save(self, file, path):
        pass
