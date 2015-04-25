from flask import json
from server import get_db
import server
from flask.ext.testing import TestCase


class BaseTestCase(TestCase):
    def create_app(self):
        return server.create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres@db:5432/'
        })

    def setUp(self):
        get_db().drop_all()
        get_db().create_all()

    def tearDown(self):
        get_db().session.remove()
        get_db().drop_all()

    # Utils used across all tests

    def create_channel(self, slug='test-channel', password='test123'):
        return self.post_json('/channel/register', {
            'name': 'test-channel',
            'slug': slug,
            'url': 'http://test-channel-servrer.opid.io/test-channel',
            'password': password
        })

    def create_video(self, slug='test-channel', password='test123', video_slug='video-slug', video_name='video_name'):
        return self.post_json('/channel/newvideo', {
            'channel-slug': slug,
            'channel-password': password,
            'video-slug': video_slug,
            'video-name': video_name
        })


    def post_json(self, url, data):
        return self.client.post(url, data=json.dumps(data),
                             headers={'content-type': 'application/json'})
