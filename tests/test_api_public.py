from flask import json
from server import get_db
import server
from flask.ext.testing import TestCase
from base_test import BaseTestCase


class ChannelListingTestCase(BaseTestCase):
    def test_no_channels_by_default(self):
        response = self.client.get('/api/channels/')
        self.assertEquals(response.json['total-channels'], 0)
