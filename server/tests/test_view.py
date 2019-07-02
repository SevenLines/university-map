from tests import TestCaseBase


class TestTeacherView(TestCaseBase):
    def test_get_view(self):
        r = self.api('get', '/api/teachers/WayView?id=3299&day=1')
        print(r)
