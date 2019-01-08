import os
from typing import Iterable, List, Tuple
from werkzeug.datastructures import FileStorage

from dao.case_data import CaseData
from dao.media_data import MediaData
from logics.media_resource import MediaResource
from logics.translation import translate_json, translate_key


class JudgingCase:

    def __init__(self, case_id: str, graph_name: str = None):
        # 尝试根据案号获取一个案件实例，如果失败，则尝试根据图名新建一个实例
        self.data_obj = CaseData.fetch_case(case_id) or CaseData.create_case(graph_name, case_id)

    @staticmethod
    def exists(case_id: str) -> bool:
        return CaseData.fetch_case(case_id) is not None

    @staticmethod
    def get_cases(graph_name: str) -> list:
        return CaseData.fetch_cases(graph_name)

    @staticmethod
    def remove_case(case_id) -> bool:
        if JudgingCase.exists(case_id):
            CaseData.remove(case_id)
            return True
        else:
            return False

    def get_data(self, lang: str = 'zh'):
        assert lang in ('en', 'zh')
        return self.data_obj.d if lang == 'zh' else translate_json(self.data_obj.d, to='en')

    def remove_media(self, tree: list):
        """
        移除一个媒体资源，包括相关文件和数据库的记录
        :param tree: 前端传来的数组, 包含子路径下的每一个目录名
        :param name: 媒体文件名称
        :return:
        """
        name = tree[-1]
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

        contents: list = ptr['内容']
        for idx, item in enumerate(map(lambda content: content['名称'], contents)):
            if name == item:
                del contents[idx]
                self.data_obj.update()
                sub_path = '/'.join(tree)
                MediaData.remove_media('/'.join(sub_path))
                return True
        print(name, "not found in", tree_nodes)
        return False

    def insert_media(self, tree: Iterable, name: str, description: str, file_bundles: List[Tuple[str, FileStorage]]):
        """
        尝试插入一个媒体资源。假如编号为 ‘测试编号123’的案件需要在
        ‘c’（证据链条）
            -> ‘死亡时间’       （查证事项）
                -> ‘视听材料’   （印证证据） 之下插入一个名为
                    -> ‘法医报告’ 的图片 （可以是多张图片）
                    和一个名为
                    -> ‘法医鉴定’的音频记录 (音频和视频只能是一个）

        那么目录结构会是这样
        |- [resource-root]                  // 目前的定义是 `static/resources`
            |- 查找被害人，确认死者身份
                |- 死亡时间
                    |- 法医报告
                        |- 报告图片1.jpg
                        |- 报告图片2.jpg
                    |- 法医鉴定
                        |- DieDieDie.mp3

        > 这里说的***一个***媒体资源事实上指：
        > - 一个视频文件或音频文件
        > - 或，一组图片
        :param tree: 前端传来的数组, 包含子路径下的每一个目录名
        :param name: 媒体文件名称，并不是原始文件的名称，注意区别。这是在上传文件时，用户起的名字
        :param description: 媒体文件描述
        :param file_bundles: 媒体文件列表，元素为元组 (文件名, 存储对象)
        :return: 如果成功插入，返回True；如果数据库中有重名媒体资源，返回False
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
        # if name in map(lambda content: content['名称'], contents):
        #     return False
        sub_path = '/'.join(tree)
        mr = MediaResource.instance(name, sub_path, description, file_bundles)
        block = mr.save()

        """ block 示例
        { 
            '名称': ...,
            '描述': ...,
            '路径': ...,
            '类型': ...,
        }        
        """
        for idx, item in enumerate(map(lambda content: content['名称'], contents)):
            if name == item:
                del contents[idx]
        contents.append(block)
        self.data_obj.update()
        return True

    @staticmethod
    def translate_tree(tree: Iterable, to: str) -> Iterable:
        return map(lambda node: translate_key(node, to), tree)
