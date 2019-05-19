import json
from unittest import TestCase

from server.base import app


class TestCaseBase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def api(self, method, *args, **kwargs):
        r = getattr(self.app, method)(*args, **kwargs)
        self.assertEqual(200, r.status_code)
        return json.loads(r.data)


class TestAuditoriesOccupation(TestCaseBase):
    def test_get_groups(self):
        r = self.api('get', '/api/auditories/day-occupation?date=20.05.2019')
        print(r)