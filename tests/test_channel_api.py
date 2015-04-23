from flask import json
import server
import unittest


class ChannelRegisterTestCase(unittest.TestCase):
    def setUp(self):
        server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        server.app.config['TESTING'] = True
        server.load()
        self.app = server.app.test_client()

    def post_json(self, url, data):
        return self.app.post(url, data=json.dumps(data),
                             headers={'content-type': 'application/json'})

    def tearDown(self):
        pass

    def test_register_no_data(self):
        """
        Test whether the request is denied when supplied no json body
        """

        rv = self.app.post('/channel/register')
        self.assertEqual(rv.status_code, 400)
        self.assertIn(b'not valid JSON', rv.data)

    def test_register_incomplete_data(self):
        """
        Test whether the request is denied when supplied with incorrect data
        """

        # No correct parameters
        rv = self.post_json('/channel/register', {'incorrect': 'incorrect'})
        self.assertIn(b'Invalid parameter', rv.data)
        self.assertEqual(rv.status_code, 400)

    def test_register_name(self):
        """
        Check if register name validation works
        """

        # Too long name
        rv = self.post_json('/channel/register', {'name': 'abc'*50, 'slug': 'a', 'url': 'a', 'password': 'a'})
        self.assertIn(b'may not be longer than', rv.data)
        self.assertEqual(rv.status_code, 400)

        # No name parameter
        rv = self.post_json('/channel/register', {'slug': 'a', 'url': 'a', 'password': 'a'})
        self.assertIn(b'name is required', rv.data)
        self.assertEqual(rv.status_code, 400)

    def test_register_slug(self):
        """
        Check if register slug validation works
        """

        # No slug parameter
        rv = self.post_json('/channel/register', {'name': 'a', 'url': 'a', 'password': 'a'})
        self.assertIn(b'slug is required', rv.data)
        self.assertEqual(rv.status_code, 400)

        # Slug with invalid characters
        rv = self.post_json('/channel/register', {'slug': 'C', 'name': 'a', 'url': 'a', 'password': 'a'})
        self.assertIn(b'slug may only contain', rv.data)
        self.assertEqual(rv.status_code, 400)

        # Too long slug
        rv = self.post_json('/channel/register', {'slug': 'a' * 100, 'name': 'a', 'url': 'a', 'password': 'a'})
        self.assertIn(b'slug may not be longer than', rv.data)
        self.assertEqual(rv.status_code, 400)

    def test_register_url(self):
        """
        Test if url parameter validation works
        """

        # No url parameter
        rv = self.post_json('/channel/register', {'name': 'a', 'slug': 'a', 'password': 'a'})
        self.assertIn(b'url is required', rv.data)
        self.assertEqual(rv.status_code, 400)

        # Too long url
        rv = self.post_json('/channel/register', {'url': 'a' * 300, 'name': 'a', 'slug': 'a', 'password': 'a'})
        self.assertIn(b'url may not be longer than', rv.data)
        self.assertEqual(rv.status_code, 400)

    def test_register_password(self):
        """
        Test URL parameter validation
        """

        # No password parameter
        rv = self.post_json('/channel/register', {'name': 'a', 'slug': 'a', 'url': 'a'})
        self.assertIn(b'password is required', rv.data)
        self.assertEqual(rv.status_code, 400)

    def test_valid_parameters(self):
        """
        Test if a channel is created when supplied valid parameters
        """
        return 
        rv = self.post_json('/channel/register', {
            'name': 'test-channel',
            'slug': 'test-channel',
            'url': 'http://test-channel-servrer.opid.io/test-channel',
            'password': 'test123'
        })
        self.assertIn(b'Channel created', rv.data)
        self.assertEqual(rv.status_code, 200)