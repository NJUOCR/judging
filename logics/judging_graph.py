import json
from logics.translation import translate_json
from dao.graph_data import GraphData
from dao.case_data import CaseData


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
                        if 3 < len(p.keys()) or len(p.keys()) < 2:
                            return False
                        if not isinstance(p["名称"], str):
                            return False
                        if not (isinstance(p["内容"], str) or isinstance(p["内容"], list)):
                            return False
                        if "类型" in p and not isinstance(p["类型"], str):
                            return False
                    if '印证证据' in j.keys():
                        temp3 = j['印证证据']
                        for q in temp3:
                            if len(q.keys()) != 2:
                                return False
                            if not isinstance(q["名称"], str):
                                return False
                            if not (isinstance(q["内容"], str) or isinstance(q["内容"], list)):
                                return False
        except KeyError:
            return False
        return True

    def get_definition(self, lang='zh') -> dict:
        assert lang in ('zh', 'en')
        return self._definition if lang == 'zh' else JudgingGraph.translate_definition(self._definition, 'en')

    @staticmethod
    def translate_definition(d: dict, to: str) -> dict:
        return translate_json(d, to)

    @staticmethod
    def get_graph_list():
        return JudgingGraph._data.get_graph_list()

    @staticmethod
    def remove_graph(graph_name: str) -> bool:
        if JudgingGraph._data.exists(graph_name):
            JudgingGraph._data.remove_graph(graph_name)
            CaseData.removeAll(graph_name)
            return True
        else:
            return False


if __name__ == "__main__":
    a = JudgingGraph.from_file("static/graph_configs/default.json")
    print(a.validate())
