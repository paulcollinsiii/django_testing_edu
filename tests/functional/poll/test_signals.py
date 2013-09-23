from django.core.exceptions import ValidationError
from django.test import TestCase
from nose.tools.trivial import eq_

from poll import models

from . import factories


class PollToResultsSignaling(TestCase):
    def setUp(self):
        self.poll = factories.PollFactory()
        self.answer = self.poll.answer_set.all()[0]
        self.usr = factories.UserFactory()

    def test_simple(self):
        models.Votes.objects.get_or_create(num=models.DEFAULT_GLOBAL_VOTES,
                                           answer=self.answer,
                                           user=self.usr)
        eq_(models.PollResult.objects.get(poll=self.poll, answer=self.answer).total_votes, models.DEFAULT_GLOBAL_VOTES)

    def test_change(self):
        v, _c = models.Votes.objects.get_or_create(num=1,
                                           answer=self.answer,
                                           user=self.usr)
        v.num=models.DEFAULT_GLOBAL_VOTES
        v.save()
        eq_(models.PollResult.objects.get(poll=self.poll, answer=self.answer).total_votes, models.DEFAULT_GLOBAL_VOTES)


class TestUserMaxVotes(TestCase):
    def test_simple(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        uv = factories.UserVotesFactory()
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
                          num=uv.votes_per_poll + 99,
                                    answer=answer,
                                    user=uv.user)

    def test_update(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        uv = factories.UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
                          num=uv.votes_per_poll - 1,
                          answer=answer,
                          user=uv.user)
        vote.num = uv.votes_per_poll + 22
        self.assertRaises(ValidationError, vote.save)

    def test_multi_answer_ok(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = factories.AnswerFactory(poll=poll)
        uv = factories.UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=uv.votes_per_poll / 2,
            answer=answer,
            user=uv.user)
        vote, _c = models.Votes.objects.get_or_create(
            num=uv.votes_per_poll / 2,
            answer=second_answer,
            user=uv.user)

    def test_multi_answer_fail(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = factories.AnswerFactory(poll=poll)
        uv = factories.UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=uv.votes_per_poll,
            answer=answer,
            user=uv.user)
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
            num=1,
            answer=second_answer,
            user=uv.user)


class TestGroupMaxVotes(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.gv = factories.GroupVotesFactory()
        self.user.groups.add(self.gv.group)

    def test_simple(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
                          num=self.gv.votes_per_poll + 99,
                          answer=answer,
                          user=self.user)

    def test_update(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        uv = None
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll - 1,
            answer=answer,
            user=self.user)
        vote.num = self.gv.votes_per_poll + 22
        self.assertRaises(ValidationError, vote.save)

    def test_multi_answer_ok(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = factories.AnswerFactory(poll=poll)
        uv = factories.UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll / 2,
            answer=answer,
            user=self.user)
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll / 2,
            answer=second_answer,
            user=self.user)

    def test_multi_answer_fail(self):
        poll = factories.PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = factories.AnswerFactory(poll=poll)
        uv = factories.UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll,
            answer=answer,
            user=self.user)
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
                          num=1,
                          answer=second_answer,
                          user=self.user)
