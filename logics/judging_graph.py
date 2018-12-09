import json

from dao.graph_data import GraphData


class JudgingGraph:
    _data: GraphData = GraphData()

    def __init__(self, d=None):
        self._definition: dict = d

    def define(self, d: dict) -> 'JudgingGraph':
        self._definition = d
        return self

    @staticmethod
    def from_json(d: dict) -> 'JudgingGraph':
        graph = JudgingGraph(d)
        return graph

    @staticmethod
    def from_file(file_path: str) -> 'JudgingGraph':
        with open(file_path, encoding='utf-8') as f:
            d = json.load(f)
            return JudgingGraph.from_json(d)

    @staticmethod
    def from_db(graph_name: str) -> 'JudgingGraph':
        d = JudgingGraph._data.fetch(graph_name)
        return JudgingGraph(d) if d else None

    def save(self):
        JudgingGraph._data.save(self._definition)

    def validate(self) -> bool:
        dic: dict = self._definition
        try:
            if len(dic.keys()) != 2:
                return False
            if not isinstance(dic["名称"], str):
                return False
            temp = dic["证据链条"]
            if not isinstance(temp, list):
                return False
            for i in temp:
                if len(i.keys()) != 2:
                    return False
                if not isinstance(dic["名称"], str):
                    return False
                temp1 = i["查证事项"]
                if not isinstance(temp1, list):
                    return False
                for j in temp1:
                    if len(j.keys()) != 2 and len(j.keys()) != 3:
                        return False
                    if not isinstance(dic["名称"], str):
                        return False
                    temp2 = j["概要"]
                    if not isinstance(temp1, list):
                        return False
                    for p in temp2:
                        if len(p.keys()) != 2:
                            return False
                        if not isinstance(p["名称"], str):
                            return False
                        if not (isinstance(p["内容"], str) or isinstance(p["内容"], list)):
                            return False
                    if '印证证据' in j.keys():
                        temp3 = j['印证证据']
                        for q in temp3.values():
                            if not isinstance(q, list):
                                return False
        except KeyError:
            return False
        return True

    @property
    def definition(self) -> dict:
        return self.definition
    
    @staticmethod
    def translate_definition(to: str, d: dict) -> dict:
        assert to in ('en', 'zh')
        d_copy = d.copy()
        # todo ...
        return d_copy


if __name__ == "__main__":
    a = JudgingGraph.from_file("static/graph_configs/default.json")
    print(a.validate())
