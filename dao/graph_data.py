from pymongo import MongoClient
from threading import Lock


class GraphData(object):
    _instance = None
    _instance_lock = Lock()

    def __init__(self):
        self.table = MongoClient(host='nju-vm', port=27017).get_database('judging').get_collection('graph')

    def __new__(cls, *args, **kwargs):
        """
        singleton

        > Multiple `GraphData()` usage will return the same instance
        :param args:
        :param kwargs:
        :return:
        """
        if GraphData._instance is None:
            with GraphData._instance_lock:
                if GraphData._instance is None:
                    GraphData._instance = object.__new__(cls)
        return GraphData._instance

    def exists(self, graph_name: str) -> bool:
        return self.table.count({'_id': graph_name}) > 0

    def save(self, graph: dict) -> bool:
        """
        **Attention: this method will override the exist graph**
        :param graph:
        :return:
        """
        self.table.save({**{'_id': graph['名称']}, **graph})
        return True

    def fetch(self, graph_name: str) -> dict:
        return self.table.find_one({'_id': graph_name})
