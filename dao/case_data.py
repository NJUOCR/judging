from pymongo import MongoClient
from dao.graph_data import GraphData


class CaseData:
    table = MongoClient('101.132.40.25', 27017).get_database('judging').get_collection('case')

    def __init__(self, d: dict, case_id: str):
        self.d = d
        self.case_id = case_id
        self.d['_id'] = case_id

    @staticmethod
    def create_case(graph_name: str, case_id: str) -> 'CaseData':
        d = GraphData().fetch(graph_name)
        if d is not None:
            d['_id'] = case_id
            CaseData.table.insert_one(d)
            return CaseData(d, case_id)
        else:
            return None

    @staticmethod
    def fetch_case(case_id: str) -> 'CaseData':
        d = CaseData.table.find_one({'_id': case_id})
        return CaseData(d, case_id) if d is not None else None

    @staticmethod
    def fetch_cases(graph_name: str) -> list:
        cursors = CaseData.table.find({'名称': graph_name}, {'_id': 1})
        cases = []
        for case in cursors:
            cases.append(case['_id'])
        return cases

    @property
    def data(self) -> dict:
        return self.d

    def update(self, d: dict = None):
        """

        :param d: use a new document to override the old
        :return: True if have tried to update, else False
        """
        if d is None:
            CaseData.table.save(self.d)
            return True
        elif '_id' in d and d['_id'] != self.case_id:
            print('案号不一致')
            return False
        else:
            CaseData.table.save(d)
            self.d = CaseData.table.find_one({'_id': self.case_id})
            return True

    @staticmethod
    def remove(case_id: str):
        CaseData.table.remove(case_id)

    @staticmethod
    def removeAll(graph_name: str):
        CaseData.table.remove({'名称': graph_name})

