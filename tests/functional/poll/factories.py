import datetime

from django.contrib.auth import get_user_model, models as auth_models
import pytz
import factory
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
