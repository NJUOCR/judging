from dao.graph_data import GraphData


class GetGraph:
    _data = GraphData()

    def __init__(self):
        self.graph_name: str = None

    def define(self, graph_name: str) -> 'GetGraph':
        self.graph_name = graph_name
        return self

    @staticmethod
    def getInstance(graph_name: str) -> 'GetGraph':
        return GetGraph().define(graph_name)


    def get_graph_from_name(self):
        return self._data.fetch(self.graph_name)
