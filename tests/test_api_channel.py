from flask import json
from base_test import BaseTestCase


class ChannelRegistrationTestCase(BaseTestCase):

    def create_channel(self):
        return self.post_json('/channel/register', {
            'name': 'test-channel',
            'slug': 'test-channel',
            'url': 'http://test-channel-servrer.opid.io/test-channel',
            'password': 'test123'
        })

    def test_register_no_data(self):
        """
        Test whether the request is denied when supplied no json body
        """

        rv = self.client.post('/channel/register')
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

        # 0 Channels before
        rv = self.client.get('/api/channels/')
        self.assertEqual(json.loads(rv.data)['total-channels'], 0)

        # Add channel
        rv = self.post_json('/channel/register', {
            'name': 'test-channel',
            'slug': 'test-channel',
            'url': 'http://test-channel-servrer.opid.io/test-channel',
            'password': 'test123'
        })
        self.assertIn(b'Channel created', rv.data)
        self.assertEqual(rv.status_code, 200)

        # Should be 1 channel now
        rv = self.client.get('/api/channels/')
        self.assertEqual(json.loads(rv.data)['total-channels'], 1)

    def test_no_duplicate_slug(self):
        """
        Make sure there cannot be any duplicate slugs
        """

        # First should succeed
        rv = self.create_channel()
        self.assertEqual(rv.status_code, 200)

        # And next with same params should be taken
        rv = self.create_channel()
        self.assertIn(b'slug is already in use', rv.data)
        self.assertEqual(rv.status_code, 400)