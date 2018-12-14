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
        return CaseData(d, case_id) if d is not None else None

    @staticmethod
    def fetch_case(case_id: str) -> 'CaseData':
        d = CaseData.table.find_one({'_id': case_id})
        return CaseData(d, case_id) if d is not None else None

    @property
    def data(self) -> dict:
        return self.d

    def update(self, d: dict):
        if '_id' in d and d['_id'] != self.case_id:
            print('案号不一致')
            return False

        CaseData.table.save(d)
        return True
