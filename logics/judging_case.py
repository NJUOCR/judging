import os
from typing import Iterable

from dao.case_data import CaseData
from logics.judging_graph import translate_key
from logics.media_resource import MediaResource


class JudgingCase:

    def __init__(self, case_id: str, graph_name: str = None):
        self.data_obj = CaseData.fetch_case(case_id) or CaseData.create_case(graph_name, case_id)

    @staticmethod
    def exists(case_id: str) -> bool:
        return CaseData.fetch_case(case_id) is not None

    def insert_media(self, tree: Iterable, name: str, description: str, file):
        """

        :param tree: 前端传来的数组
        :param name: 媒体文件名称
        :param description: 媒体文件描述
        :param file: 媒体文件
        :return:
        """
        sub_path = os.path.join(*tree)
        mr = MediaResource(name, sub_path, description, file)
        block = mr.save()
        ptr: dict = self.data_obj.data
        hierachy = ('证据链条', '查证事项', '印证证据')
        tree_nodes = JudgingCase.translate_tree(tree, to='zh')
        for node, level in zip(tree_nodes, hierachy):
            items = ptr[level]
            for idx, item in enumerate(items):
                if item['名称'] == node:
                    ptr = items[idx]
                    break
            else:
                # 找不到指定路径
                print(tree_nodes, 'not found')




    @staticmethod
    def translate_tree(tree: Iterable, to: str) -> Iterable:
        return map(lambda node: translate_key(node, to), tree)
