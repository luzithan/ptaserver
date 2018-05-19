import json
import unittest

from app import create_app

data = (
    ('Game.of.Thrones.S07E06.PROPER.720p.HDTV.x264-AVS[eztv].mkv', {'codec': 'x264',
                                                                    'container': 'mkv',
                                                                    'episode': 6,
                                                                    'group': 'AVS[eztv].mkv',
                                                                    'proper': True,
                                                                    'quality': 'HDTV',
                                                                    'resolution': '720p',
                                                                    'season': 7,
                                                                    'title': 'Game of Thrones'}),
)

@pytest.
def setUp(self):
    self.app = create_app().test_client()

def test_parse(app):
    rv = self.app.get('/', data=data[0][0])
    self.assertEquals(200, rv.status_code)
    result = json.loads(rv.data)
    self.assertEquals(data[0][1], result)
