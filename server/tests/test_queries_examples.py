from tests import TestCaseBase
from models.raspnagr import Auditory

class TestQueriesExamples(TestCaseBase):
    def test_list_all_auds(self):
        print(Auditory.query.all())
