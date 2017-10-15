import unittest

from dotenv import find_dotenv,load_dotenv

from app import create_app


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        load_dotenv(find_dotenv())
        self.app = create_app().test_client()

    def test_connection(self):
        rv = self.app.get('/')
        pass
