from base_test import BaseTestCase


class FollowTestCase(BaseTestCase):
    def test_follow_user(self):
        token = self.create_user('Test User', 1)
        to_follow = self.create_user('Test User To Follow', 2)
        resp = self.post_json('/api/follow', {
            'access_token': token,
            'user_to_follow': 2
        })
        self.assert200(resp)

        resp = self.client.get('/api/my-followers/', environ_base={'HTTP_ACCESS_TOKEN': to_follow})
        self.assertEquals(len(resp.json['followers']), 1)

    def test_no_refollow(self):
        """
        Make sure that you cannot follow the same user twice
        """
        token = self.create_user('Test User', 1)
        to_follow = self.create_user('Test User To Follow', 2)
        resp = self.post_json('/api/follow', {
            'access_token': token,
            'user_to_follow': 2
        })
        self.assert200(resp)

        self.client.get('/api/my-followers/', environ_base={'HTTP_ACCESS_TOKEN': to_follow})
        resp = self.client.get('/api/my-followers/', environ_base={'HTTP_ACCESS_TOKEN': to_follow})
        self.assertEquals(len(resp.json['followers']), 1)


class FeedTestCase(BaseTestCase):
    def test_empty_feed(self):
        """
        Make sure that you can get an empty feed
        """
        token = self.create_user('Test User', 1)
        resp = self.client.get('/api/feed', environ_base={'HTTP_ACCESS_TOKEN': token})
        self.assertEquals(resp.json['total-items'], 0)

    #def test_follow_feed(self):
        """
        Make sure that follow actions end up in the feed
        """
