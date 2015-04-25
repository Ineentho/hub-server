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

    def post_json(self, url, data):
        return self.client.post(url, data=json.dumps(data),
                             headers={'content-type': 'application/json'})
