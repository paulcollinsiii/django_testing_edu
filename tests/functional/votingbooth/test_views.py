from django.test import TestCase, client
from django.core.urlresolvers import reverse
from nose.tools.trivial import eq_

class TestVotingBoothPages(TestCase):
    def setUp(self):
        self.client = client.Client()

    def test_index(self):
        url = reverse('home')
        response = self.client.get(url)
        eq_(response.status_code, 200)

