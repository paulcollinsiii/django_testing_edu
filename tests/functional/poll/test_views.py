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


class TestPollVotePages(TestCase):
    USER_PASSWORD = 'sekret!'

    def setUp(self):
        """
        We want the poll reset between every test, thus this can't be in
        a setupClass method
        """

        self.poll = factories.PollFactory()
        self.url = reverse('poll:vote', kwargs={'pk': self.poll.pk})
        self.user = factories.UserFactory()
        self.user.set_password(self.USER_PASSWORD)
        self.user.save()

    def test_vote_requires_login(self):
        assert_code(self.client.get(self.url), 302)

    def test_vote_simple_view(self):
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)
        assert_code(self.client.get(self.url), 200)

    def test_vote_simple_view_answers_present(self):
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)
        response = self.client.get(self.url)
        for answer in self.poll.answer_set.all():
            assert_contains(response, answer.text)

    def test_vote_inactive_poll_redirect(self):
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)
        self.poll.start = factories.YEYESTERDAY
        self.poll.end = factories.YESTERDAY
        self.poll.save()
        assert_code(self.client.get(self.url), 302)

    def test_vote_saves_to_db(self):
        """
        This is the first test we have that's fairly fragile
        Changing the implementation of the view here could break this test
        even if the view is still doing the right thing!

        This makes it a bit harder to maintain, but that's also kind of
        the price of functional testing
        """

        self.client.login(username=self.user.username, password=self.USER_PASSWORD)
        answer = self.poll.answer_set.all()[0]
        form_data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'1',
            'form-MAX_NUM_FORMS': u'',
            'id_form-0-num_votes': '1',
            'id_form-0-answer_id': answer.pk}
        response = self.client.post(self.url, data=form_data)
        assert_code(response, 302)  # Successful vote posts redirect to poll results


class TestPollResultsView(TestCase):
    USER_PASSWORD = 'sekret!'

    def setUp(self):
        """
        We want the poll reset between every test, thus this can't be in
        a setupClass method
        """

        self.poll = factories.PollFactory()
        self.url = reverse('poll:results', kwargs={'pk': self.poll.pk})
        self.user = factories.UserFactory()
        self.user.set_password(self.USER_PASSWORD)
        self.user.save()

    def test_simple_view(self):
        assert_code(self.client.get(self.url), 200)

    def test_answers_in_view(self):
        response = self.client.get(self.url)
        for answer in self.poll.answer_set.all():
            assert_contains(response, answer.text)
