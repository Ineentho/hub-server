from base_test import BaseTestCase


class ChannelListingTestCase(BaseTestCase):
    def test_no_channels_by_default(self):
        response = self.client.get('/api/channels/')
        self.assertEquals(response.json['total-channels'], 0)

    def test_one_channel(self):
        # Add channel
        self.create_channel()

        # There should be one channel
        response = self.client.get('/api/channels/')
        self.assertEquals(response.json['total-channels'], 1)

    def test_pagination(self):
        # Add channel
        for i in range(22):
            self.create_channel('test-channel-' + str(i))

        # There should now be one page (20) + 2 channels
        response = self.client.get('/api/channels/2')
        self.assertEqual(response.json['total-channels'], 22)
        self.assertEqual(len(response.json['channels']), 2)

        # And the third page should not exist
        response = self.client.get('/api/channels/3')
        self.assert404(response)