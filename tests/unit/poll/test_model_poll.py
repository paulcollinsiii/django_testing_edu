import datetime
import mock
import pytz

# Must be done BEFORE importing any models or other django related bits
from ..dj_nosettings import nosettings
nosettings(INSTALLED_APPS=['django.contrib.auth'])

from poll import models

class TestPollDateRanges(object):
    @staticmethod
    def get_model(valid_from, valid_to):
        return models.Poll(start=valid_from, end=valid_to)

    @classmethod
    def setupClass(cls):
        cls.today = datetime.datetime.now(tz=pytz.UTC)
        cls.yeyesterday = cls.today - datetime.timedelta(days=2)
        cls.yesterday = cls.today - datetime.timedelta(days=1)
        cls.tomorrow = cls.today + datetime.timedelta(days=1)
        cls.totomorrow = cls.today + datetime.timedelta(days=2)

    def test_valid_range(self):
        mdl = self.get_model(self.yesterday, self.tomorrow)
        assert mdl.is_active() is True

    def test_invalid_past(self):
        mdl = self.get_model(self.yeyesterday, self.yesterday)
        assert mdl.is_active() is False

    def test_invalid_future(self):
        mdl = self.get_model(self.tomorrow, self.totomorrow)
        assert mdl.is_active() is False


@mock.patch('poll.models.Poll.num_responses')
class TestPollMaxVotes(object):
    @staticmethod
    def get_model_set_response(max_votes, num_resp_mock, num_votes):
        num_resp_mock.return_value = num_votes
        return models.Poll(max_num_responses=max_votes)

    def test_no_responses(self, num_resp_mock):
        mdl = self.get_model_set_response(999, num_resp_mock, 0)
        assert mdl.is_active() is True

    def test_less_than_max_responses(self, num_resp_mock):
        mdl = self.get_model_set_response(20, num_resp_mock, 2)
        assert mdl.is_active() is True

    def test_equal_to_max_responses(self, num_resp_mock):
        mdl = self.get_model_set_response(2, num_resp_mock, 2)
        assert mdl.is_active() is False


@mock.patch('poll.models.Poll.num_responses')
class TestPollMaxVotesAndDates(object):
    @staticmethod
    def get_model_set_response(valid_from, valid_to, max_votes, num_resp_mock, num_votes):
        num_resp_mock.return_value = num_votes
        return models.Poll(start=valid_from, end=valid_to, max_num_responses=max_votes)

    @classmethod
    def setupClass(cls):
        cls.today = datetime.datetime.now(tz=pytz.UTC)
        cls.yeyesterday = cls.today - datetime.timedelta(days=2)
        cls.yesterday = cls.today - datetime.timedelta(days=1)
        cls.tomorrow = cls.today + datetime.timedelta(days=1)
        cls.totomorrow = cls.today + datetime.timedelta(days=2)

    def test_no_responses_valid_date(self, num_resp_mock):
        mdl = self.get_model_set_response(self.yesterday, self.tomorrow, 999, num_resp_mock, 0)
        assert mdl.is_active() is True

    def test_no_responses_invalid_date(self, num_resp_mock):
        mdl = self.get_model_set_response(self.yeyesterday, self.yesterday, 999, num_resp_mock, 0)
        assert mdl.is_active() is False

    def test_less_than_max_responses_valid_date(self, num_resp_mock):
        mdl = self.get_model_set_response(self.yesterday, self.tomorrow, 20, num_resp_mock, 2)
        assert mdl.is_active() is True

    def test_less_than_max_responses_invalid_date(self, num_resp_mock):
        mdl = self.get_model_set_response(self.yeyesterday, self.yesterday, 20, num_resp_mock, 2)
        assert mdl.is_active() is False

    def test_equal_to_max_responses_valid_date(self, num_resp_mock):
        mdl = self.get_model_set_response(self.yesterday, self.tomorrow, 2, num_resp_mock, 2)
        assert mdl.is_active() is False

    def test_equal_to_max_responses_invalid_date(self, num_resp_mock):
        mdl = self.get_model_set_response(self.yeyesterday, self.yesterday, 2, num_resp_mock, 2)
        assert mdl.is_active() is False
