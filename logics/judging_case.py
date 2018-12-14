import os
from typing import Iterable, List, Tuple
from werkzeug.datastructures import FileStorage
from dao.case_data import CaseData
from logics.media_resource import MediaResource
from logics.translation import translate_json, translate_key


class JudgingCase:

    def __init__(self, case_id: str, graph_name: str = None):
        self.data_obj = CaseData.fetch_case(case_id) or CaseData.create_case(graph_name, case_id)

    @staticmethod
    def exists(case_id: str) -> bool:
        return CaseData.fetch_case(case_id) is not None

    def get_data(self, lang: str = 'zh'):
        assert lang in ('en', 'zh')
        return self.data_obj.d if lang == 'zh' else translate_json(self.data_obj.d, to='en')

    def insert_media(self, tree: Iterable, name: str, description: str, file_bundles: List[Tuple[str, FileStorage]]):
        """

        :param tree: 前端传来的数组
        :param name: 媒体文件名称
        :param description: 媒体文件描述
        :param file_bundles: 媒体文件列表，元素为元组 (文件名, 存储对象)
        :return:
        """
        ptr: dict = self.get_data()
        hierarchy = ('证据链条', '查证事项', '印证证据')
        tree_nodes = JudgingCase.translate_tree(tree, to='zh')
        for node, level in zip(tree_nodes, hierarchy):
            items = ptr[level]
            for idx, item in enumerate(items):
                if item['名称'] == node:
                    ptr = items[idx]
                    break
            else:
                # 找不到指定路径
                print(tree_nodes, 'not found')

        """  ptr 现在应该指向
        {
            名称: "视听材料",
            内容: []
        }
        """

        contents: list = ptr['内容']
        sub_path = os.path.join(*tree)
        mr = MediaResource(name, sub_path, description, file_bundles)
        block = mr.save()

        """ block 示例
        { 
            '名称': ...,
            '描述': ...,
            '路径': ...,
            '类型': ...,
        }        
        """
        contents.append(block)
        self.data_obj.update()

    @staticmethod
    def translate_tree(tree: Iterable, to: str) -> Iterable:
        return map(lambda node: translate_key(node, to), tree)
