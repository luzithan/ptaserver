import json

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

def setUp(self):
    self.app = create_app().test_client()

def test_parse(app):
    rv = app.get('/', data=data[0][0])
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result == data[0][1]
