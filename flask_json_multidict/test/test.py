from unittest import TestCase
from flask_json_multidict import flask_json_multidict


class TestRunFunction(TestCase):
    def test_run_exists(self):
        self.assertTrue(bool(flask_json_multidict.run))
