import json

from dao.graph_data import GraphData


class JudgingGraph:
    _data = GraphData()

    def __init__(self):
        self.definition: dict = None

    def define(self, d: dict) -> 'JudgingGraph':
        self.definition = d
        return self

    @staticmethod
    def from_json(d: dict) -> 'JudgingGraph':
        graph = JudgingGraph().define(d)
        return graph

    @staticmethod
    def from_file(file_path: str) -> 'JudgingGraph':
        with open(file_path, encoding='utf-8') as f:
            d = json.load(f)
            return JudgingGraph.from_json(d)

    def validate(self) -> bool:
        pass
