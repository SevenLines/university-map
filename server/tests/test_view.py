from namespaces.teachers import TeacherWayView
from tests import TestCaseBase


class TestTeacherView(TestCaseBase):
    def test_get_view(self):
        r = self.api('get', '/api/teachers/way_view?id=3299&day=1')
        aud = r[0]['auditory']
        print(aud)






