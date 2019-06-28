from tests import TestCaseBase


class TestAuditoriesOccupation(TestCaseBase):
    def test_get_groups(self):
        r = self.api('get', '/api/auditories/day-occupation?date=20.05.2019')
        print(r)
