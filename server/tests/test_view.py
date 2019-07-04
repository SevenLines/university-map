from tests import TestCaseBase

class TestTeacherView(TestCaseBase):
    def test_get_view(self):
        r = self.api('get', '/api/teachers/way_view?id=3095&day=1')
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0]['auditory'], 'В-310а')
        self.assertEqual(r[1]['auditory'], 'В-105')
        self.assertEqual(r[2]['auditory'], 'В-105')
        self.assertEqual(r[0]['para'], 3)
        self.assertEqual(r[0]['para'], 4)
        self.assertEqual(r[0]['para'], 5)











