from tests import TestCaseBase


class TestAuditoriesOccupation(TestCaseBase):
    def test_get_groups(self):
        r = self.api('get', '/api/auditories/day-occupation?date=20.05.2019')
        print(r)

    def test_get_stat_para(self):
        r = self.api('get', '/api/auditories/statistic-para?auditory_id=908')
        print(r)

    def test_get_stat_day(self):
        r = self.api('get', '/api/auditories/statistic-day?auditory_id=908')
        print(r)
