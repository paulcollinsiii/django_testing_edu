import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
import factory
import pytz

from poll import models

TODAY = datetime.datetime.now(tz=pytz.UTC)
YEYESTERDAY = TODAY - datetime.timedelta(days=2)
YESTERDAY = TODAY - datetime.timedelta(days=1)
TOMORROW = TODAY + datetime.timedelta(days=1)
TOTOMORROW = TODAY + datetime.timedelta(days=2)


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


class PollToResultsSignaling(TestCase):
    def test_simple(self):
        poll = PollFactory(start=YESTERDAY, end=TOTOMORROW)
        answer = poll.answer_set.all()[0]
        usr = UserFactory()
        models.Votes.objects.get_or_create(num=100,
                                           answer=answer,
                                           user=usr)
        assert models.PollResult.objects.get(poll=poll, answer=answer).num == 100
