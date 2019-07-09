from tests import TestCaseBase


class TestTeacherView(TestCaseBase):
    def test_get_view_teachers(self):
        r = self.api('get', '/api/teachers/way_view_teachers?id=2844&day=1')
        # self.assertEqual(len(r), 3)
        #         # self.assertEqual(r[0]['auditory'], 'В-310а')
        #         # self.assertEqual(r[1]['auditory'], 'В-105')
        #         # self.assertEqual(r[2]['auditory'], 'В-105')
        #         # self.assertEqual(r[0]['auditory_id'], 509)
        #         # self.assertEqual(r[1]['auditory_id'], 561)
        #         # self.assertEqual(r[2]['auditory_id'], 561)
        #         # self.assertEqual(r[0]['para'], 3)
        #         # self.assertEqual(r[1]['para'], 4)
        #         # self.assertEqual(r[2]['para'], 5)
        print(r)


    def test_get_view_groups(self):
        r = self.api('get', '/api/groups/way_view_groups?kont_id=22762&day=5')
        # self.assertEqual(len(r), 4)
        # self.assertEqual(r[1]['auditory'], 'В-304')
        # self.assertEqual(r[2]['auditory'], 'В-105')
        # self.assertEqual(r[2]['auditory'], 'В-105')
        # self.assertEqual(r[1]['auditory_id'], 908)
        # self.assertEqual(r[2]['auditory_id'], 561)
        # self.assertEqual(r[3]['auditory_id'], 561)
        # self.assertEqual(r[0]['para'], 2)
        # self.assertEqual(r[1]['para'], 4)
        # self.assertEqual(r[2]['para'], 4)
        # self.assertEqual(r[3]['para'], 5)
        print (r)



