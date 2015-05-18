from base_test import BaseTestCase


class ChannelListingTestCase(BaseTestCase):
    def test_no_channels_by_default(self):
        """
        Make sure the channel count is 0 when querying an empty database
        """
        response = self.client.get('/api/channels/')
        self.assertEquals(response.json['total-channels'], 0)

    def test_one_channel(self):
        """
        If you have 1 channel, one should be returned
        """

        # Add channel
        self.create_channel()

        # There should be one channel
        response = self.client.get('/api/channels/')
        self.assertEquals(response.json['total-channels'], 1)
        self.assertEquals(len(response.json['channels']), 1)

    def test_pagination(self):
        """
        Test if the pagination is reasonable
        """

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


class VideoListingTestCase(BaseTestCase):
    def test_no_videos_by_default(self):
        """
        There should be no videos by default
        """
        response = self.client.get('/api/videos/')
        self.assertEquals(response.json['total-videos'], 0)

    def test_one_video(self):
        """
        If you have 1 video, one should be returned
        """

        # Add video and channel
        self.create_channel('test-channel', 'test123')
        self.create_video('test-channel', 'test123', 'my-video', 'My Video')

        # There should be one channel
        response = self.client.get('/api/videos/')
        self.assertEquals(response.json['total-videos'], 1)
        self.assertEquals(len(response.json['videos']), 1)


class UserSearchTestCase(BaseTestCase):
    def test_no_users(self):
        """
        When searching for anything with no users, there should be 0 results
        """

        resp = self.client.get('/api/users/Test Search/')
        self.assertEquals(resp.json['total-users'], 0)

    def test_correct_user(self):
        """
        When there is a user that matches, there should be 1 result
        """

        #self.create_dummy_user()