import dao.document_data as doc_data
from typing import Iterable, List, Tuple
from werkzeug.datastructures import FileStorage

from dao.case_data import CaseData
from dao.media_data import MediaData
from logics.media_resource import MediaResource
from logics.translation import translate_json, translate_key


class JudgingCase:

    def __init__(self, case_id: str, graph_name: str = None):
        """
        尝试根据案号获取一个案件实例，如果失败，则尝试根据图名新建一个实例
        :param case_id: 案号
        :param graph_name: 链式证据模板名称（案由）名称
        """
        self.case_id = case_id
        self.data_obj = CaseData.fetch_case(case_id) or CaseData.create_case(graph_name, case_id)

    def exists(self) -> bool:
        return self.data_obj is not None

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

    @staticmethod
    def update_case(case: dict):
        """
        保存最新案件数据
        :param case: 使用case覆盖原来的数据
        :return:
        """
        case_zh = translate_json(case, to='zh')
        case_data = CaseData(case_zh, case_zh['_id'])
        return case_data.update(case_zh)

    def get_data(self, lang: str = 'zh'):
        """
        获取该案件的json数据
        :param lang: 选择语言，前端中key需要翻译为英文
        :return:
        """
        assert lang in ('en', 'zh')
        return self.data_obj.d if lang == 'zh' else translate_json(self.data_obj.d, to='en')

    # Not in use
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
        for node, level in zip(tree_nodes[1:], hierarchy):
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

    # Not in use
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
        for node, level in zip(tree_nodes[1:], hierarchy):
            items = ptr[level]
            for idx, item in enumerate(items):
                if item['名称'] == node:
                    ptr = items[idx]
                    break
            else:
                # 找不到指定路径
                print(tree_nodes, 'not found')

        """  ptr 现在应该指向, eg.
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
        """
        第一个元素将不会被翻译，因为它是案号
        :param tree: case_id, levels...
        :param to:
        :return:
        """
        return tree[:1] + list(map(lambda node: translate_key(node, to), tree[1:]))

    def save_document(self, file_bundle: List[Tuple[str, FileStorage]]) -> List[str]:
        """
        保存卷宗，图片文件直接保存，PDF先转换为图片再保存
        :param file_bundle: [(file_name, file_obj), ...]
        :return: 图片路径列表
        """
        if len(file_bundle) == 1 and file_bundle[0][0].split('.').pop().lower() == 'pdf':
            paths = doc_data.save_transform_pdf(self.case_id, file_bundle[0][1])
        else:
            paths = doc_data.save_document(self.case_id, [(file, name.split('.').pop()) for name, file in file_bundle])
        return paths

    def get_document_urls(self):
        """
        获取卷宗图片url列表
        :return:
        """
        return list(map(lambda path: '/'+path, doc_data.get_document_paths(self.case_id)))

    def get_headers(self):
        """
        获取目录项的集合，即印证证据所在卷宗页对应的目录，如“询问笔录”、“远程勘验笔录”
        :return: 返回结果中无重复项
        """
        d = self.data_obj.d
        if '目录' in d:
            headers = d['目录']
        else:
            headers = set()
            for first in d['证据链条']:
                for second in first['查证事项']:
                    for third in second['印证证据']:
                        headers.add(third['名称'])
            headers = list(map(lambda h_name: {'名称': h_name, '起始页': None}, headers))
        return translate_json(headers, to='en')
