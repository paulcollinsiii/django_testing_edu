import datetime

from django.contrib.auth import get_user_model, models as auth_models
from django.core.exceptions import ValidationError
from django.test import TestCase
import factory
from nose.tools.trivial import eq_
import pytz

from poll import models

TODAY = datetime.datetime.now(tz=pytz.UTC)
YEYESTERDAY = TODAY - datetime.timedelta(days=2)
YESTERDAY = TODAY - datetime.timedelta(days=1)
TOMORROW = TODAY + datetime.timedelta(days=1)
TOTOMORROW = TODAY + datetime.timedelta(days=2)

USER_VOTES_PER_POLL = 10

class AnswerFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Answer

    text = factory.Sequence(lambda n: 'Answer {}'.format(n))


class PollFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Poll

    question = factory.Sequence(lambda n: 'Poll question {}'.format(n))
    answers = factory.RelatedFactory(AnswerFactory, 'poll')
    start = YESTERDAY
    end = TOMORROW


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda n: 'user_{}'.format(n))
    email = factory.LazyAttribute(lambda a: '{}@brightscope.com'.format(a.username))

class GroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = auth_models.Group

    name = factory.Sequence(lambda n: 'group_{}'.format(n))


class UserVotesFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.UserVotes

    votes_per_poll = USER_VOTES_PER_POLL
    user = factory.SubFactory(UserFactory)


class GroupVotesFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.GroupVotes

    votes_per_poll = USER_VOTES_PER_POLL / 2
    group = factory.SubFactory(GroupFactory)


class PollToResultsSignaling(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.answer = self.poll.answer_set.all()[0]
        self.usr = UserFactory()

    def test_simple(self):
        models.Votes.objects.get_or_create(num=100,
                                           answer=self.answer,
                                           user=self.usr)
        eq_(models.PollResult.objects.get(poll=self.poll, answer=self.answer).total_votes, 100)

    def test_change(self):
        v, _c = models.Votes.objects.get_or_create(num=100,
                                           answer=self.answer,
                                           user=self.usr)
        v.num=25
        v.save()
        eq_(models.PollResult.objects.get(poll=self.poll, answer=self.answer).total_votes, 25)


class TestUserMaxVotes(TestCase):
    def test_simple(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        uv = UserVotesFactory()
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
                          num=uv.votes_per_poll + 99,
                                    answer=answer,
                                    user=uv.user)

    def test_update(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        uv = UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
                          num=uv.votes_per_poll - 1,
                          answer=answer,
                          user=uv.user)
        vote.num = uv.votes_per_poll + 22
        self.assertRaises(ValidationError, vote.save)

    def test_multi_answer_ok(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = AnswerFactory(poll=poll)
        uv = UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=uv.votes_per_poll / 2,
            answer=answer,
            user=uv.user)
        vote, _c = models.Votes.objects.get_or_create(
            num=uv.votes_per_poll / 2,
            answer=second_answer,
            user=uv.user)

    def test_multi_answer_fail(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = AnswerFactory(poll=poll)
        uv = UserVotesFactory()
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
        self.user = UserFactory()
        self.gv = GroupVotesFactory()
        self.user.groups.add(self.gv.group)

    def test_simple(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
                          num=self.gv.votes_per_poll + 99,
                          answer=answer,
                          user=self.user)

    def test_update(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        uv = None
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll - 1,
            answer=answer,
            user=self.user)
        vote.num = self.gv.votes_per_poll + 22
        self.assertRaises(ValidationError, vote.save)

    def test_multi_answer_ok(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = AnswerFactory(poll=poll)
        uv = UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll / 2,
            answer=answer,
            user=self.user)
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll / 2,
            answer=second_answer,
            user=self.user)

    def test_multi_answer_fail(self):
        poll = PollFactory()
        answer = poll.answer_set.all()[0]
        second_answer = AnswerFactory(poll=poll)
        uv = UserVotesFactory()
        vote, _c = models.Votes.objects.get_or_create(
            num=self.gv.votes_per_poll,
            answer=answer,
            user=self.user)
        self.assertRaises(ValidationError, models.Votes.objects.get_or_create,
                          num=1,
                          answer=second_answer,
                          user=self.user)
