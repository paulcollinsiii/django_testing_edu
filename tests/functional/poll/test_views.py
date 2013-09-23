from django.test import TestCase, client
from django.core.urlresolvers import reverse
from django_nose.tools import assert_code, assert_contains

from . import factories

class TestPollPages(object):
    """
    Want to use a nose test style generator? Have to derive from object.
    The Django TestCase class derives from unittest TestCase which won't work.
    """

    def setUp(self):
        self.client = client.Client()

    def test_smoketest_views(self):
        views_to_check = [reverse('poll:new'),
                          reverse('poll:list')
                          ]
        for v in views_to_check:
            yield self.check_200_resp, v

    def check_200_resp(self, url):
        assert_code(self.client.get(url), 200)


class TestPollDataPages(TestCase):
    def setUp(self):
        self.client = client.Client()

    @staticmethod
    def get_polls():
        return [factories.PollFactory() for x in range(5)]

    def test_poll_list_ok(self):
        url = reverse('poll:list')
        self.get_polls()
        assert_code(self.client.get(url), 200)

    def test_poll_list_all(self):
        url = reverse('poll:list')
        polls = self.get_polls()
        response = self.client.get(url)
        for poll in polls:
            assert_contains(response, poll.question)

    def test_poll_details_ok(self):
        poll = self.get_polls()[0]
        url = reverse('poll:detail', kwargs={'pk': poll.pk})
        assert_code(self.client.get(url), 200)

    def test_poll_details_answers_listed(self):
        poll = self.get_polls()[0]
        url = reverse('poll:detail', kwargs={'pk': poll.pk})
        response = self.client.get(url)
        for answer in poll.answer_set.all().iterator():
            assert_contains(response, answer.text)
