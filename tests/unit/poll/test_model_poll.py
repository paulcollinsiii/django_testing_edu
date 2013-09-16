import datetime
import pytz

# Must be done BEFORE importing any models or other django related bits
from ..dj_nosettings import nosettings
nosettings()

from poll.models import Poll

class TestPollDateRanges(object):
    @staticmethod
    def get_model(valid_from, valid_to):
        return Poll(start=valid_from, end=valid_to)

    @classmethod
    def setupClass(cls):
        cls.today = datetime.datetime.now(tz=pytz.UTC)
        cls.yeyesterday = cls.today - datetime.timedelta(days=2)
        cls.yesterday = cls.today - datetime.timedelta(days=1)
        cls.tomorrow = cls.today + datetime.timedelta(days=1)
        cls.totomorrow = cls.today + datetime.timedelta(days=2)

    def test_valid_range(self):
        mdl = self.get_model(self.yesterday, self.tomorrow)
        assert mdl.is_active()

    def test_invalid_past(self):
        mdl = self.get_model(self.yeyesterday, self.yesterday)
        assert not mdl.is_active()

    def test_invalid_future(self):
        mdl = self.get_model(self.tomorrow, self.totomorrow)
        assert not mdl.is_active()
