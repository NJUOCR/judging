# fixme [杨关]转换逻辑迁移到`logics.judging_graph`中的`JudgingGraph.translate_definition()`
# ps. 没必要为转换的逻辑专门写一个工具类，**删除这个类**
class TransferGraph:

    def __init__(self):
        self.graph = None

    def define(self, graph: dict) -> 'TransferGraph':
        self.graph = graph
        return self

    @staticmethod
    def getInstance(graph: dict) -> 'TransferGraph':
        return TransferGraph().define(graph)

    @staticmethod
    def get_eng(name: str):
        if name == "名称":
            return "name"
        elif name == "证据链条":
            return "firstLevelItems"
        return name

    def transfer_graph(self) -> dict:
        optimal_dict = self.graph
        result_dict = {}
        for i in optimal_dict:
            print(i)
            result_dict[TransferGraph.get_eng(i)] = optimal_dict[i]
        print(result_dict)
        return optimal_dict
